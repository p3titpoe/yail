from enum import Enum
from dataclasses import dataclass,field
from yail.logic import LoggerLevel,LoggerMessage
from yail.formatter.formatter import Formatter


class HandlerType(Enum):
    CONSOLE = 10
    FILE = 20
    SOCKET = 30
    WEB = 40


@dataclass
class BaseHandler:
    _htype:HandlerType
    _formatter:Formatter
    _paths:dict = field(init=False,default_factory=dict)
    _muted_channels:list = field(init=False,default_factory=dict)

    def __post_init__(self):
        pass

    @property
    def muted_channels(self)->list[str]:
        return self._muted_channels



    def process_loggermsg(self:LoggerMessage)->None:




