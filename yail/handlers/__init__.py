from .consolehandler import ConsoleHandler
from .filehandler import FileHandler
from .sockethandler import SocketHandler
from .webhandler import WebHandler
from .logic import BaseHandler,Enum, HandlerType

class HandlerObject(Enum):
    CONSOLE = ConsoleHandler
    FILE = BaseHandler
    SOCKET = BaseHandler
    WEB = BaseHandler

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att

class HandlerManager:

    _library = {HandlerObject.CONSOLE.name:None,
               HandlerObject.FILE.name:{},
               HandlerObject.SOCKET.name:None,
               HandlerObject.WEB.name:None
            }

    def __init__(self):
        self._library[HandlerObject.CONSOLE.name] = self.create_handler(HandlerObject.CONSOLE)
        self._file_handlers ={}

    @property
    def console(self)->ConsoleHandler:
        return self._library[HandlerObject.CONSOLE.name]

    @property
    def file(self)->dict:
        return self._library[HandlerObject.FILE.name]

    @property
    def socket(self)->SocketHandler:
        return self._library[HandlerObject.SOCKET.name]

    @property
    def web(self)->WebHandler:
        return self._library[HandlerObject.WEB.name]

    def create_handler(self,what:HandlerObject, filehandler_name:str=None)->BaseHandler:
        out = None
        if what == HandlerObject.FILE and filehandler_name is None:
            exit("FileHandler needs a name")
        elif what == HandlerObject.FILE and filehandler_name is not None:
            if filehandler_name not in self.file.keys():
                fh = what.value(HandlerType.by_name(what.name))
                self._library[what.name][filehandler_name] = fh
                out = fh
        else:
            if self._library[what.name] is None:
                hdler = what.value(HandlerType.by_name(what.name))
                self._library[what.name] = hdler
                out = hdler

            else:
                out = self._library[what.name]

        return out

