import re
import inspect
from dataclasses import dataclass,field
from yail.logic import LoggerLevel, LoggerMessage
from .templater import Templater,FormTags



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


    def get_tags(self,form:LoggerLevel = None) -> list:
        fmt:list = []
        if form is None:
            fmt =self._conf.default_active
        else:
            fmt = self._conf.column_by_name(form)
        print(fmt)
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


    def compile(self,msg_obj:LoggerMessage )->str:
        """
            Compiles the given data into a string

            PARAMETERS:
                - msg(str)
                - frame(any|inspection.Frame)
                - loglevel(LoggerLevel)
                - data(any|None)

            RETURNS:
                - list[FormatterTagStruct]
        """

        form = self.get_tags(msg_obj.log_level)
        # print(form)
        conf = self._conf
        val_table={ 'msg':msg_obj.msg,
                    'loglevel':msg_obj.log_level,
                    'data':msg_obj.data,
                    'logger':msg_obj.logger_name,
                    'frame':msg_obj.frame
                    }

        out=""
        for i,tagstruct in enumerate(form):
            # print(form)

            func = FormTags.by_name(tagstruct.formtag.upper())
            form_data = msg_obj.frame
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



def tstfunc():
    fmt = Formatter("DDD")
    return fmt.compile_new("TEST", inspect.currentframe(), LoggerLevel.DEBUG)
