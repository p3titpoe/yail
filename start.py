import yail as logger
from testing.models import testclass,testclassb

hh =logger.get_logger("OOOOO")

bb = logger.get_logger('Test')
tst = testclass()
tst2 = testclassb()
logger.warning("Logger will stop output to console")
tt2 = logger.logger_by_name('test3')
# print("TEST2 ", tt2.cache.booked)
tst2.blas(3,4)
tt2.info("well Then..")
# print("TEST2 ", tt2.cache.booked)
def fr():
    logger.info("Who is this")
fr()
logger.sip('test3')
# logger.info("Logger stopped processind")
logger.info("Rootlogger is still working")
hh.info("Other logger")
# # for k,x in logger.LOGGER.rootcache.registry.items():
# #     if x is not None:
# #         print("Main Logger",k,"  ",x.name)
tst2.blas(5, 5)
# print("TEST2 ", tt2.cache.booked)
# print("TEST2 ", tt2.mute_all,tt2.console)
#
cc = logger.logger_by_name("test3")
cc.warning("Switched to another module")
# logger.muteoff()
cc.critical("This is  printing")
hh.info("I'm here!!")

#
# class testclassc:
#     def __init__(self, bb="WWWW"):
#         self.ar = bb
#         cc.debug("Init Testclassc")
#
#
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