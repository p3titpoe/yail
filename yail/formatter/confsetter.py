from pydoc import importfile
from dataclasses import dataclass,field
from yail.formatter.cols_func import *
from yail.formatter import base_template as base_tmpl
from yail.formatter.columns import ColumnType,ColumnSetup,BaseColumn


def make_tagconfs_from_confline(form:str)->list[ColumnSetup]:
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
        tagstruct = ColumnSetup()
        #check for column width
        sp = line.split("|")
        command = sp[0]
        if len(sp) == 2:
            # command = sp[0]
            col_options = sp[1].split()
            tagstruct.width = int(col_options[0])
            if len(col_options) == 2:
                tagstruct.align = col_options[1]

        command_test = command.split(" ")
        if len(command_test) > 1:
            command = command_test[0]
            options = command_test[1:]

        tagstruct.htype = command
        tagstruct.setts = options
        out.append(tagstruct)
    return out


@dataclass
class Templater:
    """
        Holds the configurations(ColumnSetup) from template for loglevels.
        Generates *Column classes
    """
    _name:str = None
    _template_path:str = None
    _columns_separator: str = "::"
    _default_cols_len:list = field(init=False, default_factory=list)
    _init_short:str = "date today|26:logger name|20:loglevel name|10"
    _init_long:str = (f"date iso:logger name|8 c:loglevel name|8:"
                      f"lineno pad4|13 c:package mcf args|33 l:"
                      f"msg|100")
    _init_default_attr:str ="active short long"
    _init_log_attr:str ="debug info warning error critical fatal"
    _lib: dict = field(init=False,default_factory=dict)
    _short:bool = False

    def __post_init__(self):
        if self._name is None:
            exit("Templater has no name!")

        base_templ = base_tmpl
        if self._template_path is not None:
            base_templ = importfile(self._template_path)

        def_list = [f"default_{x}" for x in self._init_default_attr.split(" ")]
        def_list.extend([f"log_{x.name.lower()}" for x in LoggerLevel if x.value >= 10])

        for x in def_list:
            #Get the default Columsetup if there's none provided
            config = getattr(base_tmpl,x)
            if hasattr(base_templ,x):
                config = getattr(base_templ,x)

            self._tokenize_fmt(x,config)

        self._tokenize_fmt('default_active', getattr(base_templ,'default_long'))

    def _tokenize_fmt(self,name:str, configline:str)->None:
        tokens = make_tagconfs_from_confline(configline)
        self._lib[name]: list[ColumnSetup] = tokens

    def _create_colclass(self,conf:ColumnSetup)->BaseColumn:
        colclass = ColumnType.by_name(conf.htype.upper())
        return colclass(conf)

    def _return_col_config(self,name:str)->list[ColumnSetup]:
        tokens = [None]
        if name in self._lib:
            tokens = self._lib[name]
        return tokens

    def _return_conf(self,name:str)->list[BaseColumn]:
        tokens = self._return_col_config(name)
        out = []
        for conf in tokens:
            out.append(self._create_colclass(conf))
        return out

    def _extract_colwidths(self,tokens:list[ColumnSetup])->list:
        tmp=[x.width for x in tokens]
        return tmp

    @property
    def default_long(self)->list[BaseColumn]:
        return self._return_conf('default_long')

    @property
    def default_short(self)->list[BaseColumn]:
        return self._return_conf('default_short')

    @property
    def default_active(self)->list[BaseColumn]:
        return self._return_conf('default_active')

    @property
    def log_debug(self)->list[BaseColumn]:
        return self._return_conf('log_debug')

    @property
    def log_info(self)->list[BaseColumn]:
        return self._return_conf('log_info')

    @property
    def log_warning(self)->list[BaseColumn]:
        return self._return_conf('log_warning')

    @property
    def log_error(self)->list[BaseColumn]:
        return self._return_conf('log_error')

    @property
    def log_critical(self)->list[BaseColumn]:
        return self._return_conf('log_critical')

    @property
    def log_fatal(self)->list[BaseColumn]:
        return self._return_conf('log_fatal')


    def toggle_short_format(self)->str:
        """
            Toggles short format on / off
        """
        self._short = True if not self._short else False
        self.default_active = self.default_long if not self._short else self.default_short

    def column_by_name(self, loglevel:LoggerLevel)->BaseColumn:
        fmt_name = f"log_{loglevel.name.lower()}"
        fmt_class = ColumnType.by_name(loglevel.name)
        fmt = self._return_col_config(fmt_name)
        # print(f"FMT:::   {fmt_name}")
        return fmt

#
# fc = FormatterConfig()
# print(fc.log_info)