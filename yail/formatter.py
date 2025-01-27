import re
import inspect
from datetime import datetime
from enum import Enum
from dataclasses import dataclass,field
from yail.logic import LoggerLevel, Registry
from yail.formatter_func import *

class FormTags(Enum):
    DATE = date_func
    PACKAGE = package_func
    MSG = msg_func
    DATA = data_func
    LOGLEVEL = loglevel_func
    LINENO = lineno_func
    LOGGER = logger_func


    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att

def get_tags_old(form:str) -> list:
    re_blob = re.compile('<<([a-z]+ ?[a-z]+)>>')
    # re_blob = re.compile('<<([a-z]+ [a-z]+)>>')
    out =  re.findall(re_blob,form)
    return out




@dataclass
class FormatterTag:
    """
        Holds the format & stringed data and is
        responsible for proper output of the f"" string

    .. note::
        If replace is longer than column it is truncated

    Accpetable values for align:
        - l = left
        - c = centered
        - r = right
    """

    name:str
    replace: str = ""
    column_align: str ="c"
    _column_width: int = 0
    _fixed: bool = True
    _fmt: str = ""
    _is_to_long:bool = False
    _filler_len:int = 0
    _filler = " "
    _align_dict = {'l': '<',
                   'c': '^',
                   'r': '>'
                   }
    cnt:int = 0
    def __post_init__(self):
        self._check_if_to_long()


    def _check_if_to_long(self)->None:
        """
            Sets the appropriate flag for compiling output
        """
        # print("REPL :: ", self.replace)
        repl_len = len(self.replace)
        if  repl_len > self.column_width:
            self._is_to_long = True
        else:
            self._filler_len = self.column_width - repl_len
            self._is_to_long = False
        self._fixed = False if self.column_width == 0 else True
        # print(self._is_to_long," .... ", repl_len,self.column_width)


    @property
    def fmt(self)->str:
        return self._fmt

    @property
    def column_width(self)->int:
        return self._column_width

    def set_column_width(self,width:int)->None:
        self._column_width = width
        self._check_if_to_long()

    def set_fmt(self,fmt:str)->None:
        self._fmt = fmt

    def compile(self)->str:
        fmt: str =""
        if self._fixed:
            if self._is_to_long:
                fmt = f"{self.replace:.{self.column_width}}"
                if self.name == 'package':
                    startpos = len(self.replace)+3 - self.column_width
                    if startpos < 0:
                        startpos = 0
                    new_repl ="".join([x for x in self.replace[startpos:]])
                    align_str = self._align_dict[self.column_align]
                    fmt = f"{new_repl:{self._filler}{align_str}{self._column_width}}"

            if self.replace != "" and not self._is_to_long:
                align_str = self._align_dict[self.column_align]
                fmt = f"{self.replace:{self._filler}{align_str}{self._column_width}}"

        else:
            fmt = f"{self.replace}"

        return fmt

@dataclass
class FormatterTagStruct:
    """
        Configuration class for FormatterTag
    """
    formtag:str = ""
    column_width:str = 0
    column_align:str ="l"
    args:list = field(init=False,default_factory=list)

    def __post_init__(self):
        self.column_width = int(self.column_width)

