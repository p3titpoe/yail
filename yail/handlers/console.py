from dataclasses import dataclass,field
from yail.logic import LoggerLevel
# from yail.formatter.logic import Formatter
from yail.handlers.logic import BaseHandler,HandlerType
from yail.logic import LoggerMessage


@dataclass
class ConsoleHandler(BaseHandler):

    def __init__(self,handlertype:HandlerType):
        super().__init__(handlertype)
        _colors:bool = False
        _color_engine:any = None

    def __post_init__(self):
        self._htype = HandlerType.CONSOLE



    def process_loggermsg(self,msg_obj:LoggerMessage) ->None:
        kk = self._formatter.compile(msg_obj)
        print(kk)
        pass

