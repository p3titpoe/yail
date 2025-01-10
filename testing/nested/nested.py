import inspect
import yail as logger
from yail.formatter import Formatter
from yail.logic import LoggerLevel
fmt = logger.formatter.Formatter("Test")

log = logger.get_logger('test2')
class nestedclass:
    def __init__(self,ar = 10):
        self.ar = ar
        # log.debug("Init")

    def nestedBlas(self,x:int,y:int,z:int):
        data = x*y*z
        # log.debug("Mulitplicated",loggger_msg_data=data)
        return fmt.compile_new("TEST", inspect.currentframe(), LoggerLevel.DEBUG)

