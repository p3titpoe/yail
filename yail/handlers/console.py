from dataclasses import dataclass,field
from yail.logic import LoggerLevel
from yail.formatter.formatter import Formatter
from .logic import BaseHandler,HandlerType
from .. import LoggerMessage


@dataclass
class ConsoleHandler(BaseHandler):
    _colors:bool = False
    _color_engine:any = None

    def __post_init__(self):
        self._htype = HandlerType.CONSOLE
        self._formatter = Formatter('blbl',_conf='conf',_)

    def process_loggermsg(self:LoggerMessage) ->None:
