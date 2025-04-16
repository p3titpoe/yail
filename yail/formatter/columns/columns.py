import inspect
from datetime import datetime
from dataclasses import dataclass,field
from yail.logic import LoggerMessage, LoggerLevel
from enum import Enum

class InnerColumnType(Enum):
    DATE = 'date'
    PACKAGE = "package"
    MSG = "msg"
    LOGLEVEL = 'loglevel'
    LINENO = 'lineno'
    DATA = 'data'
    LOGGER = 'logger'

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att

@dataclass(repr=False)
class ColumnSetup:
    htype:str = None
    align:str = "c"
    width:int = 0  #if zero, the width is dynamc
    setts:list = field(default_factory=list)
    filler:str = " "
    fill_space = False

    def __repr__(self):
        txt=f"ColumnSetUp\n"
        txt +="-"*len(txt)
        txt += "\n"
        for k,v in self.__dict__.items():
            txt += f"{k} : {v} \n"
        return txt

@dataclass(init=False)
class BaseColumn:
    _htype:InnerColumnType = None
    _width:int = 0
    _align:str = "l"
    _filler:str = ""
    _fill_space = False
    _fixed:bool = True
    _setts:list = None
    _align_dict = {'l': '<',
                   'c': '^',
                   'r': '>'
                   }

    def __init__(self,sp:ColumnSetup):
        self._htype = InnerColumnType.by_name(sp.htype.upper())
        self._width = sp.width
        self._align = sp.align
        self._filler = sp.filler
        self._fill_space = sp.fill_space
        self._setts = sp.setts
        if sp.width == 0:
            self._fixed=False
        else:
            self._width = sp.width
            self._fixed = True

        self.__post_init__()

    def __repr__(self):
        txt=f"{self._htype.name.capitalize()}Column\n"
        txt +="-"*len(txt)
        txt += "\n"
        for k,v in self.__dict__.items():
            txt += f"{k} : {v} \n"
        return txt

    def __post_init__(self):
        """
        """

    def _white_spacer(self,content:str)->str:
        wrest = self._width - len(content)
        left = ""
        right = ""
        lib = {'l':left,
               'r':right,
               'c':[left,right],
               }
        if self._align != "c":
            lst = lib[self._align]
            lst = " "*wrest

        if self._align == "c":
            l = round(wrest/2)
            ends = [l,wrest-l]
            for i,sides in lib[self._align]:
                sides = self._filler*ends[i]

        return f"{left}{content}{right}"

    def _f_spacer(self,content:str):
        out = f"{content}"
        fix = ""
        if self._fixed:
            endl = f"{self._align_dict[self._align]}{str(self._width)}"
            fix = f"{out:{endl}}"
        return fix


    def compile(self,content:str)->str:
        """
        Compiles the given class and content to a string

        PARAMETERS:
            - content(str)

        RETURNS:
            - str


        """
        len_c = len(content)
        trunc = "..."
        tmp  = content

        lib = { True: self._white_spacer,
                False:self._f_spacer
        }
        if self._fixed and len_c > self._width:
            tmp = content[:self._width+len(trunc)]
            tmp += trunc

        fc = lib[self._fill_space]
        out = fc(content=tmp)
        if out == "":
            print("KKKKK:: ", out, self._htype)

        return out


    def process(self,lm:LoggerMessage)->str:
        """
            Process the class with given LoggerMessage
            Calls Setup First

            .. warning::
               Must be overwritten by Kids
               Must implement the compile function!
        """
        content = "No Content"
        return self.compile(content=content)


