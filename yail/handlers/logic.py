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
    _htype:HandlerType = None
    _formatter:Formatter = None
    _paths:dict = field(init=False,default_factory=dict)
    _muted_channels:list = field(init=False,default_factory=dict)

    def __post_init__(self):
        pass

    @property
    def muted_channels(self)->list[LoggerLevel]:
        return self._muted_channels


    def mute_channels(self,ch:LoggerLevel|list[LoggerLevel])->list[LoggerLevel]:
        """
        Mutes the given log channels

        PARAMETER:
           - ch(LoggerLevel | list[LoggerLevel)

        RETURNS:
           - mutedchannels(list[Loggerlevel[)
        """

        wrk_list = [ch]
        if isinstance(ch,list):
            wrk_list = ch
        for lgl in wrk_list:
            if lgl not in self._muted_channels:
                self._muted_channels.append(lgl)

        return self.muted_channels

    def unmute_channels(self,ch:LoggerLevel|list[LoggerLevel])->list[LoggerLevel]:
        """
        Mutes the given log channels

        PARAMETER:
           - ch(LoggerLevel | list[LoggerLevel)

        RETURNS:
           - mutedchannels(list[Loggerlevel[)
        """

        wrk_list = [ch]
        if isinstance(ch,list):
            wrk_list = ch
        for lgl in wrk_list:
            if lgl not in self._muted_channels:
                self._muted_channels.remove(lgl)

        return self.muted_channels

    def process_loggermsg(self:LoggerMessage)->None:
        """
        Has to be implemented by kids
        """
        pass



