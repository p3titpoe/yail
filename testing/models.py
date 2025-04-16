import inspect
import yail as logger

log = logger.get_logger('test2',logger.LoggerLevel.WARNING,public=True)
log2 = logger.get_logger('test22',logger.LoggerLevel.ERROR,block_level=True)

class testclass:
    def __init__(self,ar = 10):
        self.ar = ar
        log.debug("Init Debug")
        log2.warning("Init Wann")
        log.error("Init Error")

    def blas(self):
        # log.debug("Mulitplicated",loggger_msg_data=data)
        log2.warning("WAERNIFNF")
        log2.error("Blas Error")
        log.critical("Ctritical Error")

class testclassb:
    def __init__(self, ar=10):
        self.ar = ar
        self.log=logger.get_logger('test3')
        log.debug("Init 2")
        self.log.warning("INIT Warn")
        self.log.error("INIT Erro")

    def blas(self):
        self.log.debug("Mulitplicated  2", loggger_msg_data={"dd":1212,"eee":33})
        log.error("Init Error")
        log2.critical("Init Error")
        self.log.debug("Init Debug")
        self.log.info("Init Info")

        # for k,x in logger.LOGGER._root_cache.registry.items():
        #     if x is not None:
        #         print("Sub Logger",k,"  ",x.name)
        # logger.info("Testing Root in other classes")
        # return fmt.compile_new("TEST", inspect.currentframe(), LoggerLevel.DEBUG)

        # return data

def tsrtsr(kk:str,vv:str)->str:
    out = f"{kk} = {vv}"
    log.info(f"Function output:: {out}")
    # print(out)

tsrtsr('heloo','wöörld')