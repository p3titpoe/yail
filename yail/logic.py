from enum import Enum
from dataclasses import dataclass,field

class LoggerLevel(Enum):
    """
        Lists all the default logger types
    """
    INHERIT = 0
    DEBUG =10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


@dataclass
class LoggerMessage:
    """
        Dataclass representing a
    """
    sender: str
    log_level: LoggerLevel
    msg: str

@dataclass(repr=False)
class BaseData:
    """
        Basic obj class derived from dataclass

        Uses a custom __repr__ method. \n
        Built in serialization of the attributes, sorts out protected (__) and shows private(_) as normal attribute\n
        Can be initialized with a key-value dictionary for data-representation. Keys will be set as attribute for
        . accessing style.\n
        Built in save method for convenience

        PARAMETERS:
            - None

        RETURNS:
            - BaseData object

    """
    def __repr__(self):
        data = self.keypairs
        out = f'{self.__class__.__name__} ('
        for k, v in data.items():
            out += f'{k} = {v}, '
        out = out[:-2]
        out += f')'
        return out

    def _keypairs(self,show_private: bool = True) -> dict:
        """
            Creates a dict based on the inner .__dict__ by filtering out protected(__) attributes.

            Private attributes will be printed without capitalized (Default)
            Call __keypairs(show_private=False) to omit the private fields

            PARAMETERS:
                - show_private: Bool = if private fields should be shown.

            RETURNS:
                - dict = output of _keypairs
        """
        own_fields: dict = self.__dict__
        outd = {}
        for k, v in own_fields.items():
            f_name = k
            if k.find("__") == 0:
                pass
            else:
                if k.find("_") == 0 and show_private:
                    spl = k.split("_")
                    f_name = spl[-1]
                outd[f_name] = v
        return outd

    @property
    def keypairs(self ) -> dict:
        """
            sorts out protected (__) and shows private(_) as normal attribute from members

            PARAMETERS:
                 -None

            RETURNS:
                - dict = name:values of fields
        """
        return self._keypairs()

    def init_from_db(self, db_res: dict) -> None:
        """
            Initialize from a dictionnary
            Practical for on the fly datamodel creation or extension of attributes

            PARAMETERS:
                - db_res: dictionary - Dict with datamodel

            RETURNS:
                - None

        """
        for k, v in db_res.items():
            setattr(self, k, v)

    def save(self)->dict:
        """
            Convenience method for _keypairs

            .. warning::
                !!Might change in future!!

            PARAMETERS:
                - None

            RETURNS:
                - dict = _keypairs output

        """
        return self._keypairs()

