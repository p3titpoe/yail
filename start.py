import inspect

import testing.nested.nested
import yail as logger
import yail.formatter.formatter
from yail.logic import LoggerLevel,LoggerMessage
from testing.models import testclass,testclassb
from testing.nested.innernested.blested import  nestedclass

def infoprint():
    reg = logger.rootcache().registry
    log_ = [(reg[x].name, reg[x].logger.log_level) for x in logger.rootcache().booked]
    out = [f"{x[0]:<15} :: {x[1].name:<16}\n" for x in log_]
    print("".join(out))


hh =logger.get_logger("OOOOO")

logger.master_loglevel('info')
# infoprint()

logger.warning("BLAAA")

hh.debug("trztrztrztrzt")
logger.master_loglevel('warning')
infoprint()
hh.error("ERRtruzpoipökjklhh")
hh.info("INFOOOOOOO")
# fmt = yail.formatter.Formatter("Test")
oo = testclassb()
bb = testclass()
class testclassc:
    def __init__(self, bb="WWWW"):
        hh.info("Init Testclassc")
        self.ar = bb

    def harrr(self):
        msg = ("This is a veryyyy loooong sentence,just to check how the it displays in the colnsole,considering allmeans."
               ",just to check how the it displays in the colnsole,considering allmeans.")
        hh.debug(msg)

    def haha(self):
        # fmt.conf.default_long = "loglevel name:msg"
        hh.info("vvvvvvv")
        logger.debug("mnbmnb",{2:45,4:"tztut",0:"loki"})
oo.blas()

# logger.master_loglevel('error')
logger.master_loglevel('error')
bb.blas()
infoprint()
nn = testclassc(bb="WWWWWW")
nn.harrr()
nn.haha()
log_types = []