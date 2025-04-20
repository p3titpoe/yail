from linecache import cache

from . import signaling as sig
from .loggers import LoggerManager,BaseLogger,LoggerLevel,LoggerStack,LoggerMessage
from inspect import currentframe
from .handlers import HandlerObject, HandlerManager

__doc__="""

"""
############################################################
# SET Up Signaling
############################################################
#SetUp a new cache
sig_cache = sig.SignalCache()
sig_cache.create_signal('system-bus', {'msg_obj': LoggerMessage})
sig_cache.create_signal('system-aux', {'msg_obj': LoggerMessage})
sig_cache.create_signal('system-com', {'msg_obj': LoggerMessage})
sig_cache.create_signal("handler-console",{'msg_obj':LoggerMessage})
sig_cache.create_signal("handler-file",{'msg_obj':LoggerMessage})

#Link the new cache
sig._sign_manager = sig_cache
sig.signals = sig._sign_manager.signal
sig.subscribers = sig._sign_manager.subscriber
############################################################
# SET Up BaseClasses
############################################################
stacks:LoggerManager = LoggerManager()
handlers:HandlerManager = HandlerManager()




# cc = handlers.create_handler(HandlerObject.FILE,fh_path="/home/petrit/Documents/llm_test_dir")

############################################################
# Convenience Logger Functions
############################################################

def get_logger(name:str, loglevel:LoggerLevel=None, public:bool=False, block_level=False)->BaseLogger:
    return stacks.make_new_logger(name, loglevel=loglevel, public=public, block_level=block_level, handlers=['handler-console'])

def logger_by_name(name:str)->BaseLogger:
    return stacks.get_logger_by_name(name)
#
# def stacks


def loglevel(loglvlname:str,loggername:None)->None:
    stacks.set_loglevel(loglvlname, loggername)
def master_loglevel(loglvlname:str)->None:
    stacks.set_loglevel(loglvlname)
def stop_processing(name:str | None)->None:
    if name is None:
        warning("Logger will stop all processing!!!")
        stacks.stop_processing_all()
    else:
        stacks.stop_processing(name)
def resume_processing(name:str|None)->None:
    if name is None:
        warning("Logger will stop all processing!!!")
        stacks.stop_processing_all()
    else:
        stacks.stop_processing(name)
        info(f"Resuming processing of logger {name}")

##############################################################
# Convenience Fucntions for handlers
##############################################################
def muteall()->None:
    stacks.mute_all_or_sip()

def muteoff()->None:
    mute()

def sip(loggername:str|None)->None:
    msg = "Solo In Place OFF!"
    if loggername is None:
        solo()

    else:
        stacks.mute_all_or_sip(loggername)
        msg=f"Solo in Place for {loggername}"
    info(msg)

def solo(name:str = None)->None:
    if name is None:
        stacks.solo_off()
    else:
        stacks.solo_logger(name)

def mute(name:str = None)->None:
    if name is None:
        stacks.mute_off()
    else:
        stacks.mute_logger(name)

##############################################################
# convennience functions for logging to root loggger
#
##############################################################
def debug(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    stacks._root_logger.debug(info, loggger_msg_data, external_frame=frame)

def info(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    stacks._root_logger.info(info, loggger_msg_data, external_frame=frame)

def warning(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    stacks._root_logger.warning(info, loggger_msg_data, external_frame=frame)

def error(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    stacks._root_logger.error(info, loggger_msg_data, external_frame=frame)

def critical(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    stacks._root_logger.critical(info, loggger_msg_data, external_frame=frame)


