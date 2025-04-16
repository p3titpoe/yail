## Yail
Yet Another Interactive Logger

> [!NOTE]
> yail is still alpha, so changes may occur frequently 


## Features
yail is being developed with a 'coding phase first' approach,giving the user the ability to handle the log system like an audio console.

Analog to it, yail provides mute, solo, SIP, loglevel and group controls for logging to the terminal and other output handlers.

Loggers in yail can be locked to a certain log level and made shareable.

It features a simple template system for different log levels and overrides on an output handler basis.  


### Basic Usage

##### Root Logger
yail gives you access to a console logger from the start.

```python
import yail as logger

logger.info("Hello World")
logger.warning("Hello World! You are burning")
```

This is ok for small projects where you only need one logger and then filter by log level.
yail features an introspective package column tracking up to module level who called the log function.

> [!warning]
> The root logger is **not** affected by these functions: 
> - mute
> - solo 
> - processing
> - log level


##### Get a new logger
yail gives you enough flexibility for creating loggers as to adapt to most use cases.
For example, active loggers are NOT shareable per default, but they can be set to public and so be retrieved everywhere yail is imported.

```python
#main.py
import yail as logger
from yail import LoggerLevel

#public controls whether the logger can be called from another module
#block_level set to True blocks the logger at his initial loglevel to keep it safe from global level change
log = logger.get_logger(name='MyLogger',  
                        loglevel=LoggerLevel.INFO,
                        public=True, 
                        block_level=False
                        )

log.info("Hello World")
```
##### Get a created public logger
```python
#other.py
import yail as logger

log = logger.logger_by_name('MyLogger')
log.info("Hello World")
```
##### Orchestrate 

#### Case 1: Single loggers for warning and error messages
```python
#Main py
import yail as logger 
from yail import LoggerLevel

#Define the loggers
warn_logger = logger.get_logger('Warn')
warn_logger.set_loglevel(LoggerLevel.WARNING)
err_logger = logger.get_logger('Error')
err_logger.set_loglevel(LoggerLevel.ERROR)

#other py
import yail as logger

warn = logger.logger_by_name("Warn")

logger.warning("Hello World! You are burning")


```
