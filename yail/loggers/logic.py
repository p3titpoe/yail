from dataclasses import dataclass,field
from yail.logic import LoggerLevel, Registry

@dataclass
class LoggerMessage:
    """
        Dataclass representing a LoggerMessage
    """
    logger_name: str
    log_level: LoggerLevel
    msg: str
    frame:any
    data:any

@dataclass
class LoggerStack:
    """
        The data stored by MasterLoggerCache
    """
    logger: object = None
    public:bool = False
    name: str = ""
    log_level: LoggerLevel = LoggerLevel.DEBUG
    handlers:list = None

    def __post_init__(self):
        self.handlers = []

    def process(self,msg:LoggerMessage):
        for h in self.handlers:
            h.process(msg)


@dataclass
class MasterRegistry(Registry):
    """
        Extends LoggerCache with managing functions for several loggercach's.

        .. warning::
            Overides the parent register function

        PARAMETERS:
            - None

        RETURNS:
            - None

    """
    _logger_by_names: dict =field(init=False,default_factory=dict)

    @property
    def logger_by_name(self)->list[str]:
        """
            Returns a list of loggernames.

            PARAMETERS:
                - None

            RETURNS:
                - list[str]

        """

        return [x for x in self._logger_by_names.keys()]

    # def register(self, logger,public:bool):
    #     """
    #         Register a cache item.
    #
    #         .. warning::
    #             Overides the parent register function
    #
    #         PARAMETERS:
    #             - logger(Loggercache)
    #
    #         RETURNS:
    #             - None
    #
    #     """
    #     reg_id = None
    #     cacheline = LoggerStack(logger, public)
    #     if len(self.booked) + 1 <= self.max_len:
    #         reg_id = self.free[0]
    #         self._registry[reg_id] = cacheline
    #         self._make_lists()
    #
    #     return reg_id


    def hook_on_makelists(self)->str:
        self._logger_by_names = {v.name:k for k,v in self.registry.items() if v is not None}


    def cache_entry(self, reg_id:int)->LoggerStack:
        """
            Returns a cache entry by id.

            .. warning::
                Overrides the parent register function

            PARAMETERS:
                - reg_id(int)

            RETURNS:
                - LoggerCacheline

        """
        return self.registry[reg_id]

    def cache_entry_by_name(self,name:str)->LoggerStack:
        """
            Returns a cache entry by name.

            PARAMETERS:
                - name(str)

            RETURNS:
                - LoggerCacheline

        """
        if name in self._logger_by_names:
            return self.cache_entry(self._logger_by_names[name])