@dataclass(init=False)
class DateColumn(BaseColumn):
    def __init__(self,sp:ColumnSetup):
        super().__init__(sp=sp)

        self.iso_separator:str = " "
        self.iso_timespecs:str = 'seconds'
        self.custom_format:str = None
        self.timezone:str = None
        self._dt:datetime = None

        self._dt = datetime.now()

    def isodate(self)->str:
        return  self._dt.isoformat(sep=self.iso_separator,timespec=self.iso_timespecs)

    def today(self)->str:
        return  self._dt.today().date().isoformat()

    def custom(self)->str:
        """
            Needs a format like :
            "%a, %d %b %Y %H:%M:%S" = Mon, 14 Apr 2025 19:14:23
            "%H:%M:%S::%A, %d %b %Y" =  19:16:44::Monday, 14 Apr 2025
            "%H:%M:%S::%d-%m-%Y" = 19:19:56::14-04-2025

        """
        return self._dt.strftime(self.custom_format)

    def process(self,lm:LoggerMessage)->str:
        possibles = {'iso': self.isodate,
                     'today':self.today,
                     'cstm':self.custom}

        content = possibles[self._setts[0]]()
        print("CONTENT ::DATECOLUMN", content)
        return self.compile(content)

@dataclass(init=False)
class LoggerColumn(BaseColumn):
    def __init__(self,sp:ColumnSetup):
        super().__init__(sp=sp)

    def process(self,lm:LoggerMessage)->str:
        return self.compile(lm.logger_name)

@dataclass(init=False)
class DataColumn(BaseColumn):
    def __init__(self,sp:ColumnSetup):
        super().__init__(sp=sp)

    def process(self,lm:LoggerMessage)->str:
        # return self.compile(lm.data)
        return "OVERIDDWEN IN DATACOLUMN"

@dataclass(init=False)
class LinenoColumn(BaseColumn):
    def __init__(self,sp:ColumnSetup):
        super().__init__(sp=sp)

    def process(self,lm:LoggerMessage)->str:
        frame = lm.frame
        linenr = frame.f_lineno
        mr =self._setts[0].split('pad')
        nr = 0 if len(mr) != 2 else mr[1]
        fmt = f"{linenr}"
        if nr != 0:
            sett = f"0{nr}d"
            fmt = f"line {linenr:0{nr}d}"
        return self.compile(fmt)

@dataclass(init=False)
class LoglevelColumn(BaseColumn):
    def __init__(self,sp:ColumnSetup):
        super().__init__(sp=sp)

    def process(self,lm:LoggerMessage)->str:
        level:LoggerLevel = lm.log_level
        lib = {'name':level.name,
               'value':level.value
               }
        return self.compile(lib[self._setts[0]])

@dataclass(init=False)
class MsgColumn(BaseColumn):
    def __init__(self,sp:ColumnSetup):
        super().__init__(sp=sp)

    def process(self,lm:LoggerMessage)->str:
        return self.compile(lm.msg)

@dataclass(init=False)
class PackageColumn(BaseColumn):
    def __init__(self,sp:ColumnSetup):
        super().__init__(sp=sp)

    def package(self,frame:inspect.FrameInfo,lib:dict)->dict[str:str]:
        mod = inspect.getmodule(frame).__name__.split(".")
        wanted_keys = [k for k in lib.keys()]
        for k,v in lib.items():
            if k == 'm':
                lib[k] = mod[0]

                if len(mod) > 1:
                    lib[k] = mod[1]

            if k == 'p':
                lib[k] = mod[0] if len(mod) > 1 else ""

            if k == 'c':
                klasspath = frame.f_code.co_qualname.split(".")
                if len(klasspath)==2:
                    lib[k] = klasspath[0]

        return lib

    def package_function(self,frame) -> str:
        nn = frame.f_code.co_name
        show = self._setts[1]
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

        return f"{fname}({out_arg})"

    def process(self,lm:LoggerMessage)->str:
        library: dict = {x: "" for x in self._setts[0]}
        library = self.package(lm.frame,library)
        if 'f' in library:
            library['f'] = self.package_function(lm.frame)

        out: str = ""
        for x in self._setts[0]:
            out += f"{library[x]}."
        out = out[:-1]
        return self.compile(out)

