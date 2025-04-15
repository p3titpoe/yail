from .logic import *

class FormatterType(Enum):
    CONSOLE = ConsoleFormatter
    WEB = BaseFormatter
    SOCKET = BaseFormatter
    FILE = BaseFormatter

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att
