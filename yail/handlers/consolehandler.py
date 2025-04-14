from dataclasses import dataclass,field
from yail.logic import LoggerLevel
from yail.formatter.formatter import Formatter

@dataclass
class BaseHandler:
    _htype:
    _formatter:Formatter
