from .consolehandler import ConsoleHandler
from .filehandler import FileHandler
from .sockethandler import SocketHandler
from .webhandler import WebHandler
from .logic import BaseHandler,Enum, HandlerType,HandlerChannelMixer
from pathlib import Path
import yail.signaling as sig

class HandlerObject(Enum):
    CONSOLE = ConsoleHandler
    FILE = FileHandler
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
               HandlerObject.FILE.name.lower():None,
               HandlerObject.SOCKET.name.lower():None,
               HandlerObject.WEB.name.lower():None
            }
    _handler:HandlerRouting = None
    _mixer:MixerRouting = None

    def __init__(self):
        self._library[HandlerObject.CONSOLE.name.lower()] = self.create_handler(HandlerObject.CONSOLE)
        self._handler = HandlerRouting()
        self._mixer = MixerRouting()
        self.__post_init__()

    def __post_init__(self):
        for n in self._library.keys():
            setattr(self._handler,n,self._library[n])

    @property
    def handlers(self)->dict[str:BaseHandler]:
        return self._library

    @property
    def handler(self)->HandlerRouting:

        return self._handler

    @property
    def mixer(self)->MixerRouting:
        for k,v in self._library.items():
            itm = v
            if itm is not None and k !="file":
                setattr(self._mixer,k,self._library[k].mixer)

        return self._mixer

    def create_handler(self,what:HandlerObject, fh_path:str=None)->BaseHandler:
        out = None
        if what == HandlerObject.FILE:
            # print("FFFF::: create",self._library['file'])

            if fh_path is None:
                error = f"Filehandler needs a path! "
                raise ValueError(error)
            else:
                pth = Path(fh_path)
                if not pth.exists():
                    error = f"{fh_path} is not a path! "
                    raise ValueError(error)

                fh = what.value(HandlerType.by_name(what.name))
                self._library[what.name.lower()] = fh
                out = fh
        else:
            if self._library[what.name.lower()] is None:
                hdler = what.value(HandlerType.by_name(what.name))
                self._library[what.name.lower()] = hdler
                out = hdler

            else:
                out = self._library[what.name.lower()]

        return out

