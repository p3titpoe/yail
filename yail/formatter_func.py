import inspect
from datetime import datetime
from yail.logic import LoggerLevel

APP_NAME ="Appname"
LOGGER_NAME ="LogName"
# TODO implement set these attribute in Loggermanager
def date_func(*args)->str:
    what = args[1]
    format = None if len(args)==2 else args[2]
    dt = datetime.now()
    out: dict = {'iso':dt.isoformat(" ",timespec='seconds'),
                 'today': dt.today().date().isoformat()
                 }
    # print(out, what)
    return out[what]

def package_func(frame:inspect.FrameInfo,*args)->str:
    library:dict = {x:"" for x in 'pmcf'}
    mod = inspect.getmodule(frame).__name__.split(".")

    # print(mod)
    library['m'] = mod[0]
    if len(mod) > 1:
        library['m'] = mod[1]
        library['p'] = mod[0]
    klasspath = frame.f_code.co_qualname.split(".")
    if len(klasspath)==2:
        library['c'] = klasspath[0]
    library['f'] = package_func_functions(frame,args[1])
    out:str = ""
    for x in args[0]:
        out += f"{library[x]}."
    out = out[:-1]
    return out
def package_func_functions(frame, show:str)->str:
    nn =frame.f_code.co_name
    argsval:dict = {}
    fname:str = ""
    out:str = ""
    if nn[0] not in ["","_","<"]:
            fname = nn
            args = inspect.getargs(frame.f_code)
            for arg in args.args:
                val = frame.f_locals[arg]
                if arg != 'self':
                    argsval[arg]= val
    if show == "":
        return f"{fname}"
    out_arg="-"
    if show == 'args':
        out_arg = ",".join([x for x in argsval.keys()])
    if show == 'argsval':
        tmp = [f"{k} = {v}" for k,v in argsval.items()]
        out_arg = ",".join(tmp)

    out += f"{fname}("
    return f"{fname}({out_arg})"
    pass

def msg_func(*args)->str:
    return args[0]

def data_func(data:any):
    pass

def loglevel_func(level:LoggerLevel,what:str)->str:
    out:dict ={'name':level.name,
               'value':level.value
               }
    return out[what]
def lineno_func(frame:inspect.FrameInfo,*args):
    linenr = frame.f_lineno
    mr = args[0].split('pad')
    nr = 0 if len(mr) != 2 else mr[1]
    fmt =f"{linenr}"
    if nr != 0:
        sett =f"0{nr}d"
        fmt =f"{linenr:0{nr}d}"
    return fmt


def logger_func(data:str,name:str)->str:
    return data
