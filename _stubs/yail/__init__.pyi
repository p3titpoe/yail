from .yail_log import BaseLogger, LoggerCache, LoggerCacheline as LoggerCacheline, LoggerLevel as LoggerLevel, LoggerManager, LoggerMessage as LoggerMessage

LOGGER: LoggerManager

def get_logger(name: str) -> BaseLogger: ...
def logger_by_name(name: str) -> BaseLogger: ...
def muteall() -> None: ...
def muteoff() -> None: ...
def sip(loggername: str) -> None: ...
def sipoff() -> None: ...
def solo(name: str = None) -> None: ...
def mute(name: str = None) -> None: ...
def rootcache() -> LoggerCache: ...
def rootlogger() -> BaseLogger: ...
def debug(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
def info(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
def warning(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
def error(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
def critical(info: str, loggger_msg_data: any = None) -> None:
    """
        Calls on root logger
    """
