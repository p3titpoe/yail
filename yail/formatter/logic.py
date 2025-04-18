import importlib
from enum import Enum
from dataclasses import dataclass,field
from yail.logic import LoggerLevel,LoggerMessage
from .templater import Templater, importfile,BaseColumn

class FormatType(Enum):
    CONSOLE = importlib.import_module('yail.formatter.templates.base_console_template','templates')
    FILE = importlib.import_module('yail.formatter.templates.base_file_template','templates')
    SOCKET = importlib.import_module('yail.formatter.templates.base_socket_template','templates')
    WEB = importlib.import_module('yail.formatter.templates.base_web_template','templates')

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att


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
    ctype:any
    _htype:FormatType = None
    _conf: Templater = None
    _table:dict = field(default_factory=dict)
    _table_row_len = 170
    _table_view:bool = False
    _table_row_prepend:bool = True
    _col_lens:dict = field(default_factory=dict)
    _total_msglen_to_msgcolumn:int = 0
    _total_msglen:int = 0
    _data_frame_end:int  = 0
    _data_view:bool = True


    def __post_init__(self):
        self._total_msglen_to_msgcolumn = 0
        self._htype = FormatType.by_name(self.ctype.name)
        self._conf = Templater(_template_path=self._htype.value)
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
        fmt:list[BaseColumn] = []
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

    def make_table_line(self):
        out=""
        if not self._table_row_prepend:
            out += "\n"
        totlen = 0
        cl:list[int] = [len(v)+1 for k,v in self._table.items() if k != "MSG"]
        markers = []
        for k in cl:
            totlen += k
            markers.append(totlen)
        markers.append(self._table_row_len)

        for i in range(1,self._table_row_len+1):
            repl = "—"
            if i in markers:
                repl = self._conf._columns_separator

            out += repl
        if self._table_row_prepend:
            out += "\n"
        return out

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

        tmpl:list[BaseColumn] = self.get_format(msg_obj.log_level)
        # print(tmpl)

        out=""
        sep = self._conf._columns_separator
        comps = ""
        table_view = ""
        self._total_msglen = 0
        self._table = {v._htype.name: v.process(msg_obj) for v in tmpl if v._htype.name != 'DATA'}
        self._data_frame_end = sum([len(v)+len(self._conf._columns_separator) for k,v in self._table.items() if k not in ['DATA','MSG']])-len(self._conf._columns_separator)
        tableview = self.make_table_line()

        for i,cols in enumerate(tmpl):
            sep = sep
            composite = ""
            if cols._htype.name not in ['DATA']:
                composite = self._table[cols._htype.name]

                if i != 0:
                    composite = f"{sep}{composite}"

                # if cols._htype.name != 'MSG':

                if cols._htype.name == "DATE":
                    self._total_msglen_to_msgcolumn = len(composite)

                self._total_msglen += len(composite)+len(self._conf._columns_separator)
                # self._table.append(self._total_msglen+len(sep))
            else:
                if self._data_view:
                    if msg_obj.data is not None:
                        cols._width = self._total_msglen_to_msgcolumn
                        cols._colsep = sep
                        composite = cols.process(msg_obj,self._table_row_len, self._table_view, self._data_frame_end,self._total_msglen_to_msgcolumn)
                        # col_w = self._total_msglen_to_msgcolumn
                        # composite = f"\n{cols.filler:{col_w}}{sep}{composite}"


            comps += composite
        out = comps
        if self._table_view:
            if self._table_row_prepend:
                out = tableview+comps
            else:
                out += tableview

        return out

class ConsoleFormatter(BaseFormatter):
    _colord:bool = False
    _colord_conf:dict = None