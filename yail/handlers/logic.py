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
               f"parent = ovj, is_muted = {self.is_muted}, "
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
        # if self._muted:
        #     self.parent._muted_channels.remove(self.channel)
        # else:
        #     self.parent._muted_channels.append(self.channel)

        self._muted = nxt_state
        return nxt_state

    def color(self)->dict:
        return self._colored_sett

class ChannelRouting:
    debug:HandlerChannel = None
    info:HandlerChannel = None
    warning:HandlerChannel = None
    error:HandlerChannel = None
    critical:HandlerChannel = None


@dataclass
class HandlerChannelMixer:
    _channels:dict[str:HandlerChannel] = field(init=False,default_factory=dict)
    _channels_convenience:ChannelRouting = None
    _muted_channels:list[LoggerLevel] = field(init=False,default_factory=list)
    _snapshot:list = field(init=False,default_factory=list)
    _is_muted:bool = False
    _is_soloed:bool = False

    def __post_init__(self):
        self._channels = {lvl.name.lower():HandlerChannel(self,lvl) for lvl in LoggerLevel}
        self._channels_convenience = ChannelRouting()
        self._muted_channels = []
        for k,v in self._channels.items():
            setattr(self._channels_convenience,k,v)

    def _mk_worklist(self,ch: str | LoggerLevel | list[LoggerLevel] | None)->list[LoggerLevel]:
        wrk_lst = [ch]
        if isinstance(ch, list):
            wrk_lst = ch
        if isinstance(ch, str):
            lvl = LoggerLevel.by_name(ch.upper())
            wrk_lst = [lvl]
        return wrk_lst

    @property
    def channels(self)->dict[str:HandlerChannel]:
        return self._channels

    @property
    def channel(self)->ChannelRouting:
        return self._channels_convenience

    @property
    def muted_channels(self):
        return self._muted_channels

    def solo_channels(self, ch: str | LoggerLevel | list[LoggerLevel] | None = None) -> None:
        wrk_lst = self._mk_worklist(ch)


        if not self._is_soloed:
            # print(wrk_lst,1)
            self._snapshot = self._muted_channels
            self._muted_channels = [lv for lv in LoggerLevel if lv not in wrk_lst]
            self._is_soloed = True

        elif self._is_soloed:
            # print(wrk_lst, 0,2)
            tmp = []
            if wrk_lst[0] is None:
                self._muted_channels = self._snapshot
                self._snapshot = []
                self._is_soloed = False

            else:
                solod = [l for l in LoggerLevel if l not in self._muted_channels]

                if set(wrk_lst).isdisjoint(solod):
                    solod.extend(wrk_lst)
                    solod = set(solod)
                    self._muted_channels = [lv for lv in LoggerLevel if lv not in solod ]

                elif not set(wrk_lst).isdisjoint(solod):
                    # print(wrk_lst)
                    self._muted_channels.extend(wrk_lst)
                    tmp = set(self._muted_channels)
                    # print(tmp)
                    self._muted_channels = [lv for lv in tmp]

        for lvl, channel in self._channels.items():
            mute = False
            olmute = channel.is_muted
            if LoggerLevel.by_name(lvl.upper()) in self._muted_channels:
                mute = True
            if channel.is_muted != mute:
                channel.mute()
                print(channel.channel,channel.is_muted,olmute)

    def mute_channels(self, ch: LoggerLevel | list[LoggerLevel] | None = None) -> None:
        wrk_lst = self._mk_worklist(ch)
        cyc = 0
        to_mute = False
        if not self._is_muted:
            self._snapshot = self._muted_channels
            self._muted_channels = [lv for lv in wrk_lst]
            # self._is_muted = True
            to_mute = True


        if self._is_muted:
            if wrk_lst[0] is None:
                self._muted_channels = self._snapshot
                self._snapshot = []
                self._is_muted = False
            else:
                if set(wrk_lst).isdisjoint(self._muted_channels):
                    self._muted_channels.extend(wrk_lst)
                    setted = set(self._muted_channels)
                    self._muted_channels = [lv for lv in LoggerLevel if lv in setted ]
                else:
                    tmp = [lv for  lv in self._muted_channels if lv not in wrk_lst]
                    self._muted_channels = tmp
        if to_mute:
            self._is_muted = True
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
    _mixer:HandlerChannelMixer = None


    def __init__(self,htype:HandlerType):
        self._htype  = htype
        self._formatter = FormatterType.by_name(self._htype.name).value(self._htype)
        self._mixer = HandlerChannelMixer()
        self._paths = {}
        self._snapshot = []
        self._muted_channels = []
        self._muted_loggers = []
        self.__post_init__()

    def __post_init__(self):

        pass

    @property
    def channels(self)->dict[str:HandlerChannel]:
        return self._mixer.channels

    @property
    def channel(self)->ChannelRouting:
        return self._mixer.channel

    @property
    def mixer(self)->HandlerChannelMixer:
        return self._mixer

    @property
    def muted_channels(self)->list[LoggerLevel]:
        return self._mixer.muted_channels

    @property
    def fmt(self)->BaseFormatter:
        return self._formatter

    def can_pass(self,lvl:LoggerLevel)->bool:
        out = True
        if lvl in self.mixer.muted_channels:
            out = False
        return out

    def process_loggermsg(self, msg_obj:LoggerMessage)->None:
        """
        Has to be implemented by kids
        """

        pass



