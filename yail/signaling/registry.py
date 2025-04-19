from dataclasses import dataclass,field
from idlelib.window import registry


@dataclass
class RegistryEntry:
    _name:str

    @property
    def name(self)->str:
        return self._name


@dataclass(repr=False)
class Registry:
    """
        Creates a dictionary with register from 0 to  given max_len and
        manages the data inside these registers.
        \n
        .. tip::
            LOGICAL COMPONENTS:
                _registry :dict(rw)
                    Represents the initial registry where data is stored

                _booked: list(read-only)
                    A list holding registry id's in which data is stored (which are booked)

                _free: list(read-only)
                    A list containing empty registry id's

        PARAMETERS:
            - max_len: int = length of the registry
            - parent_cache: LoggerCache = Parent cache, normally in cachemanager

        RETURNS:
            - Registry Object


    """
    _registry: dict[int:RegistryEntry] = field(init=False, default_factory=dict)
    _booked: list[int] = field(init=False, default_factory=list)
    _free: list[int] = field(init=False, default_factory=list)
    _by_name:dict[str:int] = field(init=False,default_factory=dict)
    #: Length of the register, eg how many rooms
    _size: int = field(default=70)
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
        self._registry = {nr: None for nr in range(0, self.size)}
        self._make_lists()

    def _make_lists(self) -> None:
        """
            Creates the _free and booked list
            Add a hook for childs to clamp on the listgenerations

            PARAMETERS:
                - None

            RETURNS:
                - None
        """
        self._booked, self._free = [[],[]]
        self._by_name = {}
        for k,v in self._registry.items():
            if v is None:
                self._free.append(k)
            else:
                self._booked.append(k)
                self._by_name[v.name] = k

    @property
    def booked(self) -> list[int]:
        """Booked registers (ro)"""
        return self._booked

    @property
    def free(self) -> list[int]:
        """Free registers (ro)"""
        return self._free

    @property
    def by_name(self)->dict[str:int]:
        return  self._by_name

    @property
    def registry(self) -> dict:
        """Access to the registry (ro)"""
        return self._registry

    @property
    def size(self)->int:
        return self._size

    def reset_cache(self) -> bool:
        """
            Resets the _registry

            PARAMETERS:
                - None

            RETURNS:
                - bool
        """
        out = False
        new_cache = {i: None for i in range(0, self._size)}
        fatalities = [v for k,v in self._registry.items()]
        self._registry = new_cache
        self._make_lists()
        out = True
        self.post_cache_manips(data=fatalities)
        return out

    def resize_cache(self,to_size:int)->None:
        rng = range(0,to_size)
        new_cache = {i: None for i in rng}
        fatalities = []

        for k,v in self._registry.items():
            if k in rng:
                new_cache[k] = v
            else:
                fatalities.append(v)

        self._registry = new_cache
        self.post_cache_manips(data=fatalities)

    def entry_by_id(self,regid:int)->RegistryEntry:
        """
            Returns a cache entry by given id
        """
        return self.registry[regid]

    def entry_by_name(self,name:str) -> RegistryEntry:
        regid = self._by_name[name]
        return self.registry[regid]

    def register(self,element:RegistryEntry) -> int:
        """
            Register a cache item.

            .. warning::
                Overrides the parent register function

            PARAMETERS:
                - None

            RETURNS:
                - None

        """
        reg_id = None
        if len(self.booked) + 1 <= self._size:
            reg_id = self.free[0]
            self._registry[reg_id] = element
            self._make_lists()
            self.post_register(reg_id)
        return reg_id

    def unregister(self,regid:int)->None:
        self.registry[regid] = None
        self._make_lists()
#########################################
# HOOKS
#########################################
    def post_cache_manips(self,data:list[RegistryEntry])->None:
        """
        Hook after cache manipulation.
        Data will be a list of RegistryEntry that will be lost because of reseting or resizing.
        Here is the place if you to collect them


        """

    def post_register(self,regid:int)->any:
        """
        Post Register HooK
        Hook is called after register process, before returning ID's
        Use this method to extend the function block of the register function

        .. attention::
                Should be defined by kids

        """
@dataclass
class RegistryController:
    _reg:Registry

    @property
    def booked(self)->list[int]:
        return self.registry._booked

    @property
    def free(self)->list[int]:
        return self.registry._booked

    @property
    def registry(self)->Registry:
        return self._reg

    @property
    def registry_by_name(self)->dict:
        return self.registry.by_name
    
    def add(self, entry:RegistryEntry):
        regid = -1
        if entry.name not in self.registry_by_name:
            regid = self.registry.register(entry)
            return regid
        else:
            error = f"An entry named {entry.name} already exists"
            raise ValueError(error)

    def rm(self, entry:str)->int:
        regid = -1
        if entry in self.registry_by_name:
            regid= self.registry_by_name[entry]
            self.registry.unregister(regid)
        return regid

    def by_name(self,entryname:str)->RegistryEntry:
        return self.registry.entry_by_name(entryname)

    def by_regid(self,regid:int)->RegistryEntry:
        return self.registry.entry_by_id(regid)



    
    
    
    
    