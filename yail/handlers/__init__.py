from .consolehandler import ConsoleHandler
from .filehandler import FileHandler
from .sockethandler import SocketHandler
from .webhandler import WebHandler
from .logic import BaseHandler,Enum, HandlerType,HandlerChannelMixer

class HandlerObject(Enum):
    CONSOLE = ConsoleHandler
    FILE = BaseHandler
    SOCKET = BaseHandler
    WEB = BaseHandler

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att

class HandlerRouting:
    console:ConsoleHandler = None
    file:dict[str:FileHandler] = None
    socket:SocketHandler = None
    web:WebHandler = None

class MixerRouting:
    console:HandlerChannelMixer = None
    file:dict[str:HandlerChannelMixer] = None
    socket:HandlerChannelMixer = None
    web:HandlerChannelMixer = None

class HandlerManager:

    _library:dict[str:BaseHandler] = {HandlerObject.CONSOLE.name.lower():None,
               HandlerObject.FILE.name.lower():{},
               HandlerObject.SOCKET.name.lower():None,
               HandlerObject.WEB.name.lower():None
            }
    _handler:HandlerRouting = None
    _mixer:MixerRouting = None

    def __init__(self):
        self._library[HandlerObject.CONSOLE.name.lower()] = self.create_handler(HandlerObject.CONSOLE)
        self._file_handlers ={}
        self._handler = HandlerRouting()
        self._mixer = MixerRouting()
        self.__post_init__()

    def __post_init__(self):
        pass
        # for n in self._library.keys():
        #     setattr(self._handler,n,self._library[n])
        #     setattr(self._mixer,n,self._library[n].mixer)

    @property
    def handlers(self)->dict[str:BaseHandler]:
        return self._library

    @property
    def handler(self)->HandlerRouting:
        for n in self._library.keys():
            print(n)
            setattr(self._handler,n,self._library[n])
        return self._handler

    @property
    def mixer(self)->MixerRouting:
        for k,v in self._library.items():
            if v is not None:
                setattr(self._mixer,k,self._library[k].mixer)
        return self._mixer

    def create_handler(self,what:HandlerObject, filehandler_name:str=None)->BaseHandler:
        out = None
        if what == HandlerObject.FILE and filehandler_name is None:
            exit("FileHandler needs a name")
        elif what == HandlerObject.FILE and filehandler_name is not None:
            if filehandler_name not in self.file.keys():
                fh = what.value(HandlerType.by_name(what.name.lower()))
                self._library[what.name.lower()][filehandler_name] = fh
                out = fh
        else:
            if self._library[what.name.lower()] is None:
                hdler = what.value(HandlerType.by_name(what.name))
                self._library[what.name.lower()] = hdler
                out = hdler

            else:
                out = self._library[what.name]

        return out

