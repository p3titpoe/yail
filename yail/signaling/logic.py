import inspect
from dataclasses import dataclass,field
from typing import Callable
from enum import Enum
from .registry import RegistryController,RegistryEntry


@dataclass
class SignalEvent(RegistryEntry):
    """Registry Entry for the Signals"""
    _sig:dict[str:type]
    docs:str = "Executor is the func being executed when the signal is called"
    _emitted:dict[str:int] = None

    def __post_init__(self):
        self._emitted = {}

    @property
    def signature(self)->list:
        return self._sig

    @property
    def emitted(self)->dict[str:int]:
        return self._emitted

    @emitted.setter
    def emitted(self, value:str)->None:
        if value not in self._emitted:
            self._emitted[value] = 0
        self._emitted[value] += 1


@dataclass
class SignalSubscriber(RegistryEntry):
    """
    Registry Entry for the subscriber
    """
    _receiver_func:Callable
    _subscription:SignalEvent

    def __post_init__(self):
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
        """ hooks on Registry when registry is deleted"""
        if isinstance(who,SignalEvent):

            for k in self.links[who.name]:
                regid = self.subscriber.registry_by_name[k]
                self.subscriber.registry.unregister(regid)
            del self.links[who.name]

        if isinstance(who,SignalSubscriber):
            sig:SignalEvent = who._subscription
            self.links[sig.name].remove(who.name)

    def _on_add(self,who)->None:
        """ Hook on Registry when entry is added"""

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
        """
            Subscribe the given function to the given Signal.

            Subscriber names have to be unique. but a function can listen to more channels other different subscriber name
        """
        sig = self.signal.by_name(signal_name)
        new_subscriber = SignalSubscriber(subscriber_name,receiver_func,sig)
        self.subscriber.add(new_subscriber)
        return new_subscriber

    def unsubscribe(self,subscriber_name:str)->None:
        """
        Unsubscribe the given subscriber from the signal it's listening to.
        """
        if subscriber_name in self.subscriber.registry_by_name:
            sub:SignalSubscriber = self.subscriber.by_name(subscriber_name)
            self.subscriber.rm(subscriber_name)

    def create_signal(self, signalname:str,signature:dict[str:type],docs:str="Say somtehing")->SignalEvent:
        """
        Creates a new signal.

        .. warning:
           The signal name MUST be unique.
        """
        new_signal = SignalEvent(signalname,signature,docs)
        if signalname in self.signal.registry_by_name:
            error = f"A signal named {new_signal.name} already exists"
            raise ValueError(error)

        else:
            self.signal.add(new_signal)
            return new_signal

    def emit_signal(self,signalname:str,**kwargs)->None:
        """Emits the given the signal."""

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