import random
import string
import yail
from yail import LoggerLevel,LoggerStack,handlers,BaseLogger
from threading import Thread
import yail.signaling as sig

cnt=0
def cunt()->int:
    global cnt
    cnt += 1
    # print(cnt)
    return cnt

print(yail.stacks.rootcache.cache_entry_by_name('-root-'))
# yail.handlers.handler.console.m
class logTest:
    def __init__(self, loggers:int, msgs_per_logger:int, break_points:dict):
        self.logd = self.create_loggers(loggers)
        self.datad = [[x._name for x in self.logd],LoggerLevel,"HELlsL",10.9887869875,13232,{v.name:v for v in LoggerLevel}]
        self.breakpoints = break_points
        # print(handlers.mixer.console.muted_channels, cunt())
        self.run_tests(msgs_per_logger)

    def create_loggers(self,nbr:int)->list[yail.BaseLogger]:
        length = 6
        loggers = []
        randm_level = [x for x in LoggerLevel]
        rndm_public =[True,False]
        for i in range(0,nbr):
            # name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            name = f"Test-{i}"
            logglvl = random.choice(randm_level)
            public = random.choice(rndm_public)
            loggers.append(yail.get_logger(name=name,loglevel=logglvl,public=public))
            print()
        return loggers

    def run_tests(self,nbr_messages:int)->None:
        breakpoints = self.breakpoints


        func_names = [x.name.lower() for x in LoggerLevel]
        last_round = 0
        for n in range(0,nbr_messages):
            if n in breakpoints:
                yail.critical(f"BReakpont {n}")
                fc = breakpoints[n][0]
                fcd = breakpoints[n][1]
                fc(fcd)
            log = random.choice(self.logd)
            msglen = random.randint(10,30)
            data_val = random.randint(11,32)
            msg = ''.join(random.choices(string.ascii_letters + string.digits, k=msglen))
            msg += f" ---cunt{cunt()}"
            func = random.choice(func_names)
            logfunc = getattr(log,func)
            params = [msg]
            if data_val%3 == 0:
                dd = random.choice(self.datad)
                params.append(dd)
            logfunc(*params)
breakp={50:[handlers.handler.console.mixer.solo_channels,
          [LoggerLevel.DEBUG]],
        90: [handlers.handler.console.mixer.solo_channels,
            [LoggerLevel.ERROR]],
        90: [handlers.handler.console.mixer.solo_channels,
            []],
        140: [handlers.handler.console.mixer.solo_channels,
             [LoggerLevel.CRITICAL]],
        200: [handlers.handler.console.mixer.mute_channels,
            [LoggerLevel.CRITICAL,LoggerLevel.WARNING]],
        }


ltc = logTest(6,300,breakp)
