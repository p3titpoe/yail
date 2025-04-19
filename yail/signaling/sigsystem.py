import inspect
from dataclasses import dataclass,field
from typing import Callable
from enum import Enum
from venv import create

from yail.signaling.registry import RegistryController,RegistryEntry


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
    _signals:RegistryController = field(init=False,default_factory=RegistryController)
    _subscribers:RegistryController = field(init=False,default_factory=RegistryController)
    _lnks:dict[SignalEvent:list[str]] = field(init=False,default_factory=dict)


    def __post_init__(self):
        self._signals.parent = self
        self._subscribers.parent = self
        pass

    def __cleanup(self,who)->None:
        if isinstance(who,SignalEvent):
            for k in self.subscriber.registry_by_name:
                sub:SignalSubscriber = self.subscriber.by_name(k)
                if sub.subscription == who:
                    sub._subscription = None
            delattr(self.links[who.name])

        if isinstance(who,SignalSubscriber):
            sig:SignalEvent = who.subscription
            self.links[sig.name].remove(who.name)

    def _emit_signal(self,funclist:list[Callable],**kwargs):
        for func in funclist:
            func(**kwargs)


    @property
    def signal(self)->RegistryController:
        return self._signals

    @property
    def subscriber(self)->RegistryController:
        return self._subscribers

    @property
    def links(self)->dict[SignalEvent:list[Callable]]:
        return self._lnks

    def unsubscribe(self,subscriber_name:str)->None:
        if subscriber_name in self.subscriber.registry_by_name:
            sub:SignalSubscriber = self.subscriber.by_name(subscriber_name)
            if sub.subscription.name in self.links:
                self.links[sub.subscription.name].remove(subscriber_name)
            self.subscriber.rm(subscriber_name)

    def subscribe(self,subscriber_name:str,signal_name:str,receiver_func:Callable)->None:
        sig = self.signal.by_name(signal_name)
        new_subscriber = SignalSubscriber(subscriber_name,receiver_func,sig)
        self.subscriber.add(new_subscriber)
        print(self.subscriber)
        self.links[sig.name].append(new_subscriber.lnk)

    def create_signal(self, signalname:str,signature:dict[str:type],docs:str="Say somtehing")->SignalEvent:
        new_signal = SignalEvent(signalname,signature,docs)
        if signalname in self.signal.registry_by_name:
            error = f"A signal named {new_signal.name} already exists"
            raise ValueError(error)

        else:
            self.signal.add(new_signal)
            self.links[new_signal.name] = []
            return new_signal



def hh(data:int,name:str)->list:
    return [data,name]

def ggh(data:int,name:str)->int:
    print('Received signal')
    return data*3

cache = SignalCache()
kk = SignalEvent('NEwSig',{'data': int,'name': str})
print(kk)
cache.signal.add(kk)
gg = cache.create_signal('NmwSig',{'data': int,'name': str})
cache.subscribe('kkkkk','NmwSig',ggh)
ss = SignalSubscriber('name',hh,gg)
cache.subscriber.add(ss)
print("Subscriber ",cache.subscriber.booked," Signals ",cache.signal.booked)

cache.create_signal('Ng',{'data': int,'name': str})
print("Subscriber ",cache.subscriber.booked," Signals ",cache.signal.booked)
cache.signal.rm('NmwSig')
print("Subscriber ",cache.subscriber.booked," Signals ",cache.signal.booked)
cache.signal.add(gg)
print("Subscriber ",cache.subscriber.booked," Signals ",cache.signal.booked)
print(cache)
# cache.add_signal(gg)
# print(ss)
