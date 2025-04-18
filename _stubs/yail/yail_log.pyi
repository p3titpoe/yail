from .logic import *
from .formatter.formatter import Formatter as Formatter
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
    def debug(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None: ...
    def info(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None: ...
    def warning(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None: ...
    def error(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None: ...
    def critical(self, info: str, loggger_msg_data: any = None, external_frame: any = None) -> None: ...

@dataclass(init=False)
class LoggerManager:
    def __init__(self) -> None: ...
    def mute_all_or_sip(self, sip: str = None) -> None: ...
    def solo_logger(self, name: str) -> None: ...
    def solo_off(self, name: str = None) -> None: ...
    def mute_logger(self, logger: str) -> None: ...
    def mute_off(self, name: str = None) -> None: ...
    def stop_processing_all(self) -> None: ...
    def stop_processing(self, name: str) -> None: ...
    def resume_processing(self, name: str = None) -> None: ...
    @property
    def rootcache(self) -> MasterLoggerCache: ...
    @property
    def rootlogger(self) -> MasterLoggerCache: ...
    def get_logger_by_name(self, name: str) -> LoggerCacheline: ...
    def make_new_logger(self, name: str) -> BaseLogger: ...
    def shutdown(self) -> None: ...
