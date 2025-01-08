from dataclasses import dataclass
from enum import Enum

@dataclass(repr=False)
class BaseData:
    """
        Basic obj class derived from dataclass

        Uses a custom __repr__ method. 

        Built in serialization of the attributes, sorts out protected (__) and shows private(_) as normal attribute

        Can be initialized with a key-value dictionary for data-representation. Keys will be set as attribute for
        . accessing style.

        Built in save method for convenience

        PARAMETERS:
            - None

        RETURNS:
            - BaseData object

    """
    @property
    def keypairs(self) -> dict:
        """
            sorts out protected (__) and shows private(_) as normal attribute from members

            PARAMETERS:
                 -None

            RETURNS:
                - dict = name:values of fields
        """
    def init_from_db(self, db_res: dict) -> None:
        """
            Initialize from a dictionnary
            Practical for on the fly datamodel creation or extension of attributes

            PARAMETERS:
                - db_res: dictionary - Dict with datamodel

            RETURNS:
                - None

        """
    def save(self) -> dict:
        """
            Convenience method for _keypairs

            .. warning::
                !!Might change in future!!

            PARAMETERS:
                - None

            RETURNS:
                - dict = _keypairs output

        """

@dataclass(repr=False)
class Registry:
    """
        Creates a dictionnary with register from 0 to  given max_len and
        manages the data inside these registers.
        

        .. tip::
            LOGICAL COMPONENTS:
                registry :dict(read-only)
                    Represents the initial registry where data is stored

                booked: list(read-only)
                    A list holding registry id's in which data is stored (which are booked)

                free: list(read-only)
                    A list containing empty registry id's

        PARAMETERS:
            - max_len: int = length of the registry
            - parent_cache: LoggerCache = Parent cache, normally in cachemanager

        RETURNS:
            - Registry Object


    """
    max_len: int = ...
    def __post_init__(self) -> None: ...
    def reset_cache(self) -> bool:
        """
            Resets the _registry

            PARAMETERS:
                - None

            RETURNS:
                - None
        """
    def hook_on_makelists(self) -> any:
        """
        .. attention::
                Should be defined by childs

        """
    @property
    def booked(self) -> list[int]:
        """Booked registers (ro)"""
    @property
    def free(self) -> list[int]:
        """Free registers (ro)"""
    @property
    def registry(self) -> dict:
        """Access to the registry (ro)"""
    def register(self, element: any) -> int:
        """
            Register a cache item.

            .. warning::
                Overides the parent register function

            PARAMETERS:
                - None

            RETURNS:
                - None

        """
    def __init__(self, max_len=..., _cache=...) -> None: ...

class LoggerLevel(Enum):
    """
        Lists all the default logger types
    """
    INHERIT = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

@dataclass
class LoggerMessage:
    sender: str
    log_level: LoggerLevel
    msg: str
    def __init__(self, sender, log_level, msg) -> None: ...

@dataclass(repr=False)
class LoggerCache(Registry):
    def register(self, log_msg: LoggerMessage) -> int:
        """
            Register a cache item.

            .. warning::
                Overides the parent register function

            PARAMETERS:
                - None

            RETURNS:
                - None

        """
    def cache_entry(self, reg_id: int) -> LoggerMessage:
        """
            Returns a caxhe  item

            PARAMETERS:
                - None

            RETURNS:
                - None
        """
    def flush(self, to_screen: bool = False) -> list:
        """
            Collects & returns
        :return:
        """
    max_len = ...
    def resize(self, new_size: int) -> list:
        """
            Changes the size of the registry.
            If registry is shrunk, elements will be flushed

            PARAMETERS:
                - new_Size: int = new size of the cache

            RETUNS:
                - list = containing flushed items.(if any)

        """
    @dataclass
    class LoggerLogParameters:
        loglevel: LoggerLevel
        qual_name: str = ...
        function_name: str = ...
        def __init__(self, loglevel, qual_name=..., function_name=...) -> None: ...
    def __init__(self, max_len=..., _cache=...) -> None: ...

@dataclass
class LoggerCacheline:
    logger: object
    name: str = ...
    log_level: LoggerLevel = ...
    cache: LoggerCache = ...
    def __post_init__(self) -> None: ...
    def __init__(self, logger, name=..., log_level=..., cache=...) -> None: ...

@dataclass
class MasterLoggerCache(LoggerCache):
    @property
    def logger_by_name(self) -> list: ...
    def register(self, logger): ...
    def hook_on_makelists(self) -> str: ...
    def cache_entry(self, reg_id) -> LoggerCacheline: ...
    def cache_entry_by_name(self, name: str) -> LoggerCacheline: ...
    def __init__(self, max_len=..., _cache=...) -> None: ...
