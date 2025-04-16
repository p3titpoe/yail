import inspect

import testing.nested.nested
import yail as logger
from yail import LoggerLevel
# import yail.formatter.formatter
from testing.models import testclass,testclassb
from testing.nested.innernested.blested import  nestedclass

def infoprint():
    reg = logger.rootcache().registry
    log_ = [(reg[x].name, reg[x].logger.log_level) for x in logger.rootcache().booked]
    out = [f"{x[0]:<15} :: {x[1].name:<16}\n" for x in log_]
    print("".join(out))

hh =logger.get_logger("OOOOO")

# logger.master_loglevel(LoggerLevel.CRITICAL)
# infoprint()
tst = logger.logger_by_name('test2')

tst.log("Log has happened")

logger.muteall()
logger.warning("BLAAA")
hh.debug("trztrztrztrzt")

logger.master_loglevel('critical')
# # infoprint()q
hh.error("ERRtruzpoipökjklhh")
# hh.info("INFOOOOOOO")
tst.log("blblblblblb")

# logger.master_loglevel('critical')
tst.log("33333blblblblblb")
hh.info("INFO")
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
print('hh cominng')
hh.log("Logger passed the settings")
logger.master_loglevel(LoggerLevel.CRITICAL)
print('hh cominng')
hh.log("Logger passed the settings")

# logger.master_loglevel('error')
# logger.master_loglevel('error')
# bb.blas()
# # infoprint()
# nn = testclassc(bb="WWWWWW")
# nn.harrr()
# nn.haha()
# log_types = []