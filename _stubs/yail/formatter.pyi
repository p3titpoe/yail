import inspect
from .logic import LoggerLevel as LoggerLevel
from _typeshed import Incomplete
from dataclasses import dataclass
from enum import Enum

def iso_date(dummy: str) -> str: ...
def today(dummy: str) -> str: ...
def package(tosplit: inspect.FrameInfo) -> str: ...
def moduul(data: inspect.FrameInfo) -> str: ...
def klass(tosplit: inspect.FrameInfo) -> str: ...
def func(data: inspect.FrameInfo, showargs: bool = False, showargsval: bool = False) -> str: ...
def func_args(data: inspect.FrameInfo) -> str: ...
def func_argsval(data: inspect.FrameInfo) -> str: ...
def msg(inp: str) -> str: ...
def data2str(data: any) -> str: ...
def loglevel2str(data: LoggerLevel) -> str: ...
def loglevel2val(data: LoggerLevel) -> str: ...
def lineno(data: inspect.FrameInfo) -> str: ...

class FormTags(Enum):
    ISODATE = iso_date
    TODAY = today
    PACKAGE = package
    MODULE = moduul
    CLASS = klass
    FUNCTION = func
    FUNCTION_ARGS = func_args
    FUNCTION_ARGSVAL = func_argsval
    MSG = msg
    DATA = data2str
    LOGLEVEL = loglevel2str
    LOGLEVEL_NAME = loglevel2str
    LOGLEVEL_VALUE = loglevel2val
    LINENO = lineno
    @classmethod
    def by_name(cls, name: str): ...

def replace_tag_in_format(form: str, tag: str, repl: str) -> str: ...
def replace_taglist_in_format(form: str, data: dict) -> str: ...
def get_tags(form: str) -> list: ...

ccc: str

@dataclass
class Formatter:
    '''
        Formats the log string

    .. note::
        This needs refactoring to accomodate for a column aproached structure of the messages.

        The idea is to pass a dicr as structre and to build it from there instead like now,
        definig the string and fiddle with it.

        The dict should be structured like this

            name_of_option : length of the column
            ("loglevel value":40,)

        How to:
            Uselful formats
                f"{tag:>10}" -> left align 10
                f"{tag:<10}" -> right align 10
                f"{tag:^10}" -> centered 10
                f"{tag:.10}" -> truncated

            Code
                tag = "loglevel value"
                col_len = structure[tag]
                tag = tag.replace(" ","_")
                func = FormTags.by_name(tag.upper())
                res = func(data) #fetch the data

            Almost same, then
                res_len = len(res)   #check how long the str is
                len_diff = col_len - res_len    #get the len diff between str & col
                if len_diff >= 0:
                    tag_option = f">{len_diff}"
                else:
                    tag_option = f".{col_len}"

                txt = f"{tag:{tag_option}}"


    '''
    logger_name: str
    def __post_init__(self) -> None: ...
    @property
    def format(self) -> str: ...
    def toggle_short_format(self) -> str:
        """
            Toggles sgort format on / off
        """
    def toggle_data(self) -> bool: ...
    def seek_and_replace_taglist_in_format(self, form: str, data: dict) -> str: ...
    def get_tags(self, form: str = None) -> list: ...
    def replace_format(self, which: str, fmt: str) -> None:
        """
            Replace one of the format strings

            allowd for which are
            long, short, datadict
        """
    def compile(self, msg: str, frame: any, loglevel: LoggerLevel, data: Incomplete | None = None) -> str: ...
    def __init__(self, logger_name, _active_format=..., _format_short=..., _format_long=..., _tags=..., _short=..., _show_data=...) -> None: ...
