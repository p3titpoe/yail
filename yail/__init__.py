
from .loggers import LoggerManager,BaseLogger,LoggerLevel,LoggerStack,LoggerMessage
from inspect import currentframe
from .handlers import HandlerObject, HandlerManager

############################################################


yail:LoggerManager = LoggerManager()
handlers:HandlerManager = HandlerManager()

def get_logger(name:str, loglevel:LoggerLevel=None, public:bool=False, block_level=False)->BaseLogger:
    return yail.make_new_logger(name, loglevel=loglevel, public=public, block_level=block_level)

def logger_by_name(name:str)->BaseLogger:
    return yail.get_logger_by_name(name)

def muteall()->None:
    yail.mute_all_or_sip()

def muteoff()->None:
    mute()

def sip(loggername:str|None)->None:
    msg = "Solo In Place OFF!"
    if loggername is None:
        solo()

    else:
        yail.mute_all_or_sip(loggername)
        msg=f"Solo in Place for {loggername}"
    info(msg)

def solo(name:str = None)->None:
    if name is None:
        yail.solo_off()
    else:
        yail.solo_logger(name)

def mute(name:str = None)->None:
    if name is None:
        yail.mute_off()
    else:
        yail.mute_logger(name)

def loglevel(loglvlname:str,loggername:None)->None:
    yail.set_loglevel(loglvlname, loggername)
def master_loglevel(loglvlname:str)->None:
    yail.set_loglevel(loglvlname)
def stop_processing(name:str | None)->None:
    if name is None:
        warning("Logger will stop all processing!!!")
        yail.stop_processing_all()
    else:
        yail.stop_processing(name)
def resume_processing(name:str|None)->None:
    if name is None:
        warning("Logger will stop all processing!!!")
        yail.stop_processing_all()
    else:
        yail.stop_processing(name)
        info(f"Resuming processing of logger {name}")

##############################################################
# convennience functions for accessing the rootcache and
# - logger
##############################################################


def rootcache()->any:
    return yail._root_cache

def rootlogger()->BaseLogger:
    return yail._root_logger

##############################################################
# convennience fucnctions for logging to root loggger
#
##############################################################
def debug(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    yail._root_logger.debug(info, loggger_msg_data, external_frame=frame)

def info(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    yail._root_logger.info(info, loggger_msg_data, frame, external_frame=frame)

def warning(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    yail._root_logger.warning(info, loggger_msg_data, external_frame=frame)

def error(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    yail._root_logger.error(info, loggger_msg_data, external_frame=frame)

def critical(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    yail._root_logger.critical(info, loggger_msg_data, external_frame=frame)


