from yail.formatter.columns.columns import *

class ColumnType(Enum):
    DATE = DateColumn
    PACKAGE = PackageColumn
    MSG = MsgColumn
    LOGLVL = LoglevelColumn
    LINENO = LinenoColumn
    DATA = DataColumn
    LOGGER = LoggerColumn

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att
