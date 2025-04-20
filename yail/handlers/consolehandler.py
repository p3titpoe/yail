from dataclasses import dataclass,field
from yail.loggers.logic import LoggerMessage
from yail.signaling import subscribe
from .logic import BaseHandler,HandlerType



@dataclass
class ConsoleHandler(BaseHandler):

    def __init__(self,handlertype:HandlerType):
        super().__init__(handlertype)
        self._colors:bool = False
        self._color_engine:any = None
        self.sys_enabled:bool = True

        subscribe('listener-console','handler-console',self.process)
        subscribe('syscom-listener-console','system-com',self.sys_process)


    def sys_process(self,msg_obj:LoggerMessage)->None:
        if self.sys_enabled:
            self.process(msg_obj)

    def process(self,msg_obj:LoggerMessage) ->None:
        kk = self._formatter.compile(msg_obj)

        if self.can_pass(lvl=msg_obj.log_level):
            # print(self.can_pass(lvl=msg_obj.log_level))
            print(kk)
            pass
