import inspect
from dataclasses import dataclass,field
from typing import Callable
from enum import Enum
from yail.signaling.registry import Registry,RegistryEntry


class InternalSystemEvent(Enum):
    pass
@dataclass
class SignalEvent(RegistryEntry):
    _sig:dict[str:type]
    docs:str = "Executor is the func being executed when the signal is called"

    @property
    def signature(self)->list:
        return self._sig


@dataclass
class SignalSubscriber(RegistryEntry):
    _receiver_func:Callable
    _subscription:SignalEvent

    def __post_init__(self):
        # jj = inspect.signature(self._receiver_func)
        pp = inspect.getfullargspec(self.lnk)
        jj = {k:v for k,v in pp.annotations.items() if k != 'return'}
        if self._subscription.signature != jj:
            error = f"Signatures do not match.\n Need: {self._subscription.signature}"
            raise AttributeError(error)

    @property
    def lnk(self)->Callable:
        return self._receiver_func

    @property
    def subscription(self)->SignalEvent:
        return

@dataclass
class SignalCache:
    """
        Needed functions:
        add_event(name:str, data:bool, docs="") Must Return SignalEvent
        del_event(eventname:str)
        subscribe(eventname:str)
    """
    _signals:Registry = field(init=False,default_factory=Registry)
    _subscribers:Registry = field(init=False,default_factory=Registry)
    _lnks:dict[SignalEvent:list] = field(init=False,default_factory=dict)


    def __post_init__(self):
        pass

    def _emit_signal(self,funclist:list[Callable],**kwargs):
        for func in funclist:
            func(**kwargs)


    @property
    def signals(self)->Registry:
        return self._signals

    @property
    def subscribers(self)->Registry:
        return self._subscribers

    @property
    def links(self)->dict[SignalEvent:list[Callable]]:
        return self._lnks

    def signals_by_name(self,name:str)->SignalEvent:
        return self.signals.entry_by_name(name=name)

    def subscribe(self,subscriber_name:str,signal_name:str,):
        pass

    def create_signal(self, signalname:str,signature:dict[str:type],docs:str="Say somtehing")->SignalEvent:
        new_signal = SignalEvent(signalname,signature,docs)
        if signalname in self.signals.by_name:
            error = f"A signal named {new_signal.name} already exists"
            raise ValueError(error)

        else:
            self.add_signal(new_signal)
            return new_signal

    def add_signal(self,signal:SignalEvent)->int:
        regid = -1
        if signal.name not in self.signals.by_name:
            regid = self.signals.register(signal)
            return regid
        else:
            error = f"A signal named {signal.name} already exists"
            raise ValueError(error)

    def rm_signal(self,signalname:str)->int:
        regid = -1
        if signalname in self.signals.by_name:
            regid= self.signals.by_name[signalname]
            self.signals.unregister(regid)
        return regid

def hh(data:int,name:str)->list:
    return [data,name]

def ggh(data:int,name:str)->int:
    print('Received signal')
    return data*3

cache = SignalCache()
kk = SignalEvent('NEwSig',{'data': int,'name': str})
print(kk)
cache.add_signal(kk)
gg = cache.create_signal('NmwSig',{'data': int,'name': str})
cache.create_signal('Ng',{'data': int,'name': str})
print(cache.signals.booked)
cache.rm_signal('NmwSig')
print(cache.signals.booked,cache.signals.registry)
cache.add_signal(gg)
print(cache.signals.booked,cache.signals.registry)

# cache.add_signal(gg)
# ss = SignalSubscriber('subs',ggh,kk)
# print(ss)
