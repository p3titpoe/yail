from .logic import *
from .logger import BaseLogger
from yail.handlers import BaseHandler



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
    _root_cache:MasterRegistry
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
        self._root_cache = MasterRegistry(200, self)

    def _getlogger_for_sys(self, name:str)->BaseLogger:
        cl: LoggerStack = self.rootcache.cache_entry_by_name(name)
        return cl.logger

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
        print(loggerlist)

        for log in loggerlist:
            logger:BaseLogger = self._getlogger_for_sys(log)
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

                print("LOGBOOL ::", logbool)

    @property
    def rootcache(self)->MasterRegistry:
        return self._root_cache

    @property
    def rootlogger(self)->MasterRegistry:
        return self._root_logger

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
                        handlers:list[BaseHandler]=None)->BaseLogger:
        """
            Returns a new logger with given name and stores it in the registry

            The new logger inherits the Threshhold level from the __root__ logger

            PARAMETER:
                name(str)
                loglevel(LoggerLevel)

            RETURNS:
                Baselogger
        """
        stack = LoggerStack()
        loglvl = self._master_loglevel
        if isinstance(loglevel,LoggerLevel):
            loglvl = loglevel
        if handlers is None:
            handlers = []
        new_logger = BaseLogger(name,stack,loglvl,block_loglevel=block_level)
        self._root_cache.register(new_logger)
        return new_logger

    def shutdown(self)->None:
        """
            .. warning::
                Needs to be implemented

        """
        self._root_logger.info("YAIL is shuting down!")
        pass