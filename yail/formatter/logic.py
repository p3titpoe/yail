import importlib
from enum import Enum
from json import dumps
from dataclasses import dataclass,field
from yail.logic import LoggerLevel,LoggerMessage
from .templater import Templater, BaseColumn

class TemplateType(Enum):
    CONSOLE = importlib.import_module('yail.formatter.templates.base_console_template','templates')
    FILE = importlib.import_module('yail.formatter.templates.base_file_template','templates')
    SOCKET = importlib.import_module('yail.formatter.templates.base_socket_template','templates')
    WEB = importlib.import_module('yail.formatter.templates.base_web_template','templates')
    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att

@dataclass(repr=False)
class BaseFormatter:
    """
        Formats the log string according to columns in templates




    """
    ctype:any
    _ttype:TemplateType = None
    _conf: Templater = None
    _extension:str = None
    _table:dict = field(default_factory=dict)
    _table_row_len = 170
    _table_view:bool = True
    _col_lens:dict = field(default_factory=dict)
    _total_msglen_to_msgcolumn:int = 0
    _total_msglen:int = 0
    _data_frame_end:int  = 0
    _data_view:bool = False


    def __post_init__(self):
        self._total_msglen_to_msgcolumn = 0
        #Loads the tmplate
        hand,self._extension = self.ctype.name.split("_")
        self._ttype = TemplateType.by_name(hand)
        self._conf = Templater(_template_path=self._ttype.value)
        pass

    def __repr__(self):
        txt =self.__class__.__name__
        txt += f"(table_view={self._table_view}, data_view={self._data_view})"
        return txt

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
        """Fetch the columns from given LoggerLevel from Template"""

        fmt:list[BaseColumn] = []
        if form is None:
            fmt =self._conf.default_active
        else:
            fmt = self._conf.column_by_name(form)

        return fmt

    def _compile(self,msg_obj:LoggerMessage, _tmpl:list[BaseColumn]=None )->str:
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
        if _tmpl is not None:
            tmpl = _tmpl

        sep = self._conf._columns_separator
        comps = ""
        self._total_msglen = 0
        self._table = {v._htype.name: v.process(msg_obj) for v in tmpl if v._htype.name != 'DATA'}
        self._data_frame_end = sum([len(v)+len(self._conf._columns_separator) for k,v in self._table.items() if k not in ['DATA','MSG']])-len(self._conf._columns_separator)

        for i,cols in enumerate(tmpl):
            sep = sep
            composite = ""
            if cols._htype.name not in ['DATA']:
                composite = self._table[cols._htype.name]

                if i != 0:
                    composite = f"{sep}{composite}"

                if cols._htype.name == "DATE":
                    self._total_msglen_to_msgcolumn = len(composite)

                self._total_msglen += len(composite)+len(self._conf._columns_separator)

            else:
                if self._data_view:
                    if msg_obj.data is not None:
                        cols._width = self._total_msglen_to_msgcolumn
                        cols._colsep = sep
                        composite = cols.process(msg_obj,self._table_row_len, self._table_view, self._data_frame_end,self._total_msglen_to_msgcolumn)

            comps += composite
        return comps

    def process(self,msg_obj:LoggerMessage)->str:
        """Subscription function for the signaling system"""
        return self._compile(msg_obj)

@dataclass(repr=False)
class ConsoleFormatter(BaseFormatter):
    def __init__(self,ctype:str):

        super().__init__(ctype)
        self._colord:bool = False
        self._colord_conf:dict = None
        self._table_row_prepend:bool = True
        if self._extension == "TXT":
            self._table_view = False


    def make_table_line(self):
        """Create a row line before or after the row"""
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

    def process(self,msg_obj:LoggerMessage)->str:
        """Subscription function for the signaling system"""
        tableview = self.make_table_line()
        out = self._compile(msg_obj)
        if self._table_view:
            if self._table_row_prepend:
                out = tableview+out
            else:
                out += tableview
        return out

@dataclass(repr=False)
class FileFormatter(BaseFormatter):
    def __init__(self,ctype:str):
        super().__init__(ctype)
        _colord:bool = False
        _colord_conf:dict = None
        self._table_row_prepend:bool = True
        if self._extension == "TXT":
            self._table_view = False


    def make_table_line(self):
        """Subscription function for the signaling system"""

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

    def process(self,msg_obj:LoggerMessage)->str:
        """Subscription function for the signaling system"""

        tableview = self.make_table_line()
        out = self._compile(msg_obj)
        if self._table_view:
            if self._table_row_prepend:
                out = tableview+out
            else:
                out += tableview
        return out