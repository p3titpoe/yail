import inspect
import yail as logger
from yail.formatter import Formatter
from yail.logic import LoggerLevel
fmt = logger.formatter.Formatter("Test")

log = logger.get_logger('test2')
class testclass:
    def __init__(self,ar = 10):
        self.ar = ar
        # log.debug("Init")

    def blas(self,x:int,y:int):
        data = x*y
        # log.debug("Mulitplicated",loggger_msg_data=data)
        return data


class testclassb:
    def __init__(self, ar=10):
        self.ar = ar
        self.log=logger.get_logger('test3')
        log.debug("Init 2")

    def blas(self, x: int, y: int):
        data = x * y
        self.log.debug("Mulitplicated  2", loggger_msg_data=data)
        # for k,x in logger.LOGGER._root_cache.registry.items():
        #     if x is not None:
        #         print("Sub Logger",k,"  ",x.name)
        # logger.info("Testing Root in other classes")
        # return fmt.compile_new("TEST", inspect.currentframe(), LoggerLevel.DEBUG)

        # return data
