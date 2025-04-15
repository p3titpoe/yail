import importlib
from enum import Enum
from dataclasses import dataclass,field
from yail.logic import LoggerLevel,LoggerMessage
from .templater import Templater, importfile

class FormatType(Enum):
    CONSOLE = importlib.import_module('yail.formatter.templates.base_console_template','templates')
    FILE = importlib.import_module('yail.formatter.templates.base_file_template','templates')
    SOCKET = importlib.import_module('yail.formatter.templates.base_socket_template','templates')
    WEB = importlib.import_module('yail.formatter.templates.base_web_template','templates')


@dataclass
class BaseFormatter:
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
    _htype:FormatType
    _conf: Templater = None
    _tags:dict = field(default_factory=dict)
    _col_lens:dict = field(default_factory=dict)

    def __post_init__(self):
        self._conf = Templater()
        pass

    @property
    def conf(self):
        return self._conf

    def toggle_short_format(self)->str:
        """
            Toggles sgort format on / off
        """
        self._conf.toggle_short_format()
        return self._conf.default_active

    def get_format(self, form:LoggerLevel = None) -> list:
        fmt:list = []
        if form is None:
            fmt =self._conf.default_active
        else:
            fmt = self._conf.column_by_name(form)
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
                - string
        """

        tmpl = self.get_format(msg_obj.log_level)
        # print(form)
        conf = self._conf


        out=""
        for i,cols in enumerate(tmpl):

            composite = cols.process(msg_obj)
            sep = "::"
            # print(composite)
            tmp = f"{composite}{sep}"
            if i == len(tmpl)-1:
                tmp = tmp[:-2]
            out += tmp

        return out

class ConsoleFormatter(BaseFormatter):
    _colord:bool = False
    _colord_conf:dict = None