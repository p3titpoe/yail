Yail Toplevel
=============

Provided classes, properties and functions by the yail package.

Classes
^^^^^^^

.. py:class:: LoggerLevel

   Enum with the Logger levels form DEBUG to CRITICAL

.. py:class:: LoggerMessage

   Dataclass, main class for passing logger messages over the signal busses

.. py:class:: LoggerStack

   Dataclass, Entry class for the Loggger registry. Is responsible for sending logg message to the right signals.

.. py:class:: LoggerManager

   Dataclass, Orchestrator for the created loggers

.. py:class:: BaseLogger

   Dataclass, simple Logger class.

Properties
^^^^^^^^^^

.. py:property:: handlers

    Access to the output handlers library

.. py:property:: loggers

    Access to the loggers library

.. py:property:: signals

    Access to the signals library


Functions
^^^^^^^^^

.. py:function:: debug(info: str, loggger_msg_data: any = None)

   Debug logger function. Shortcut to the rootlogger

.. py:function:: info(info: str, loggger_msg_data: any = None)

   Info logger function. Shortcut to the rootlogger

.. py:function:: warning(info: str, loggger_msg_data: any = None)

   Warning logger function. Shortcut to the rootlogger

.. py:function:: error(info: str, loggger_msg_data: any = None)

   Error logger function. Shortcut to the rootlogger

.. py:function:: critical(info: str, loggger_msg_data: any = None)

   Critical logger function. Shortcut to the rootlogger

Some examples
^^^^^^^^^^^^^

.. code-block::

    import yail

    #create a basic filehandler
    yail.handlers._create_handler('file',"/home/user/Documents/log_test_dir")

    #create logs to the root root logger
    yail.info('Message to the World')

    # Create a new logger
    logger = get_logger(name='Mylogger',
                    loglevel=LoggerLevel.INFO,
                    public = True,
                    blockl_level = True)

    #Logg yourself out!
    logger.info('What a nice day')
    logger.critical('Finances are very low')

    #Possible mute functionality
    #This will mute a logger in the file output
    yail.handler.file.mute_logger('Mylogger')

    #This will unmute a previously muted logger in the file output
    yail.handler.file.mute_logger('Mylogger')

    #This will unmute every logger in the file output
    yail.handler.file.mute_logger()


    #This will mute a logger in the console output
    yail.handler.console.mute_logger('Mylogger')

    #This will mute the logger globally
    yail.loggers.muter_logger('MyLogger)

    #Sunscribing a function to a systembus.
    #Systembus msgs enforce {'msg': LoggerMessage}
    yail.signals.subsribe('system-listerner-1','system-com',testfunc)