@dataclass
class FormatterConfig:
    """
        Holds the formats for loglevel
    """
    columns_separator: str = "::"
    _default_cols_len:list = field(init=False, default_factory=list)
    _init_short:str = "date today|26:logger name|20:loglevel name|10"
    _init_long:str = (f"date iso:logger name|8 c:loglevel name|8:"
                      f"lineno pad4|6 c:package mcf args|33 l:"
                      f"msg|70")
    _init_default_attr:str ="active short long"
    _init_log_attr:str ="debug info warning error critical fatal"
    _lib: dict = field(init=False,default_factory=dict)
    _package_members: list = field(init=False, default_factory=str)
    _short:bool = False
    def __post_init__(self):
        self._package_members = ['package','module','class','function']

        def_list = [f"default_{x}" for x in self._init_default_attr.split(" ")]
        def_list.extend([f"log_{x}" for x in self._init_log_attr.split(" ")])
        for x in def_list:
            if x == "default_short":
                self._tokenize_fmt(x,self._init_short)
            else:
                self._tokenize_fmt(x,self._init_long)


    def _tokenize_fmt(self,name:str, configline:str)->list[FormatterTagStruct]:
        tokens = make_tagconfs_from_confline(configline)
        self._lib[name]: list[FormatterTagStruct] = tokens
        if name == "default_long":
            cols = self._extract_colwidths(tokens)
            if cols != self._default_cols_len:
                self._default_cols_len = cols

    def _return_conf(self,name:str)->list[FormatterTagStruct]:
        if name in self._lib:
            tokens = self._lib[name]
            cols = self._extract_colwidths(tokens)
            act_cols = cols
            if cols != self._default_cols_len:
                act_cols = self._default_cols_len
            for i,x in enumerate(tokens):
                x.column_width = act_cols[i]

            return tokens

    def _extract_colwidths(self,tokens:list[FormatterTagStruct])->None:
        tmp=[x.column_width for x in tokens]
        return tmp

    @property
    def default_long(self)->list[FormatterTagStruct]:
        return self._return_conf('default_long')

    @default_long.setter
    def default_long(self, value:str)->None:
        self._tokenize_fmt('default_long',value)
        if not self._short:
            self._lib['default_active'] = self._lib['default_long']

    @property
    def default_short(self)->list[FormatterTagStruct]:
        return self._return_conf('default_short')

    @default_short.setter
    def default_short(self, value):
        self._tokenize_fmt('default_short', value)
        if not self._short:
            self._lib['default_active'] = self._lib['default_long']


    @property
    def default_active(self)->list[FormatterTagStruct]:
        return self._return_conf('default_active')

    @default_active.setter
    def default_active(self, value):
        self._tokenize_fmt('default_active', value)
    @property
    def log_debug(self)->list[FormatterTagStruct]:
        return self._return_conf('log_debug')

    @log_debug.setter
    def log_debug(self, value):
        self._tokenize_fmt('log_debug', value)


    @property
    def log_info(self)->list[FormatterTagStruct]:
        return self._return_conf('log_info')

    @log_info.setter
    def log_info(self, value):
        self._tokenize_fmt('log_info', value)

    @property
    def log_warning(self)->list[FormatterTagStruct]:
        return self._return_conf('log_warning')

    @log_warning.setter
    def log_warning(self, value):
        self._tokenize_fmt('log_warning', value)


    @property
    def log_error(self)->list[FormatterTagStruct]:
        return self._return_conf('log_error')

    @log_error.setter
    def log_error(self, value):
        self._tokenize_fmt('log_error', value)
    @property
    def log_critical(self)->list[FormatterTagStruct]:
        return self._return_conf('log_critical')

    @log_critical.setter
    def log_critical(self, value):
        self._tokenize_fmt('log_critical', value)

    @property
    def log_fatal(self)->list[FormatterTagStruct]:
        return self._return_conf('log_fatal')

    @log_fatal.setter
    def log_fatal(self, value):
        self._tokenize_fmt('log_fatal', value)


    @property
    def package_members(self)->list:
        return self._package_members

    def toggle_short_format(self)->str:
        """
            Toggles sgort format on / off
        """
        # sw = False
        # if not self._short:
        #     sw = True
        self._short = True if not self._short else False
        self.default_active = self.default_long if not self._short else self.default_short

