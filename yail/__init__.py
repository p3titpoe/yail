from . import signaling as signals
from .loggers import *
from .handlers import HandlerManager
from inspect import currentframe

__doc__="""

"""
############################################################
# Set Up Signaling
############################################################
signals._sign_manager.create_signal('system-bus', {'msg_obj': LoggerMessage})
signals._sign_manager.create_signal('system-aux', {'msg_obj': LoggerMessage})
signals._sign_manager.create_signal('system-com', {'msg_obj': LoggerMessage})
signals._sign_manager.create_signal("handler-console", {'msg_obj':LoggerMessage})
signals._sign_manager.create_signal("handler-file", {'msg_obj':LoggerMessage})

############################################################MEbe
# Set Up BaseClasses
############################################################
loggers:LoggerManager = start_log__manager()
handlers:HandlerManager = HandlerManager()

##############################################################
# Convenience Functions for handlers
##############################################################
def master_loglevel(loglvlname: str) -> None:
    loggers.set_loglevel(loglvlname)

def console_mute(loggername:str)->None:
    """Acts as a toggle"""
    handlers.handler.console.mute_loggers(loggername)

def file_mute(loggername:str)->None:
    """Acts as a toggle"""
    handlers.handler.file.mute_loggers(loggername)

##############################################################
# convennience functions for logging to root loggger
#
##############################################################
def debug(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    loggers._root_logger.debug(info, loggger_msg_data, external_frame=frame)

def info(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    loggers._root_logger.info(info, loggger_msg_data, external_frame=frame)

def warning(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    loggers._root_logger.warning(info, loggger_msg_data, external_frame=frame)

def error(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    loggers._root_logger.error(info, loggger_msg_data, external_frame=frame)

def critical(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
    frame = currentframe().f_back
    loggers._root_logger.critical(info, loggger_msg_data, external_frame=frame)


