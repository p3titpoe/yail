import inspect
from dataclasses import dataclass,field
from yail.signaling import emit,new_signal,subscribe
from .logic import LoggerLevel,LoggerMessage,MasterRegistry,LoggerStack

class BaseLogger:
    """
        Base interactive cached Logger class

        Needs LoggerCache & Formatter, Parent should be a loggermanager
        #
        Exposes log functions for the different levels
    """
    _name:str
    _log_level: LoggerLevel
    _block_loglevel:bool = False
    _mute_console: bool = False
    _mute_all: bool = False
    _solo: bool = False
    is_processing:bool = True
    is_muted:bool = False

    def __init__(self,name:str,log_level,block_loglevel:bool=False):
        self._log_level = log_level
        self._name = name
        self._block_loglevel = block_loglevel

    def __base_log_functions(self, loglevel:LoggerLevel,frame:any ,info:str, data:any, external_frame:any = None):
        """
            Backend for all logging functions, eg info(), debug ()

            PARAMETERS:
                - loglevel: LoggerLevel
                - formatter: LoggerFormatter
            RETURN:
                - None
        """
        if self.is_processing:
            act_fram = frame
            if external_frame is not None:
                act_fram = external_frame

            msg_obj = LoggerMessage(logger_name=self.name, log_level=loglevel,msg=info,frame=act_fram,data=data)

            if not self.is_muted:
                emit(f'{self.name}-stack-connection',msg_obj=msg_obj)


    @property
    def log_level(self)->LoggerLevel:
        return self._log_level

    @property
    def solo(self)->bool:
        return self._solo

    @property
    def mute_all(self)->bool:
        return self._mute_all

    @property
    def console(self)->bool:
        return self._mute_console

    @property
    def name(self) -> str:
        return self._name

    @property
    def handler(self):
        return self._handler

    def log(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with self.log_level

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = self.log_level
        # frame = external_frame
        # if frame is None:
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)

    def debug(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.DEBUG
        # frame = external_frame
        # if frame is None:
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)

    def info(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.INFO
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel, frame, info, loggger_msg_data, external_frame)

    def warning(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.WARNING
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)

    def error(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.ERROR
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)

    def critical(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.CRITICAL
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)