@dataclass(repr=False)
class Registry:
    """
        Creates a dictionnary with register from 0 to  given max_len and
        manages the data inside these registers.
        \n
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
    _registry: dict[int:tuple] = field(init=False, default_factory=dict)
    _booked: list[int] = field(init=False, default_factory=list)
    _free: list[int] = field(init=False, default_factory=list)
    #: Length of the register, eg how many rooms
    max_len: int = field(default=70)
    _cache: object | None = None


    def __repr__(self)->str:
        text = "Registry:"
        nones = 0
        for k,el in self.registry.items():
            if el is not None:
                text += f'{k}  --> {el} \n'
            else:
                nones += 1
        text += f'and {nones} empty'
        return text
    def __post_init__(self) -> None:
        # Create the Registry
        self._registry = {nr: None for nr in range(0, self.max_len)}
        self._make_lists()


    def reset_cache(self) -> bool:
        """
            Resets the _registry

            PARAMETERS:
                - None

            RETURNS:
                - None
        """
        out = False
        new_cache = {i: None for i in range(0, self.max_len)}
        self._registry = new_cache
        self._make_lists()
        out = True
        return out


    def _make_lists(self) -> None:
        """
            Creates the _free and booked list
            Add a hook for childs to clamp on the listgenerations

            PARAMETERS:
                - None

            RETURNS:
                - None
        """
        self._booked = [k for k, v in self._registry.items() if v is not None]
        self._free = [k for k, v in self._registry.items() if v is None]
        self.hook_on_makelists()

    def hook_on_makelists(self)->any:
        """
        .. attention::
                Should be defined by childs

        """

    @property
    def booked(self) -> list[int]:
        """Booked registers (ro)"""
        return self._booked


    @property
    def free(self) -> list[int]:
        """Free registers (ro)"""
        return self._free


    @property
    def registry(self) -> dict:
        """Access to the registry (ro)"""
        return self._registry


    def register(self, element:any) -> int:
        """
            Register a cache item.

            .. warning::
                Overides the parent register function

            PARAMETERS:
                - None

            RETURNS:
                - None

        """
        reg_id = None
        if len(self.booked) + 1 <= self.max_len:
            reg_id = self.free[0]
            self._registry[reg_id] = element
            self._make_lists()

        return reg_id




@dataclass(repr=False)
class LoggerCache(Registry):
    """
        A resizable Registry holding the last nn messages from a logger.

        Flushes automatically to ?parent? on the next entry if reached the full capacity.
        eg if len max is 10, will flush on 11.th msg coming in

        .. note::
            This mechanism has to be refined
    """
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
        reg_id = None
        if len(self.booked) + 1 <= self.max_len:
            reg_id = self.free[0]
            self._registry[reg_id] = log_msg
            self._make_lists()

        return reg_id
    def cache_entry(self,reg_id:int)->LoggerMessage:
        """
            Returns a caxhe  item

            PARAMETERS:
                - None

            RETURNS:
                - None
        """
        return self.registry[reg_id]

    def flush(self,to_screen:bool = False)->list:
        """
            Collects & returns
        :return:
        """
        outlist = [v for k,v in self.registry.items()]
        self.reset_cache()
        return outlist

    def resize(self,new_size:int)->list:
        """
            Changes the size of the registry.
            If registry is shrunk, elements will be flushed

            PARAMETERS:
                - new_Size: int = new size of the cache

            RETUNS:
                - list = containing flushed items.(if any)

        """
        out = []
        if new_size > self.max_len:
            diff = new_size - self.max_len
            for i in range(self.max_len, new_size):
                self.registry[i] = None


        elif new_size < self.max_len:
            self.max_len = new_size
            data = [v for k,v in self.registry.items()]
            self.reset_cache()
            for el in data[:new_size]:
                self.register(el)
            out = data[new_size:]

        self.max_len = new_size
        return out

    @dataclass
    class LoggerLogParameters:
        loglevel: LoggerLevel
        qual_name: str = None
        function_name:str = None
@dataclass
class LoggerCacheline:
    """
        The data stored by MasterLoggerCache
    """
    logger: object
    name: str = ""
    log_level: LoggerLevel = LoggerLevel.DEBUG
    cache: LoggerCache = None

    def __post_init__(self):
        """
        | Generates the needed information for the logic of MasterLoggerCache
        | from
        """
        self.name = self.logger._name
        self.log_level = self.logger.log_level
        self.cache = self.logger.cache

@dataclass
class MasterLoggerCache(LoggerCache):
    _logger_by_names: dict =field(init=False,default_factory=dict)

    @property
    def logger_by_name(self)->list:
        return [x for x in self._logger_by_names.keys()]

    def register(self, logger):
        reg_id = None
        cacheline = LoggerCacheline(logger)
        if len(self.booked) + 1 <= self.max_len:
            reg_id = self.free[0]
            self._registry[reg_id] = cacheline
            self._make_lists()

        return reg_id


    def hook_on_makelists(self)->str:
        self._logger_by_names = {v.name:k for k,v in self.registry.items() if v is not None}


    def cache_entry(self, reg_id)->LoggerCacheline:
        return self.registry[reg_id]

    def cache_entry_by_name(self,name:str)->LoggerCacheline:
        if name in self._logger_by_names:
            return self.cache_entry(self._logger_by_names[name])