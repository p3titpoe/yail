from dataclasses import dataclass,field
from .logic import HandlerType,HandlerChannelMixer,ChannelRouting,HandlerChannel
from yail.loggers import LoggerLevel,LoggerMessage
from yail.formatter import FormatterStyle,BaseFormatter
from  yail.registry import RegistryController,RegistryEntry
from yail.signaling import subscribe,new_signal,emit
from pathlib import Path

@dataclass(init=False)
class OutputHandler:
    _htype:HandlerType = None
    _formatter:BaseFormatter = None
    _mixer:HandlerChannelMixer = None


    def __init__(self,htype:HandlerType):
        self._htype  = htype
        self._mixer = HandlerChannelMixer()
        self.sys_enabled:bool = True
        self._is_processing:bool = True
        self._snapshot = []
        self._muted_channels = []
        self._muted_loggers = []
        self.__post_init__()


    def __post_init__(self):
        subscribe(f'syscom-listener-{self._htype.name.lower()}','system-com',self.sys_process)
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
    def muted_loggers(self)->list[str]:
        return self._muted_loggers

    @property
    def fmt(self)->BaseFormatter:
        return self._formatter

    def mute_loggers(self,name:str|None = None):
        """Mutes / Unmutes the given Loggers
           If no loggername given, unmutes everything
         """
        if name is None:
            self._muted_loggers = []
        elif name in self._muted_loggers:
            self._muted_loggers.remove(name)
        else:
            self._muted_loggers.append(name)

    def can_pass(self,msg:LoggerMessage)->bool:
        """
            Checks if the message is ok for output

            .. note::
            Has to be calles by kids before outputting

        """
        out = True
        if msg.log_level in self.mixer.muted_channels:
            out = False
        if msg.logger_name in self._muted_loggers:
            out = False
        return out

    def process(self, msg_obj:LoggerMessage)->None:
        """
        Listener function to the handler signal
        Has to be implemented by kids
        """

        pass

    def sys_process(self,msg_obj:LoggerMessage)->None:
        """Listener function to the system signals
        Has to be implemented by kids
        """
        pass


@dataclass
class ConsoleHandler(OutputHandler):

    def __init__(self,handlertype:HandlerType):
        super().__init__(handlertype)
        self._colors:bool = False
        self._color_engine:any = None
        self._formatter = FormatterStyle.FILE_TXT.value(FormatterStyle.CONSOLE_JSON)

        subscribe('listener-console','handler-console',self.process)


    def sys_process(self,msg_obj:LoggerMessage)->None:
        """Listener function to the system signals"""
        if self.sys_enabled:
            self.process(msg_obj)

    def process(self,msg_obj:LoggerMessage) ->None:
        """Listener function to the system signals"""
        out = self._formatter.process(msg_obj)

        if self.can_pass(msg_obj):
            print(out)

class FileHandlerEntry(RegistryEntry):
    """
        RegistryEntry for the filehandler registry.

        .. note::
           In the filehandler, the Entries are responsible for writing to their file

    """
    def __init__(self,filename:str,extension:str,filepath:Path)->None:
        super().__init__(filename)
        style_name = f'FILE_{extension}'
        style = FormatterStyle.by_name(style_name)
        self._fmt:BaseFormatter = style.value(style)
        self._filepath:Path = filepath /f'{self.name}.{extension.lower()}'
        self._signalname:str = f'fmtfile-{self.name}'

        #Create a new signal for the Filehandler to emit
        #Add the process function to the as listener to the signal
        new_signal(self.signalname,{'msg_obj':LoggerMessage})
        subscribe(f'filehandler-format-{self.name}',self.signalname,self.process)

    def __repr__(self):
        txt = self.__class__.__name__+"("
        txt +=(f'path={self._filepath}, '
               f'formatter={self._fmt}')
        txt += ')'
        return txt

    @property
    def format(self)->BaseFormatter:
        return self._fmt

    @property
    def signalname(self)->str:
        return self._signalname

    def process(self, msg_obj:LoggerMessage):
        """Listener function to the system signals"""
        out = self.format.process(msg_obj=msg_obj)
        with open(self._filepath.resolve(),"a") as fileout:
            fileout.write(f'{out}\n')


@dataclass
class FileHandler(OutputHandler):
    def __init__(self,handlertype:HandlerType,log_directory:str):
        super().__init__(handlertype)

        self._reg = RegistryController(10)
        self._formatter_signals = []
        self._work_dir:Path = Path(log_directory)
        if not self._work_dir.is_dir():
            error = f"{log_directory} is not a Directory!"
            raise ValueError(error)
        subscribe('listener-file','handler-file',self.process)
        self.new_file_entry('general','TXT')


    @property
    def wkd(self)->Path:
        return self._work_dir

    def new_file_entry(self,name:str,extension:str)->FileHandlerEntry:
        """Creates a new file entry for the file handler"""
        new_file = FileHandlerEntry(name,extension,self.wkd)
        self._reg.add(new_file)
        if new_file.signalname not in self._formatter_signals:
            self._formatter_signals.append(new_file.signalname)
        return new_file

    def sys_process(self,msg_obj:LoggerMessage)->None:
        """Listener function to the system signals"""

        if self.sys_enabled:
            self.process(msg_obj)

    def process(self,msg_obj:LoggerMessage) ->None:
        """Listener function to the handler signals"""

        if self.can_pass(msg_obj):

            for fmt_signal in self._formatter_signals:
                emit(fmt_signal,msg_obj=msg_obj)



