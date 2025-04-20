import inspect
from dataclasses import dataclass,field
from typing import Callable
from enum import Enum
from .registry import RegistryController,RegistryEntry


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
            error = f"Signature of '{str(self.lnk.__name__)}:{jj}' does not match! Need: {self._subscription.signature}"
            raise AssertionError(error)

    @property
    def lnk(self)->Callable:
        return self._receiver_func

    @property
    def subscription(self)->SignalEvent:
        return

    def new_subscription(self,sig:SignalEvent)->None:
        self._subscription = sig


cnt = 0
def cunt(msg:str =""):
    global cnt
    cnt += 1
    print(cnt, msg)

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


    def _on_delete(self,who)->None:
        if isinstance(who,SignalEvent):

            for k in self.links[who.name]:
                regid = self.subscriber.registry_by_name[k]
                self.subscriber.registry.unregister(regid)
            del self.links[who.name]

        if isinstance(who,SignalSubscriber):
            sig:SignalEvent = who._subscription
            self.links[sig.name].remove(who.name)

    def _on_add(self,who)->None:
        if isinstance(who, SignalEvent):
            self.links[who.name] = []

        if isinstance(who, SignalSubscriber):
            sig: SignalEvent = who._subscription
            self.links[sig.name].append(who.name)



    @property
    def signal(self)->RegistryController:
        return self._signals

    @property
    def subscriber(self)->RegistryController:
        return self._subscribers

    @property
    def links(self)->dict[SignalEvent:list[Callable]]:
        return self._lnks


    def subscribe(self,subscriber_name:str,signal_name:str,receiver_func:Callable)->SignalSubscriber:
        # cunt(f"subscribe: {subscriber_name}")
        sig = self.signal.by_name(signal_name)
        new_subscriber = SignalSubscriber(subscriber_name,receiver_func,sig)
        self.subscriber.add(new_subscriber)
        return new_subscriber

    def unsubscribe(self,subscriber_name:str)->None:
        if subscriber_name in self.subscriber.registry_by_name:
            sub:SignalSubscriber = self.subscriber.by_name(subscriber_name)
            self.subscriber.rm(subscriber_name)

    def create_signal(self, signalname:str,signature:dict[str:type],docs:str="Say somtehing")->SignalEvent:
        new_signal = SignalEvent(signalname,signature,docs)
        if signalname in self.signal.registry_by_name:
            error = f"A signal named {new_signal.name} already exists"
            raise ValueError(error)

        else:
            self.signal.add(new_signal)
            # self.links[new_signal.name] = []
            return new_signal

    def emit_signal(self,signalname:str,**kwargs)->None:
        # print(self.signal.registry_by_name)
        sig:SignalEvent = self.signal.by_name(signalname)
        out = {}
        if len(kwargs) == len(sig.signature):
            for k,v in kwargs.items():
                if k not in sig.signature.keys():
                    error=f"{k} not in args! Need {sig.signature} "
                    raise ValueError(error)
                if not isinstance(v,sig.signature[k]):
                    error=f"{k} has the wrong type! Need {sig.signature} "
                    raise ValueError(error)


            for subname in self.links[sig.name]:
                sub:SignalSubscriber = self.subscriber.by_name(subname)
                sub.lnk(**kwargs)