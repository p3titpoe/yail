from dataclasses import dataclass,field
# from yail.logic import LoggerLevel
# from yail.formatter.logic import Formatter
from yail.logic import LoggerMessage
from .logic import BaseHandler,HandlerType


@dataclass
class ConsoleHandler(BaseHandler):

    def __init__(self,handlertype:HandlerType):
        super().__init__(handlertype)
        _colors:bool = False
        _color_engine:any = None

        print(self.muted_channels,"CONSOLE")

    def process(self,msg_obj:LoggerMessage) ->None:
        kk = self._formatter.compile(msg_obj)

        if self.can_pass(lvl=msg_obj.log_level):
            # print(self.can_pass(lvl=msg_obj.log_level))
            print(kk)
        pass

