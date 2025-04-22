from yail.formatter.columns.columns import *
__doc__="""
        Allowed tags & Options:

            - date

                * today - date.today "YYYY-MM-DD"
                * isodat - date.now.isoformat "YYYY-MM-DD HH:MM:SS"

                Ex:
                    | date today

            - package

                * pmcf - PackageModuleClassFunction - abbreviation for .settinggs
                * args - show args
                * argsval -show args & value

                Ex:
                    | package mcf args #hides package
                    | package cf argsval #hides package & module

            - msg
                * None

            - data
                * None

            - loglevel
                * name
                * value

            - lineno
                * pad1(0*n) = number padding

                Ex:
                    * lineno pad1 #01
                    * lineno pad1 #100
                    * lineno pad4 #00001
                    * package cf argsval #hides package & module

            - logger
                * None
"""

class ColumnType(Enum):
    DATE = DateColumn
    PACKAGE = PackageColumn
    MSG = MsgColumn
    LOGLEVEL = LoglevelColumn
    LINENO = LinenoColumn
    DATA = DataColumn
    LOGGER = LoggerColumn

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att
