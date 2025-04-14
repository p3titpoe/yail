from dataclasses import dataclass,field
from yail.logic import LoggerLevel
from yail.formatter.formatter import Formatter
from yail.handlers.logic import BaseHandler,HandlerType
from yail.logic import LoggerMessage


@dataclass
class ConsoleHandler(BaseHandler):
    _colors:bool = False
    _color_engine:any = None

    def __post_init__(self):
        self._htype = HandlerType.CONSOLE
        self._formatter = Formatter('logger')


    def process_loggermsg(self,msg_obj:LoggerMessage) ->None:
        kk = self.fmt.compile(msg_obj)
        print(kk)
        pass

