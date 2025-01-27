from .yail_log import LoggerCache,LoggerManager,BaseLogger,LoggerLevel,LoggerCacheline,LoggerMessage
from inspect import currentframe

LOGGER:LoggerManager = LoggerManager()

def get_logger(name:str)->BaseLogger:
    return LOGGER.make_new_logger(name)

def logger_by_name(name:str)->BaseLogger:
    return LOGGER.get_logger_by_name(name).logger

def muteall()->None:
    LOGGER.mute_all_or_sip()
def muteoff()->None:
    mute()
def sip(loggername:str)->None:
    LOGGER.mute_all_or_sip(loggername)
    info(f"Solo in Place for {loggername}")

def sipoff()->None:
    solo()

def solo(name:str = None)->None:
    if name is None:
        LOGGER.solo_off()
    else:
        LOGGER.solo_logger(name)

def mute(name:str = None)->None:
    if name is None:
        LOGGER.mute_off()
    else:
        LOGGER.mute_logger(name)

def stop_processing(name:str | None)->None:
    if name is None:
        warning("Logger will stop all processing!!!")
        LOGGER.stop_processing_all()
    else:
        LOGGER.stop_processing(name)
def resume_processing(name:str|None)->None:
    if name is None:
        warning("Logger will stop all processing!!!")
        LOGGER.stop_processing_all()
    else:
        LOGGER.stop_processing(name)
        info(f"Resuming processing of logger {name}")

##############################################################
# convennience functions for logging to root loggger
#
##############################################################


def rootcache()->LoggerCache:
    return LOGGER._root_cache

def rootlogger()->BaseLogger:
    return LOGGER._root_logger

##############################################################
# convennience fucnctions for logging to root loggger
#
##############################################################
def debug(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    LOGGER._root_logger.debug(info,loggger_msg_data)

def info(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    LOGGER._root_logger.info(info,loggger_msg_data,frame)

def warning(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    LOGGER._root_logger.warning(info,loggger_msg_data)

def error(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    LOGGER._root_logger.error(info,loggger_msg_data)


def critical(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    LOGGER._root_logger.critical(info,loggger_msg_data)


