import inspect
import yail as logger
import yail.formatter.templates.base_console_template as testml

log = logger.get_logger('test2',logger.LoggerLevel.WARNING,public=True)
log2 = logger.get_logger('test22',logger.LoggerLevel.ERROR,block_level=True)

class testclass:
    """ TEST cLSS 111
    sddfdsfdfdsfsd
    sdfdfdfdsfd



    """

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

    def __init__(self, ar:int=10):

        self.ar:int = ar
        self.log:logger.BaseLogger=logger.get_logger('test3')
        log.debug("Init 2")
        self.log.warning("INIT Warn")
        self.log.error("INIT Erro")

    def blas(self):
        self.log.debug("Mulitplicated  2", loggger_msg_data={"dd":1212,"eee":33})
        log.error("Init Error")
        log2.critical("Init Error",loggger_msg_data=testml)
        self.log.debug("Init Debug",loggger_msg_data=[1,2,3,4,5,6])
        self.log.info("Init Info")

    def error_re(self,ff:bool=False):
        try:
            if ff:
                print("FF")
        except:
            bb = ValueError("ERRRR")
            log2.warning("Exception Test",loggger_msg_data=bb)
            self.log.critical("EXCEPTION")

def tsrtsr(kk:str,vv:str)->str:
    out = f"{kk} = {vv}"
    log.info(f"Function output:: {out}")
    # print(out)

tsrtsr('heloo','wöörld')