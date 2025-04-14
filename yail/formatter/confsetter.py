from dataclasses import dataclass,field
from enum import Enum
from .confsetter_func import *
from . import base_template as base_templ

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


def make_tagconfs_from_confline(form:str)->list[FormatterTagStruct]:
    """
        Breaks the format line into columns and their settings for further processing

        PARAMETERS:
            - form(str)

        RETURNS:
            - list[FormatterTagStruct]

    """
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


@dataclass
class FormatterConfig:
    """
        Holds the formats for loglevel
    """
    columns_separator: str = "::"
    _default_cols_len:list = field(init=False, default_factory=list)
    _init_short:str = "date today|26:logger name|20:loglevel name|10"
    _init_long:str = (f"date iso:logger name|8 c:loglevel name|8:"
                      f"lineno pad4|13 c:package mcf args|33 l:"
                      f"msg|100")
    _init_default_attr:str ="active short long"
    _init_log_attr:str ="debug info warning error critical fatal"
    _lib: dict = field(init=False,default_factory=dict)
    _package_members: list = field(init=False, default_factory=str)
    _short:bool = False

    def __post_init__(self):
        self._package_members = ['package','module','class','function']

        def_list = [f"default_{x}" for x in self._init_default_attr.split(" ")]
        # def_list.extend([f"log_{x}" for x in self._init_log_attr.split(" ")])
        def_list.extend([f"log_{x.name.lower()}" for x in LoggerLevel if x.value >= 10])
        for x in def_list:
            if hasattr(base_templ,x):
                self._tokenize_fmt(x,getattr(base_templ,x))

        self._tokenize_fmt('default_active', getattr(base_templ,'default_long'))



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
            # print(act_cols)

            # if cols != self._default_cols_len:
            #     act_cols = self._default_cols_len
            for i,x in enumerate(tokens):
                x.column_width = act_cols[i]

            return tokens

    def _extract_colwidths(self,tokens:list[FormatterTagStruct])->list:
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

    def fmt_by_loglevel(self,loglevel:LoggerLevel):
        fmt_name = f"log_{loglevel.name.lower()}"
        fmt = self._return_conf(fmt_name)
        # print(f"FMT:::   {fmt_name}")
        return fmt


    def use_custom_template(self,path_to_file:str)->None:
        path_to_file = "/mnt/data/Coding/yail/yail/formatter/base_template.py"

        pass

