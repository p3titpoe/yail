import random
import string
import yail
from yail import LoggerLevel
from yail.handlers import ConsoleHandler
from threading import Thread

print(yail.handlers.console.muted_channels,1)
console_h:ConsoleHandler = yail.handlers.console
# console_h.channels['error'].mute()
print(console_h.muted_channels,2)
console_h.solo_channels(LoggerLevel.INFO)
print(console_h.muted_channels,3)
console_h.solo_channels(LoggerLevel.ERROR)
print(console_h.muted_channels,4)
console_h.solo_channels(LoggerLevel.ERROR)
print(console_h.muted_channels,5)
console_h.solo_channels()
print(console_h.muted_channels,6)


def infoprint():
    reg = yail.rootcache().registry
    log_ = [(reg[x].name, reg[x].logger.log_level) for x in yail.rootcache().booked]
    out = [f"{x[0]:<15} :: {x[1].name:<16}\n" for x in log_]
    print("".join(out))



class logTest:
    def __init__(self, loggers:int, msgs_per_logger):
        self.logd = self.create_loggers(loggers)
        self.datad = [[x._name for x in self.logd],LoggerLevel,"HELlsL",10.9887869875,13232,{v.name:v for v in LoggerLevel}]
        self.run_tests(msgs_per_logger)

    def create_loggers(self,nbr:int)->list[yail.BaseLogger]:
        length = 6
        loggers = []
        randm_level = [x for x in LoggerLevel]
        for i in range(0,nbr):
            name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            logglvl = random.choice(randm_level)
            loggers.append(yail.get_logger(name=name,loglevel=logglvl))
        return loggers

    def run_tests(self,nbr_messages:int)->None:
        func_names = [x.name.lower() for x in LoggerLevel]
        last_round = 0
        for n in range(0,nbr_messages):
            log = random.choice(self.logd)
            msglen = random.randint(10,30)
            data_val = random.randint(11,32)
            msg = ''.join(random.choices(string.ascii_letters + string.digits, k=msglen))
            func = random.choice(func_names)
            logfunc = getattr(log,func)
            params = [msg]
            if data_val%3 == 0:
                dd = random.choice(self.datad)
                params.append(dd)
            logfunc(*params)

# ltc = logTest(6,400)






# class testclassc:
#     def __init__(self, bb="WWWW"):
#         hh.info("Init Testclassc")
#         self.ar = bb
#
#     def harrr(self):
#         msg = ("This is a veryyyy loooong sentence,just to check how the it displays in the colnsole,considering allmeans."
#                ",just to check how the it displays in the colnsole,considering allmeans.")
#         hh.debug(msg)
#
#     def haha(self,v:int=2,b:int=3):
#         # fmt.conf.default_long = "loglevel name:msg"
#         hh.info(f"Result :{v*b}")
#         logger.debug("mnbmnb",{2:45,4:"tztut",0:"loki"})


# hh =logger.get_logger("OOOOO")
# tst = logger.logger_by_name('test2')
#
# # logger.master_loglevel('info')
# # # infoprint()
#
# tst.log("Log has happened")
# nn = testclassc(bb="WWWWWW")
#
# # logger.muteall()
# # logger.warning("BLAAA")
# hh.debug("trztrztrztrzt")
# hh.debug("CLASS TEST",loggger_msg_data=testclass)
# #
# logger.master_loglevel('critical')
# # # infoprint()q
# hh.error("ERRtruzpoipökjklhh")
# # hh.info("INFOOOOOOO")
# tst.log("blblblblblb")
# tst.warning("blblblblblb")
# tst.critical("blblblblblb")
# tst.debug("kljlkjlkjlkj")
# # # logger.master_loglevel('critical')
# # tst.log("33333blblblblblb")
# # hh.info("INFO")
# # # fmt = yail.formatter.Formatter("Test")
# oo = testclassb()
# bb = testclass()
# oo.blas()
# hh.log("Logger passed the settings")
# # logger.master_loglevel(LoggerLevel.CRITICAL)
# # hh.log("Logger passed the settings")
# nn.harrr()
# nn.haha()
# oo.blas()
# nn.harrr()
# nn.haha()
# oo.blas()