@dataclass
class Formatter:
    """
        Formats the log string

        format strings look like this
            "date today|20:logger name|20 c:loglevel name"

        - ":" a colon delimits tokens.
        - "|" a pipe delimits columns settings inside the token
        - " " a space separates options

        .. note::
            Trailing colons ":" and spaces " " are not stripped.

        Token repesentation:
            "[[tag] [options]*n|[column width] [column alignment]]"



        Allowed tags & Options:

            - date

                * today - date.today "YYYY-MM-DD"
                * isodat - date.now.isoformat "YYYY-MM-DD HH:MM:SS"

                Ex:
                    | date today

            - package

                * pmcf - PackageModuleClassFunction - abbreviation for .settinggs
                * args - show args
                * argsval -show args & value

                Ex:
                    | package mcf args #hides package
                    | package cf argsval #hides package & module

            - msg
                * None

            - data
                * None

            - loglevel
                * name
                * value

            - lineno
                * pad1(0*n) = number padding

                Ex:
                    * lineno pad1 #01
                    * lineno pad1 #100
                    * lineno pad4 #00001
                    * package cf argsval #hides package & module

            - logger
                * None

    """
    logger_name:str
    _conf: FormatterConfig = field(default_factory=FormatterConfig)
    _tags:dict = field(default_factory=dict)
    _col_lens:dict = field(default_factory=dict)

    def __post_init__(self):
        pass

    def _check_tags(self,taglist: list)->dict:
        """
            Convert tag list from format to a dict with tag : Formtag.

            This is a convenience to let the user use a more lexical style for formats, like <<loglevel value>>

        """
        out:dict = {}
        for tag in taglist:
            option=""
            #check for options, delimiter is Whtespace
            if " " in tag:
                option = tag.replace(" ", "_")
            else:
                option = tag
            out[tag] = option.upper()
        return out
    @property
    def format(self)->str:
        return self._active_format
    @property
    def conf(self):
        return self._conf

    def toggle_short_format(self)->str:
        """
            Toggles sgort format on / off
        """
        self._conf.toggle_short_format()
        return self._conf.default_active

    def toggle_data(self)->bool:
        self._show_data = True if not self._show_data else False
        return self._show_data


    def get_tags(self,form:str = None) -> list:
        fmt = form
        if fmt is None:
            fmt =self._conf.default_active
        return fmt

    def replace_format(self,which:str,fmt:str)->None:
        """
            Replace one of the format strings

            allowd for which are
            long, short, datadict
        """
        allowed = ["long", "short", "datadict"]
        if which in allowed:
            setattr(self,f"_format_{which}",fmt)
            setattr(self,f"_active_format",fmt)
            # self._active_format = replace_tag_in_format(self._active_format, 'loggername', self.logger_name)


    def compile(self,msg: str,frame:any, loglevel:LoggerLevel, data=None )->str:
        form = self.get_tags()
        conf = self._conf
        val_table={ 'msg':msg,
                    'loglevel':loglevel,
                    'data':data,
                    'logger':'TEST',
                    'frame':frame
                    }

        out=""
        for i,tagstruct in enumerate(form):
            func = FormTags.by_name(tagstruct.formtag.upper())
            form_data = frame
            if tagstruct.formtag in val_table:
                form_data = val_table[tagstruct.formtag]
            res = func(form_data,*tagstruct.args)

            composite = FormatterTag(tagstruct.formtag,res)
            composite.set_column_width(tagstruct.column_width)
            composite.column_align = tagstruct.column_align

            sep = self._conf.columns_separator

            tmp = f"{composite.compile()}{sep}"
            if i == len(form)-1:
                tmp = tmp[:-2]
            out += tmp

        return out


def make_tagconfs_from_confline(form:str)->list[FormatterTagStruct]:
    options = []
    command = ""
    out =[]
    #Break up the token
    configlines = form.split(":")
    for line in configlines:
        tagstruct = FormatterTagStruct()
        #check for column width
        sp = line.split("|")
        command = sp[0]
        if len(sp) == 2:
            # command = sp[0]
            col_options = sp[1].split()
            tagstruct.column_width = int(col_options[0])
            if len(col_options) == 2:
                tagstruct.column_align = col_options[1]

        command_test = command.split(" ")
        if len(command_test) > 1:
            command = command_test[0]
            options = command_test[1:]

        tagstruct.formtag = command
        tagstruct.args = options
        out.append(tagstruct)
    return out

def tstfunc():
    fmt = Formatter("DDD")
    return fmt.compile_new("TEST", inspect.currentframe(), LoggerLevel.DEBUG)
