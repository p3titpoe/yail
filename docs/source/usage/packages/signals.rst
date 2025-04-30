Signals
=======

Simple messaging library.
Enforces signature defined in signalchannel to ensure integrity

.. note::
   SignalChannel and SignalSubscriber will have unique names enforced.
   Raises ValueError if double detected


Usage
^^^^^

- Create a new signal
- Subscribe the function to the signal channel
- Every function subscribed to the channel will get the data

.. code-block::

    #main.py
    from yail import signals

    # Create a new channel
    signals.new_signal(signalname='mysignal',signature={'data':object})

    #Dummy Function to subscribe
    def dummyfunc(data:object)->None:
        #Do something with the data
        new_data = data

    #Subscribe to the signal
    signals.subscribe(subscriber_name='i-am-subscriber',
                      signal_name='mysignal',
                      receiver_func=dummyfunc)

In another file of your project

.. code-block::

    from yail import signals,LoggerLevel
    signals.emit('mysignal',data=LoggerLevel.ERROR)

Package Overview
^^^^^^^^^^^^^^^^

yail provides the convenience variable **signals** as a direct access to the loggers library.

Naturally, you can also import the parts you need from the library.

Main classes:
    - SignalCache
    - SignalEvent
    - SignalSubscriber

Functions:
    - subscribe
    - unsubscribe
    - new_signal
    - emit

Members:
    - subscribers (shortcut to the susbscriber Registry)
    - signals (shortcut to the signals Registry)

Below is an overview of the most used functions & members

.. code-block::

    from yail.signaling import *

    #access to the subscriber
    subscribers.registry_by_name
    subscribers.by_name('Myentry')
    subscribers.rm('Myentry')

    #access ro signals
    signals.registry_by_name
    signals.booked
    signals.rm('mysignal')

