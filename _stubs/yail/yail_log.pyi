from .logic import *
from .formatter import Formatter as Formatter
from dataclasses import dataclass
from datetime import datetime as datetime

class BaseLogger:
    parent: any
    log_level: LoggerLevel
    def __init__(self, name: str, parent: any, log_level) -> None: ...
    @property
    def solo(self) -> bool: ...
    @property
    def mute_all(self) -> bool: ...
    @property
    def console(self) -> bool: ...
    @property
    def cache(self) -> LoggerCache: ...
    @property
    def loggername(self) -> str: ...
    @property
    def formatter(self) -> Formatter: ...
    def toggle_solo(self) -> bool: ...
    def toggle_mute_all(self) -> bool: ...
    def toggle_console(self) -> bool: ...
    def toggle_data(self) -> None: ...
    def toggle_short(self) -> None: ...
    def debug(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
    def info(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
    def warning(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
    def error(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
    def critical(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """

@dataclass(init=False)
class LoggerManager:
    def __init__(self) -> None: ...
    def mute_all_or_sip(self, sip: str = None) -> None:
        """
            Mutes all Loggers.
            If a loggername is given in siü, it acts as SOLO IN PLACE.

            Solo in Place overrides every solo,meainig it's destructive where as the normal soolo functio is additive.


        """
    def solo_logger(self, name: str) -> None:
        """
            Solo's the logger.

            When first invoked, it sip's(solo in place) the loggers,
            then adds every solo'd logger to the solo bus
        """
    def solo_off(self, name: str = None) -> None: ...
    def mute_logger(self, logger: str) -> None:
        """ Muets the logger, is additive"""
    def mute_off(self, name: str = None) -> None: ...
    @property
    def rootcache(self) -> MasterLoggerCache: ...
    @property
    def rootlogger(self) -> MasterLoggerCache: ...
    def get_logger_by_name(self, name: str) -> LoggerCacheline: ...
    def make_new_logger(self, name: str) -> BaseLogger: ...
    def shutdown(self) -> None: ...
