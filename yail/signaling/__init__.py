from .logic import SignalCache,SignalSubscriber,SignalEvent,Callable

_sign_manager = SignalCache()

subscribers = _sign_manager.subscriber
signals = _sign_manager.signal


def subscribe(subscriber_name:str,signal_name:str,receiver_func:Callable)->SignalSubscriber:
    sub =_sign_manager.subscribe(subscriber_name,signal_name,receiver_func)
    return sub

def unsubscribe(subscriber_name:str)->None:
    _sign_manager.unsubscribe(subscriber_name)

def new_signal(signalname: str, signature: dict[str:type], docs: str = "Say somtehing") -> SignalEvent:
    sig = _sign_manager.create_signal(signalname,signature,docs)
    return sig

def emit(signalname:str,**kwargs)->None:
    _sign_manager.emit_signal(signalname, **kwargs)
