import inspect
from datetime import datetime
from dataclasses import dataclass,field
from .logic import *
from .formatter.formatter import Formatter



class BaseLogger:
    """
        Base interactive cached Logger class

        Needs LoggerCache & Formatter, Parent should be a loggermanager
        #
        Exposes log functions for the different levels
    """
    parent: any
    log_level: LoggerLevel
    _name:str
    _cache: LoggerCache
    _formatter: Formatter
    _mute_console: bool = False
    _mute_all: bool = False
    _solo: bool = False


    def __init__(self,name:str, parent:any, log_level):
        self.log_level = log_level
        self._name = name
        self.parent = parent
        self._cache = LoggerCache(30,self)
        self._formatter = Formatter(self._name)

    def __base_log_functions(self, loglevel:LoggerLevel,frame:any ,info:str, data:any, external_frame:any = None):
        """
            Backend for all logging functions, eg info(), debug ()

            PARAMETERS:
                - loglevel: LoggerLevel
                - formatter: LoggerFormatter
            RETURN:
                - None
        """
        module_name = __name__
        act_fram = frame

        if external_frame is not None:
            act_fram = external_frame

        msg = self.formatter.compile(msg=info,frame=act_fram,loglevel=loglevel,data=data)
        # msg = f'{module_name}.{qual_name}'
        # print(msg)
        msg_obj = LoggerMessage(self.loggername, loglevel, msg)
        self.__base_output_function(msg_obj)

    def __base_output_function(self,data:LoggerMessage)->None:
        if not self.mute_all:
            self.cache.register(data)
            if data.log_level.value >= self.log_level.value:
                if not self.console:
                    print(data.msg)


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
    def cache(self)->LoggerCache:
        return self._cache

    @property
    def loggername(self) -> str:
        return self._name

    @property
    def formatter(self)->Formatter:
        return self._formatter

    def set_loglevel(self,loglevel:LoggerLevel)->None:
        self.log_level = loglevel

    def toggle_solo(self)->bool:
        "Switch Solo state"
        tog = False
        if not self.solo:
            tog = True
        self._solo = tog
        return tog

    def toggle_mute_all(self)->bool:
        "Switch processing state"

        tog = False
        if not self._mute_all:
            tog = True
        self._mute_all = tog
        return tog

    def toggle_console(self)->bool:
        "Switch console log state"

        tog = False
        if not self.console:
            tog = True
        self._mute_console = tog
        return tog

    def toggle_data(self)->None:
        "Switch data log state"
        res = self.formatter.toggle_data()
        self.warning(f"Data Logging is {res}!")

    def toggle_short(self)->None:
        "Switch between short and long format"
        self.formatter.toggle_short_format()
        self.warning("Short format is Off!")

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
        Überclass managing the loggers

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
    _root_cache:MasterLoggerCache
    _root_logger: BaseLogger
    _application_name:str = "yail"
    _master_loglevel:LoggerLevel = LoggerLevel.INFO
    _solo_on: bool = False
    _solo_list:list = field(init=False,default_factory=list)
    _mute_on:bool = False
    _muted_list: list = field(init=False,default_factory=list)
    def __init__(self):
        name = '|-RooT-|'
        parent = None
        log_level = LoggerLevel.DEBUG
        self._root_logger = BaseLogger(name,self,log_level)
        self._root_cache = MasterLoggerCache(200,self)

    def _logger_actions(self,loggerlist:list,action:str)->None:
        """
            Backend functions for most of the following functions.

            Takes a list of logger names and performs the given action
            viable actions are:

            - "mute mute_all"
            - "unmute mute_all"
            - "mute console"
            - "unmute console"
            - "unmute data"
            - "mute data"

            PARAMETER:
                loggerlist(list)
                action(str)
        """

        actions_list:list=["mute mute_all",
                           "unmute mute_all",
                           "mute console",
                           "unmute console",
                           "unmute data",
                           "mute data",
                           ]
        for log in loggerlist:
            logger:BaseLogger = self.get_logger_by_name(log)
            do,what = action.split(" ")
            if action in actions_list:
                logbool = getattr(logger,what)
                if do == "mute":
                    if not logbool:
                        logfunc = getattr(logger,f"toggle_{what}")
                        logfunc()
                if do == "unmute":
                    if logbool:
                        logfunc = getattr(logger,f"toggle_{what}")
                        logfunc()

    def mute_all_or_sip(self,sip:str = None)->None:
        """
            Mutes all Loggers.
            If a loggername is given in sip, it acts as SOLO IN PLACE.

            Solo in Place overrides every solo,meainig it's destructive where as the normal soolo functio is additive.

            PARAMETER:
                name(str|None)
        """
        loggerlist = self.rootcache.logger_by_name
        self._mute_on = True
        self._solo_on = False
        self._muted_list = loggerlist
        self._solo_list = []

        if sip is not None:
            loggerlist.remove(sip)
            self._mute_on = False
            self._solo_on = True
            self._muted_list = []
            self._solo_list = [sip]

        self._logger_actions(loggerlist,"mute console")


    def solo_logger(self,name:str)->None:
        """
            Solo's the logger.

            When first invoked, it sip's(solo in place) the loggers,
            then adds every solo'd logger to the solo bus

            .. info::
               Only affects the console output!

            PARAMETER:
                name(str)
        """
        if not self._solo_on:
            self.mute_all_or_sip()
            self._solo_on = True
        else:
            self._logger_actions([name],"umute console")
        self._solo_list.append(name)

    def solo_off(self,name:str = None)->None:
        """
            Offs the Solo Bus or takes a Logger out of the bus

            .. info::
               Only affects the console output!

            PARAMETER:
                name(str|None)
        """
        if name is None:
            self._solo_on = False
            loggerlist = [x for x in self.rootcache.logger_by_name if x not in self._solo_list]
            self._solo_list = []
            self._logger_actions(loggerlist, "unmute console")
        else:
            self._logger_actions([name],"mute console")
            self._solo_list.remove(name)

    def mute_logger(self,logger:str)->None:
        """ Mutes the logger, is additive

            .. info::
               Only affects the console output!

            PARAMETER:
                name(str)
        """

        self._mute_on = True
        self._logger_actions(logger,"mute console")
        self._muted_list.append(logger)

    def mute_off(self, name: str = None) -> None:
        """
            Offs the Mute Bus or takes a Logger out of the bus

            .. info::
               Only affects the console output!

            PARAMETER:
                name(str|None)
        """
        if name is None:
            self._mute_on = False
            # loggerlist =  [x for x in self.rootcache.logger_by_name if x not in self._muted_list]
            self.solo_off()
            self._muted_list = []
        else:
            self._logger_actions([name], "unmute console")
            self._muted_list.remove(name)

    def stop_processing_all(self)->None:
        """
            Stops ALL logging

            .. warning::
               THIS STOPS ALL LOGGING!
               Nothing will be written to the handlers

        """
        loggerlist=[x for x in self.rootcache.logger_by_name ]
        self._logger_actions(loggerlist, "mute mute_all")

    def stop_processing(self,name:str)->None:
        """
            Stops logging for a given logger

            .. warning::
               THIS STOPS ALL LOGGING!
               Nothing will be written to the handlers

            PARAMETER:
                name(str)
        """

        self._logger_actions([name], "mute mute_all")

    def resume_processing(self,name:str = None)->None:
        """
            Resumes ALL or logger specific logging

            .. warning::
               THIS STOPS ALL LOGGING!
               Nothinfg will be written to the handlers

            PARAMETER:
                name(str)
        """

        if name is None:
            loggerlist = [x for x in self.rootcache.logger_by_name]
            self._logger_actions(loggerlist,"unmute mute_all")
        else:
            self._logger_actions([name],"unmute mute_all")

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


    @property
    def rootcache(self)->MasterLoggerCache:
        return self._root_cache

    @property
    def rootlogger(self)->MasterLoggerCache:
        return self._root_logger


    def get_logger_by_name(self,name:str)->BaseLogger:
        """
            Returns logger by name

            PARAMETER:
                name(str)

            RETURNS:
                Baselogger
        """
        cl:LoggerCacheline = self.rootcache.cache_entry_by_name(name)
        lg:BaseLogger = cl.logger
        return lg


    def make_new_logger(self,name:str)->BaseLogger:
        """
            Returns a new logger with given name and stores it in the registry

            The new logger inherits the Threshhold level from the __root__ logger

            PARAMETER:
                name(str)

            RETURNS:
                Baselogger
        """
        new_logger = BaseLogger(name,self._root_logger,self._master_loglevel)
        new_logger.cache.parent_cache = self._root_cache
        self._root_cache.register(new_logger)
        return new_logger

    def shutdown(self)->None:
        """
            .. warning::
                Needs to be implemented

        """
        self._root_logger.info("YAIL is shuting down!")
        pass