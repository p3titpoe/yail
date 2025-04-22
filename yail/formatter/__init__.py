from .logic import *

class FormatterStyle(Enum):
    CONSOLE_TXT = ConsoleFormatter
    CONSOLE_JSON = ConsoleFormatter
    FILE_TXT = FileFormatter
    FILE_MD = FileFormatter
    FILE_JSON = FileFormatter

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att

