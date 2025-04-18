from enum import Enum
from dataclasses import dataclass,field

import yail.handlers
from yail.logic import LoggerLevel,LoggerMessage
from yail.formatter import FormatterType,BaseFormatter


class HandlerType(Enum):
    CONSOLE = 10
    FILE = 20
    SOCKET = 30
    WEB = 40

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att

@dataclass
class HandlerChannel:
    parent: any
    _channel: LoggerLevel
    _colored:bool = False
    _muted:bool = False
    _colored_sett:dict = None

    def __repr__(self):
        txt = (f"HandelerChannel for {self._channel.name.lower()}( "
               f"parent = {self.parent._htype}, is_muted = {self.is_muted}, "
               f"is_colored = {self.is_colored})")
        return txt

    @property
    def channel(self)->LoggerLevel:
        return self._channel

    @property
    def  is_colored(self)->bool:
        return self._colored

    @property
    def is_muted(self)->bool:
        """
            Check if channel is muted

            PARAMETERS:
                - None
            RETURNS:
                - boo
        """
        return self._muted

    def mute(self)->bool:
        """
            Toggle to mute the channel.

            calls on parent ConsoleHandler to update the list

            PARAMETERS:
                - None
            RETURNS:
                - boo
        """
        nxt_state = False if self._muted else True
        if self._muted:
            self.parent._muted_channels.remove(self.channel)
        else:
            self.parent._muted_channels.append(self.channel)

        self._muted = nxt_state
        return nxt_state

    def color(self)->dict:
        return self._colored_sett

@dataclass
class HandlerChannelMixer:
    _channels:dict[str:HandlerChannel] = field(init=False,default_factory=dict)
    _muted_channels:list[LoggerLevel] = field(init=False,default_factory=list)
    _snapshot:list = field(init=False,default_factory=list)
    _is_muted:bool = False
    _is_soloed:bool = False

    def solo_channels(self, ch: str | LoggerLevel | list[LoggerLevel] | None = None) -> None:
        solod = False
        wrk_lst = [ch]
        if isinstance(ch, list):
            wrk_lst = ch
        if isinstance(ch,str):
            lvl = LoggerLevel.by_name(ch.upper())
            wrk_lst = [lvl]

        if not self._is_soloed:
            self._snapshot = self._muted_channels
            self._muted_channels = [lv for lv in LoggerLevel if lv not in wrk_lst]
            self._is_soloed = True

        if self._is_soloed:
            if ch is None:
                self._muted_channels = self._snapshot
                self._snapshot = []
                self._is_soloed = False
            else:
                tmp = [lv for lv in self._muted_channels if lv not in wrk_lst]
                self._muted_channels = tmp
                if len(tmp) == 0:
                    self._is_soloed = False
                    self._muted_channels = self._snapshot

        for lvl, channel in self._channels.items():
            mute = False
            if lvl in self._muted_channels:
                mute = True
            if channel.is_muted != mute:
                channel.mute()

    def mute_channels(self, ch: LoggerLevel | list[LoggerLevel] | None = None) -> None:
        wrk_lst = [ch]
        if isinstance(ch, list):
            wrk_lst = ch
        if isinstance(ch, str):
            lvl = LoggerLevel.by_name(ch.upper())
            wrk_lst = [lvl]

        if not self._is_muted:
            self.solo_channels()
            self._snapshot = self._muted_channels
            self._muted_channels = [lv for lv in wrk_lst]
            self._is_muted = True

        if self._is_muted:
            if ch is None:
                if len(self._snapshot) != 0:
                    self._is_soloed = True
                self._muted_channels = self._snapshot
                self._snapshot = []
                self._is_muted = False
            else:
                tmp = [lv for lv in self._muted_channels if lv not in wrk_lst]
                self._muted_channels = tmp
                if len(tmp) == 0:
                    self._is_soloed = False
                    self._muted_channels = self._snapshot

        for lvl, channel in self._channels.items():
            mute = False
            if lvl in self._muted_channels:
                mute = True
            if channel.is_muted != mute:
                channel.mute()

@dataclass(init=False)
class BaseHandler:
    _htype:HandlerType = None
    _formatter:BaseFormatter = None
    _channels:dict[LoggerLevel:HandlerChannel] = None
    _is_soloed:bool = False
    _is_muted:bool = False
    _paths:dict = None
    _snapshot:list = None
    _muted_channels:dir = None
    _muted_loggers:list = None

    def __init__(self,htype:HandlerType):
        self._htype  = htype
        self._formatter = FormatterType.by_name(self._htype.name).value(self._htype)
        self._channels = {lvl.name.lower():HandlerChannel(self,lvl) for lvl in LoggerLevel}
        self._paths = {}
        self._snapshot = []
        self._muted_channels = []
        self._muted_loggers = []
        self.__post_init__()

    def __post_init__(self):

        pass

    @property
    def channels(self)->dict[str:HandlerChannel]:
        return self._channels
    @property
    def muted_channels(self)->list[LoggerLevel]:
        return self._muted_channels

    @property
    def fmt(self)->BaseFormatter:
        return self._formatter

    # def _mute_a

    def mute_channels(self,ch:LoggerLevel|list[LoggerLevel])->list[LoggerLevel]:
        """
        Mutes the given log channels
        Unmutes

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
            if lgl in self._muted_channels:
                self._muted_channels.remove(lgl)

        return self.muted_channels

    def solo_channels(self,ch:LoggerLevel|list[LoggerLevel]|None = None)->None:
        solod = False
        wrk_lst = [ch]
        if isinstance(ch,list):
            wrk_lst = ch

        if not self._is_soloed:
            self._snapshot = self._muted_channels
            self._muted_channels = [lv for lv in LoggerLevel if lv not in wrk_lst]
            self._is_soloed = True

        if self._is_soloed:
            if ch is None:
                self._muted_channels = self._snapshot
                self._snapshot = []
                self._is_soloed = False
            else:
                tmp = [lv for lv in self._muted_channels if lv not in wrk_lst]
                self._muted_channels = tmp
                if len(tmp) == 0:
                    self._is_soloed = False
                    self._muted_channels = self._snapshot

        for lvl,channel in self._channels.items():
            mute = False
            if lvl in self._muted_channels:
                mute = True
            if channel.is_muted != mute:
                channel.mute()
        # print(self._channels)


    def process_loggermsg(self, msg_obj:LoggerMessage)->None:
        """
        Has to be implemented by kids
        """
        pass



