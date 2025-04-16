## Quick Start
:::{note}
yail is still alpha, so changes may occur frequently 
:::
### Import
yail has an extensive api for manipulating how and where your log messages should be routed.
It gives you access to a root logger from the start.

```python
import yail as logger
```

### Root Logger

You can log directly to the root logger after import.

```python
logger.info("Hello World")
logger.warning("Hello World! You are burning")
```
This is ok for small projects where you only need one logger and then filter by log level.
yail features an introspective package column tracking up to module level who called the log function.

:::{warning}
The root logger is **not** affected by these functions: 
- mute
- solo 
- processing
- log level
:::

### Use cases
yail gives you enough flexibility for creating loggers as to adapt to most use cases.
For example, active loggers are NOT shareable per default, but they can be set to public and so be retrieved everywhere yail is imported.


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

warn = logger.get_logger("Warn")

logger.warning("Hello World! You are burning")


```



```{py:function} send_message(sender, priority)

Send a message to a recipient

:param str sender: The person sending the message
:param priority: The priority of the message, can be a number 1-5
:type priority: int
:return: the message id
:rtype: int
:raises ValueError: if the message_body exceeds 160 characters
```