## Yail
Yet Another Interactive Logger

> [!NOTE]
> yail is still alpha, so changes may occur frequently 


## Features
yail is being developed with a 'coding phase first' approach,giving the user the ability to handle the log system like an audio console.

Analog to it, yail provides mute, solo, SIP, loglevel and group controls for logging to the terminal and other output handlers.

Loggers in yail can be locked to a certain log level and made shareable.

It features a simple template system for different log levels and overrides on an output handler basis.  

### Available Features 
> [!NOTE]
> As of April 2025

**Management**
- [x] Global Mute, Solo and Set Levels
- [x] Stop processing
- [x] Mute by log level
- [ ] Grouping
- [ ] Colored output

**Loggers**
- [x] Share logger
- [x] Block Logger at init level
- [x] Mute, Solo & Set level

**Output Handlers**
- [x] Console
- [x] File


### Basic Usage

##### Root Logger
yail gives you access to a console logger from the start.

```python
import yail 

yail.info("Hello World")
yail.warning("Hello World! You are burning")
```

This is ok for small projects where you only need one logger and then filter by log level.<br>
yail features an introspective package column tracking up to module level who called the log function.

> [!warning]
> The root logger is **not** affected by these functions: 
> - mute
> - solo 
> - processing
> - log level


##### Get a new logger
yail gives you enough flexibility for creating loggers as to adapt to most use cases.<br>
For example, loggers are NOT shareable per default, but they can be set to public and so be retrieved everywhere yail is imported.

```python
#main.py
import yail
from yail import LoggerLevel

#public controls whether the logger can be called from another module
#block_level set to True blocks the logger at his initial loglevel to keep it safe from global level change
log = yail.get_logger(name='MyLogger',  
                        loglevel=LoggerLevel.INFO,
                        public=True, 
                        block_level=False
                        )

log.info("Hello World")
```

##### Get a created public logger
```python
#other.py
import yail

log = yail.logger_by_name('MyLogger')
log.info("Hello World")
```

##### Orchestrate loggers
Let's assume you have several loggers created through your code and are working on a specific part of it.<br>
Sometimes you might want to single out different loggers or mute others to compare outputs for example.<br>
As long as yail is imported you can control them from anywhere.

```python
#another.py
import yail 

#mute function
yail.mute('MyLogger')
yail.mute('MyLogger4')

yail.muteall()
yail.muteoff()

#Solo In Place
yail.sip('MyLogger')
yail.sip() #offs the sip





```

