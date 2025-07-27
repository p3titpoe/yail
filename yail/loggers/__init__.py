from .logic import LoggerLevel,LoggerMessage,LoggerStack
from .logger import LoggerManager, BaseLogger

loggers:LoggerManager = None

############################################################
# Convenience Logger Functions
############################################################
def start_log__manager()->LoggerManager:
    global loggers
    if not isinstance(loggers,LoggerManager):
        loggers = LoggerManager()
    return loggers

def get_logger(name:str, loglevel:LoggerLevel=None, public:bool=False,block_level=False, handlers:list = None)->BaseLogger:
    hlist = ['handler-console']
    if handlers is not None:
        hlist.extend(handlers)
    return loggers.make_new_logger(name, loglevel=loglevel, public=public, block_level=block_level, handlers=hlist)

def logger_by_name(name:str)->BaseLogger:
    return loggers.get_logger_by_name(name)

def loglevel(loglvlname:str,loggername:None)->None:
    loggers.set_loglevel(loglvlname, loggername)

def stop_processing(name:str | None)->None:
    if name is not None:
        loggers.rootlogger.warning(f"Logger {name} will stop all processing!!!")
        loggers.stop_processing(name)

def resume_processing(name:str|None)->None:
    if name is not None:
        loggers.rootlogger.info(f"Resuming processing of logger {name}")
        loggers.stop_processing(name)

def mute_logger(logger:str | list[str])->None:
    loggers.mute_loggers(logger)

def solo_logger(logger:str | list[str])->None:
    loggers.solo_loggers(logger)
