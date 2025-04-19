import random
import string
import yail
from yail import LoggerLevel,handlers
from yail.handlers import ConsoleHandler
from threading import Thread
cnt=0
def cunt()->int:
    global cnt
    cnt += 1
    return cnt

handlers.mixer.console.solo_channels([LoggerLevel.ERROR,LoggerLevel.DEBUG])
print(handlers.handler.console.muted_channels,cunt())

class logTest:
    def __init__(self, loggers:int, msgs_per_logger):
        self.logd = self.create_loggers(loggers)
        self.datad = [[x._name for x in self.logd],LoggerLevel,"HELlsL",10.9887869875,13232,{v.name:v for v in LoggerLevel}]
        print(handlers.mixer.console.muted_channels, cunt())
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

ltc = logTest(6,40)
