import inspect

import testing.nested.nested
import yail as logger
import yail.formatter
from yail.logic import LoggerLevel,LoggerMessage
from testing.models import testclass,testclassb
from testing.nested.innernested.blested import  nestedclass

hh =logger.get_logger("OOOOO")

fmt = yail.formatter.Formatter("Test")
oo = testclassb()
class testclassc:
    def __init__(self, bb="WWWW"):
        self.ar = bb
        # cc.debug("Init Testclassc")

    def harrr(self):
        msg = "This is a veryyyy loooong sentence,just to check how the it displays in the colnsole,considering allmeans."
        return fmt.compile_new(msg, inspect.currentframe(), LoggerLevel.DEBUG)
    def haha(self):
        # fmt.conf.default_long = "loglevel name:msg"
        return fmt.compile_new("Vlasr", inspect.currentframe(), LoggerLevel.WARNING)

nn = testclassc()

def testfunc()->any:
    return fmt.compile_new("TEST",inspect.currentframe(),LoggerLevel.DEBUG)

# for x in range (0,1):
vv = testing.nested.nested.nestedclass()
ll = testing.nested.innernested.blested.nestedclass()
mm = testfunc()
ddd = nestedclass()
print(mm)
print(nn.harrr())
print(nn.haha())
print(oo.blas(8,8))
print(yail.formatter.tstfunc())
print(vv.nestedBlas(3,3,3))
# print(nestedclass.nestedBlas(2,2,2))
# print(f"{mm.compile()},mm")|____



#
#LOGGGER TESTING

# logger.debug("restarting processing")
# logger.muteoff()
# ff = testclassc()

# print([x for k,x in logger.LOGGER._root_cache.registry.items()])
# # cash = LoggerCache(max_len=30, parent_cache=central)
# log = BaseLogger("MAin",central,LoggerLevel.INFO)
# # log.toggle_short()
# log.debug("Frist module",[1,22,33,44])
# tst.blas(3,3)
# # log.debug("Is this working",tst.blas(5,8))
# # tst2 = testclassb()
# log.debug("Big Test",{'fast':'food',
#                                   'kkk':[1,2,3,4],
#                                   'mmm':{'bim':'bam','ff':'gg'}
#                         })
#
# # print(cash)
# log.toggle_data()
# def muuuh(c:Central):
#     log.debug("First Muuh")
#
#
#     log.debug("Big ewwweewe", {'fast': 'food',
#                            'kkk': [1, 2, 3, 4],
#                            'mmm': {'bim': 'bam', 'ff': 'gg'}
#                            })
#
#
# def meeeeh():
#     log.debug("First Meeh")

#     log.formatter.toggle_short_format()
#     log.warning("Warning Muh")
#     tst2.bl.as(3,3)
# muuuh(central.jt_wmc)
# meeeeh()
# class blsa:
#     logg = BaseLogger('second',central,LoggerLevel.INFO)
#     def __init__(self):
#        self.logg.debug("BBBBBBBBBBBBB")
#
#     def mmm(self):
#         log.warning("********")
# # log.info("*******")
# nn = blsa()
# nn.mmm()
#