from dataclasses import dataclass,field
from .logic import MixerRouting,Enum,HandlerType
from .handlers_obj import OutputHandler,ConsoleHandler,FileHandler
from pathlib import Path

class HandlerObject(Enum):
    CONSOLE = ConsoleHandler
    FILE = FileHandler


    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att

class HandlerRouting:
    console:ConsoleHandler
    file:OutputHandler

    def __init__(self)->None:
        self.console = None
        self.file = None

class HandlerManager:

    _library: dict[str:OutputHandler] = None
    _handler:HandlerRouting = None
    _mixer:MixerRouting = None

    def __init__(self):
        self._library ={}
        self._create_handler(HandlerObject.CONSOLE)
        self._handler = HandlerRouting()
        self._mixer = MixerRouting()
        self._not_processing:list[str] =[]
        self.__post_init__()

    def __post_init__(self):
        for n in self._library.keys():
            setattr(self._handler,n,self._library[n])

    def _create_handler(self, what:str|HandlerObject, fh_path:str=None)->OutputHandler:
        out = None
        if isinstance(what,str):
            what = HandlerObject.by_name(what.upper())
        args = [HandlerType.by_name(what.name)]

        if what == HandlerObject.FILE:
            if not Path(fh_path).is_dir():
                error = f'{fh_path} is not a directory'
                raise ValueError(error)
            args.append(Path(fh_path))

        if what.name.lower() not in self._library:
            hdler = what.value(*args)
            self._library[what.name.lower()] = hdler
            out = hdler

        else:
            out = self._library[what.name.lower()]

        return out

    @property
    def handlers(self)-> dict[str:OutputHandler]:
        return self._library

    @property
    def handler(self)->HandlerRouting:
        self._handler.console = self._library['console']
        self._handler.file = self._library['file']
        return self._handler

    @property
    def mixer(self)->MixerRouting:
        for k,v in self._library.items():
            itm = v
            if itm is not None:
                setattr(self._mixer,k,self._library[k].mixer)

        return self._mixer

    def processing(self,handler:str|None= None)->None:
        """Switches processing off / on for given handler"""

        if handler is None:
            self._not_processing = []

        if handler not in self._not_processing:
            self._not_processing.append(handler)
            self.handlers[handler]._is_processing = False

        elif handler in self._not_processing:
            self._not_processing.remove(handler)


