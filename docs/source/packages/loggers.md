### Loggers

Logger classes.

#### Usage

:::{note}
By default, evey logger will output to the console.
Filehandlers have to added manually (because )
:::

- Request a new logger 
- Start logging

Loggers offer the ability to be public - eg. reusable throughout your project - or block_leveled - meaning the logger is blocked at the initial log lvevl.



```python
#main.py
from yail import get_logger, LoggerLevel

# Create a new logger
logger = get_logger(name='Mylogger',
                    loglevel=LoggerLevel.INFO,
                    public = True,
                    blockl_level = True)

#Logg yourself out!
logger.info('What a nice day')
logger.critical('Finances are very low')

```
In another file of your project you could import your logger like this

```python
from yail import loggers
known_logger = loggers.get_logger_by_name('Mylogger')

known_logger.warning(('Logger logging from'))
```

#### Package Overview
yail provides the convenience variable **loggers** as a direct access to the siganling library.

Naturally, you can also import the parts you need from the library.

Main classes:
- LoggerManager
- LoggerLevel
- LogerStack
- Baselogger

Functions:
- start_log__manager()
- get_logger()
- logger_by_name  
- loglevel()

Members:
- loggers (shortcut to the loggers Registry)


Below is an overview of the most used functions & members


```python
from yail.loggers import *

#Start up the Loggermanager
loggers = start_log__manager()

#Create a new Logger
log = get_logger('Mylogger',LoggerLevel.DEBUG)
log.warning('This is a WARNING!')

#Access to the loggers registry
loggers.loggers.logger_by_name

#Access to the root logger
loggers.rootlogger.warning('A Root Warning')
```

:::{note}
Yail module provides all the logging functions as a shortcut on the toplevel. 
:::