@dataclass(init=False)
class LoggerManager:
    """
        Überclass managing the stacks

        Needs MAsterLoggerCache as Registry (derived from Loggercache) and a Baslogger.

        .. tip::
            Baselogger will be named __root__ and will ALWAYS log, eg. is not impacted by solo, mute, process and console
            actions. It can be off'd manually like any other Baselogger

        Allowed actions
            - mute mute_all     : stop processing
            - unmute mute_all   : resume processing
            - mute console      : mute terminal output
            - unmute console    : resume terminal output
            - unmute data       : stop data processing
            - mute data         : resume data processing

    """
    _loggers:MasterRegistry
    _root_logger: BaseLogger
    _application_name:str = "stacks"
    _master_loglevel:LoggerLevel = LoggerLevel.INFO
    _is_initd:bool = False
    _is_muted:bool = False
    _is_soloed:bool = False
    _muted_list: list = field(init=False,default_factory=list)

    def __init__(self):
        log_level = LoggerLevel.DEBUG
        self._is_initd = True
        self._muted_list = [] ##
        self._loggers = MasterRegistry(50, self)
        self._root_logger:BaseLogger = self.make_new_logger(name="ROOT",loglevel=log_level,public=False,handlers=['system-com'])

    def _getlogger_for_sys(self, name:str)->BaseLogger:
        cl: LoggerStack = self.loggers.cache_entry_by_name(name)
        return cl.logger

    def _mk_worklist(self,ch: str | LoggerLevel | list[LoggerLevel] | None)->list[LoggerLevel]:
        wrk_lst = [ch]
        if isinstance(ch, list):
            wrk_lst = ch

        return wrk_lst

    @property
    def loggers(self)->MasterRegistry:
        return self._loggers

    @property
    def rootlogger(self)->BaseLogger:
        return self._root_logger

    def solo_loggers(self, ch: str | list[str] | None = None) -> None:

        wrk_lst = self._mk_worklist(ch)
        if not self._is_soloed:
            self._snapshot = self._muted_list
            self._muted_list = [lv for lv in self.loggers.logger_by_name if lv not in wrk_lst]
            self._is_soloed = True

        elif self._is_soloed:
            tmp = []
            if len(wrk_lst)==0 or wrk_lst[0] is None:
                self._muted_list = self._snapshot
                self._snapshot = []
                self._is_soloed = False

            else:
                solod = [l for l in self.loggers.logger_by_name if l not in self._muted_list]

                if set(wrk_lst).isdisjoint(solod):
                    solod.extend(wrk_lst)
                    solod = set(solod)
                    self._muted_list = [lv for lv in LoggerLevel if lv not in solod ]

                elif not set(wrk_lst).isdisjoint(solod):
                    self._muted_list.extend(wrk_lst)
                    tmp = set(self._muted_list)
                    self._muted_list = [lv for lv in tmp]

        for lvl, loggerstack in self.loggers.registry.items():
            mute = False
            if loggerstack.logger.name in self._muted_channels:
                mute = True
            if loggerstack.logger.is_muted != mute:
                loggerstack.logger.is_muted = mute

    def mute_loggers(self, ch: str | list[str] | None = None) -> None:
        wrk_lst = self._mk_worklist(ch)
        cyc = 0
        to_mute = False
        if not self._is_muted:
            self._snapshot = self._muted_list
            self._muted_list = [lv for lv in wrk_lst]
            # self._is_muted = True
            to_mute = True


        if self._is_muted:
            if wrk_lst[0] is None:
                self._muted_list = self._snapshot
                self._snapshot = []
                self._is_muted = False
            else:
                if set(wrk_lst).isdisjoint(self._muted_list):
                    self._muted_list.extend(wrk_lst)
                    setted = set(self._muted_list)
                    self._muted_list = [lv for lv in self.loggers.registry if lv in setted ]
                else:
                    tmp = [lv for  lv in self._muted_list if lv not in wrk_lst]
                    self._muted_list = tmp
        if to_mute:
            self._is_muted = True

        for lvl, loggerstack in self.loggers.registry.items():
            mute = False
            if loggerstack.logger.name in self._muted_list:
                mute = True
            if loggerstack.logger.is_muted != mute:
                loggerstack.logger.is_muted = mute

    def set_loglevel(self, loglvl:str|LoggerLevel, loggername:str=None)->None:
        """
            Sets the loglevel at a global or a per logger level

            PARAMETER:
                loglvl(str|Loggerlevel)
                loggername(str|None)

            RETURNS:
                None
        """
        if isinstance(loglvl,str):
            loglevel = LoggerLevel.by_name(loglvl.upper())
        else:
            loglevel = loglvl
        # if isinstance(loglevel,LoggerLevel):
        if loggername is None:
            self._master_loglevel = loglevel
            for x in self.rootcache.booked:
                self.rootcache.registry[x].logger.set_loglevel(loglevel)
        else:
            logger = self.rootcache.cache_entry_by_name(loggername)
            logger.log_level = loglevel

    def get_logger_by_name(self,name:str)->BaseLogger:
        """
            Returns logger by name

            PARAMETER:
                name(str)

            RETURNS:
                Baselogger
        """
        cl:LoggerStack = self.rootcache.cache_entry_by_name(name)
        if not cl.public:
            raise PermissionError(f"{cl.name} is not Public!")
        else:
            lg:BaseLogger = cl.logger
            return lg

    def make_new_logger(self,name:str, loglevel:LoggerLevel=None,
                        public:bool=False,
                        block_level:bool=False,
                        handlers:list[str]=None)->BaseLogger:
        """
            Returns a new logger with given name and stores it in the registry

            The new logger inherits the Threshhold level from the __root__ logger

            PARAMETER:
                name(str)
                loglevel(LoggerLevel)

            RETURNS:
                Baselogger
        """
        loglvl = self._master_loglevel
        if isinstance(loglevel,LoggerLevel):
            loglvl = loglevel
        if handlers is None:
            handlers = ['handler-console']
        #Create a private channel for the connection stack-logger
        new_signal(f'{name}-stack-connection',{'msg_obj':LoggerMessage})
        new_logger = BaseLogger(name=name,log_level=loglvl,block_loglevel=block_level)
        new_stack = LoggerStack(name=name,logger=new_logger,public=False,handlers=handlers)
        subscribe(f'logger-{name}',f'{name}-stack-connection',new_stack.process)
        self._loggers.register(new_stack)
        return new_logger

    def shutdown(self)->None:
        """
            .. warning::
                Needs to be implemented

        """
        self._root_logger.info("YAIL is shuting down!")
        pass
