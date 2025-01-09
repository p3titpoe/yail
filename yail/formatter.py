import re
import inspect
from datetime import datetime
from enum import Enum
from dataclasses import dataclass,field
from yail.logic import LoggerLevel, Registry

def iso_date(dummy:str)->str:
    # return datetime.isoformat("YYYY-MM-DD HH:MM:SS")
    dt = datetime.now()
    return dt.isoformat("-",timespec='seconds')
    # return dt.today().date().isoformat()

def today(dummy:str)->str:
    dt = datetime.now()
    return dt.today().date().isoformat()

    pass
def __makesplit(data:inspect.FrameInfo,who:int):
    tosplt = data.f_code.co_qualname
    out=False
    if "." in tosplt:
        sp = tosplt.split(".")
        out = sp[who]
    return out

def package(tosplit:inspect.FrameInfo)->str:
    txt = tosplit
    if "." in tosplit:
        txt =__makesplit(tosplit,0)
    return txt

def moduul(data:inspect.FrameInfo)->str:
    name = inspect.getmodule(data).__name__
    if name == "__main__":
        name ="root"
    return name


def klass(tosplit:inspect.FrameInfo)->str:
    nn = __makesplit(tosplit,0)
    if not nn:
        nn = ""
    return nn

def func(data:inspect.FrameInfo,showargs=False,showargsval=False)->str:
    nn =data.f_code.co_name
    out:str = ""
    if nn[0] not in ["","_","<"]:
        out += f"{nn}("
        if showargs:
            args = inspect.getargs(data.f_code)
            for arg in args.args:
                val = data.f_locals[arg]
                if arg != 'self':
                    out += f"{arg}"
                    if showargsval:
                        out += f" = {data2str(data.f_locals[arg])}"
                    out += ","
            out = out[:-1]
        out += ")"
    return out

def func_args(data:inspect.FrameInfo)->str:
    return func(data=data,showargs=True)
def func_argsval(data:inspect.FrameInfo)->str:
    return func(data=data,showargs=True,showargsval=True)

def msg(inp:str)->str:
    return inp

def data2str(data:any)->str:

    def datastr(data:list)->str:
        return data[0]
    def dataint(data:list)->str:
        return f"{data[0]}"

    def datalist(data:list)->str:
        txt = f""
        # print("DADA ::",data)
        str_data = [str(x) for x in data[0]]
        lst = f",".join(str_data)
        txt += f'{str(str_data):>10}'
        return txt

    def datadict(data:list)->str:
        # txt = f"\n"
        max_field_len=10
        full_fields = False
        first_line_same = False
        first = True
        txt = f"" if first_line_same else f"\n"
        for k,v in data[0].items():
            line: str = data[1]
            val = str(v)
            if first:
                if first_line_same:
                    line = line.replace(" ","")
                first = False
            if full_fields:
                max_field_len = len(val)
            val = val[:max_field_len]
            if not full_fields and len(val)>=max_field_len:
                val += "..."
            itr = [("key",k),("val",val)]
            for x in itr:
                line = replace_tag_in_format(line,x[0],x[1])
            txt += line
        return txt[:-1]

    def datanone(data:any)->str:
        name = ""
        if data is not None:
            name = f"{data[0].__class__.__name__.__repr__()}"
            # print(name,data)
        return name

    map:dict ={
        int:dataint,
        str:datastr,
        list:datalist,
        dict:datadict,
        'none':datanone
    }
    if data[0] == None or data is not isinstance(data,l):
        return ""
    else:
        typ = type(data[0])
        if typ in map:
            func_to_call  = map[typ]
        else:
            func_to_call = map['none']
        return func_to_call(data)

def loglevel2str(data:LoggerLevel)->str:
    out = str(data.name)
    return out
def loglevel2val(data:LoggerLevel)->str:
    out = str(data.value)
    return out
    #
def lineno(data:inspect.FrameInfo)->str:
    return str(data.f_lineno)

class FormTags(Enum):
    ISODATE = iso_date
    TODAY = today
    PACKAGE = package
    MODULE = moduul
    CLASS = klass
    FUNCTION = func
    FUNCTION_ARGS = func_args
    FUNCTION_ARGSVAL = func_argsval
    MSG = msg
    DATA = data2str
    LOGLEVEL = loglevel2str
    LOGLEVEL_NAME = loglevel2str
    LOGLEVEL_VALUE = loglevel2val
    LINENO = lineno

    @classmethod
    def by_name(cls, name: str):
        att = getattr(cls, name)
        return att

def replace_tag_in_format(form:str, tag:str, repl: str)->str:
    tosearch = f"<<{tag}>>"
    if tosearch in form:
        form = form.replace(tosearch, repl)
    return form

def replace_taglist_in_format(form:str,data:dict)->str:
    for k,v in data.items():
        form = replace_tag_in_format(form,k,v)
    return form

def get_tags(form:str) -> list:
    re_blob = re.compile('<<([a-z]+ ?[a-z]+)>>')
    # re_blob = re.compile('<<([a-z]+ [a-z]+)>>')
    out =  re.findall(re_blob,form)
    return out

ccc=">12"
@dataclass
class FormatterTag:
    """
        Holds the format & stringed data and is
        responsible for proper output of the f"" string

    .. note::
        If replace is longer than column it is truncated

    Accpetable values for align:
        - l = left
        - c = centered
        - r = right
    """

    name:str
    replace: str = ""
    align: str ="l"
    _column_width: int = 0
    _fixed: bool = True
    _fmt: str = ""
    _is_to_long:bool = False
    _filler_len:int = 0
    _filler = " "
    _align_dict = {'l':'<',
                   'c': '<',
                   'r': '<'
                   }
    cnt:int = 0
    def __post_init__(self):
        self._check_if_to_long()


    def _check_if_to_long(self)->None:
        """
            Sets the appropriate flag for compiling output
        """
        repl_len = len(self.replace)
        if  repl_len > self.column_width:
            self._is_to_long = True
        else:
            self._filler_len = self.column_width - repl_len
            self._is_to_long = False
        self._fixed = False if self.column_width == 0 else True
        # print(self._is_to_long," .... ", repl_len,self.column_width)


    @property
    def fmt(self)->str:
        return self._fmt

    @property
    def column_width(self)->int:
        return self._column_width

    def set_column_width(self,width:int)->None:
        self._column_width = width
        self._check_if_to_long()

    def set_fmt(self,fmt:str)->None:
        self._fmt = fmt

    def compile(self)->str:
        fmt: str =""
        if self._fixed:
            # print(f"Compile :: {self._fixed}")
            if self._is_to_long:
                # print(f"Compile :: is too long {self._is_to_long}")

                fmt = f"{self.replace:.{self.column_width}}"
                # fmt = f"{self.replace:.4}"
            if self.replace != "" and not self._is_to_long:
                # print(f"Compile :: Not too long")

                align_str = self._align_dict[self.align]
                # padding = self._filler+align_str+self._filler_len
                fmt = f"{self.replace:{self._filler}{align_str}{self._filler_len}}"
                # print(fmt)
        else:
            # print(f"Compile :: Else close")

            fmt = f"{self.replace}"

        return fmt


@dataclass
class FormatterConfig:
    """
        Holds the formats for loglevel
    """
    module_separator: str = "."
    columns_separator: str = "::"
    default_active:list = field(init=False,default_factory=list)
    default_short:list = field(init=False,default_factory=list)
    default_long:list = field(init=False,default_factory=list)

    log_debug:list = field(init=False,default_factory=list)
    log_info:list = field(init=False,default_factory=list)
    log_warning:list = field(init=False,default_factory=list)
    log_error:list = field(init=False,default_factory=list)
    log_critical:list = field(init=False,default_factory=list)
    log_fatal:list = field(init=False,default_factory=list)

    _package_mebers: list = field(init=False, default_factory=list)
    def __post_init__(self):
        self.default_active = []
        self.default_short = ['date today','loggername','loglevel','module','function','msg']
        self.default_long = ['isodate','loggername','loglevel','module','class','function','msg']

        self.log_debug = ['date isodate','loggername','loglevel','module','class','function','lineno','msg','data']
        self.log_info = self.default_long
        self.log_warning = self.default_long
        self.log_error = self.default_long
        self.log_critical = self.default_long
        self.log_fatal = self.default_long
        self._package_members = ['package','module','class','function']

    @property
    def package_members(self)->list:
        return self._package_members


@dataclass
class Formatter:
    """
        Formats the log string

    .. note::
        This needs refactoring to accomodate for a column aproached structure of the messages.

        The idea is to pass a dicr as structre and to build it from there instead like now,
        definig the string and fiddle with it.

        The dict should be structured like this

            name_of_option : length of the column
            ("loglevel value":40,)

        How to:
            Uselful formats

            .. code::

                f"{tag:>10}" # left align 10
                f"{tag:<10}" # right align 10
                f"{tag:^10}" # centered 10
                f"{tag:.10}" # truncated

            Code

            .. code::
               :linenos:

                tag = "loglevel value"
                col_len = structure[tag]
                tag = tag.replace(" ","_") # Conversion to underscore as writing with space is more convenient
                func = FormTags.by_name(tag.upper())
                res = func(data) #fetch the data

            Almost same, then

            .. code::

                res_len = len(res)   #check how long the str is
                len_diff = col_len - res_len    #get the len diff between str & col
                if len_diff >= 0:
                    tag_option = f">{len_diff}"
                else:
                    tag_option = f".{col_len}"

                txt = f"{tag:{tag_option}}"

        Also, the formatter should have a .. ::py:class: logic.Registry as to implement different layouts for the different
        .. ::py:class: logic.LoggerLevel


    """
    logger_name:str
    _conf: FormatterConfig = field(default_factory=FormatterConfig)
    _active_format:str = 'long'
    _format_short:str =(f"<<today>>::<<loggername>>::<<loglevel value>>::<<lineno>> - <<function>>::<<msg>>::<<data>>")
    _format_long:str =(f"<<isodate>>::<<loggername>>:: <<lineno>> ::<<loglevel>>:<<module>>.<<class>>.<<function>>::<<msg>>")
    _format_datadict=(f"DATA::<<function>>::<<key>>::<<val>>\n")
    _tags:dict = field(default_factory=dict)
    _short:bool = False
    _show_data:bool = True

    def __post_init__(self):
        self._active_format = self._format_long if not self._short else self._format_short
        self._active_format = replace_tag_in_format(self._active_format,'loggername',self.logger_name)
    def _check_tags(self,taglist: list)->dict:
        """
            Convert tag list from format to a dict with tag : Formtag.

            This is a convenience to let the user use a more lexical style for formats, like <<loglevel value>>

        """
        out:dict = {}
        for tag in taglist:
            option=""
            #check for options, delimiter is Whtespace
            if " " in tag:
                option = tag.replace(" ", "_")
            else:
                option = tag
            out[tag] = option.upper()
        return out
    @property
    def format(self)->str:
        return self._active_format
    def toggle_short_format(self)->str:
        """
            Toggles sgort format on / off
        """
        # sw = False
        # if not self._short:
        #     sw = True
        self._short = True if not self._short else False
        self._active_format = self._format_long if not self._short else self._format_short

        return self._short

    def toggle_data(self)->bool:
        self._show_data = True if not self._show_data else False
        return self._show_data

    def seek_and_replace_taglist_in_format(self,form:str,data:dict)->str:
        taglist = self.get_tags()
        for tag in taglist:
            if tag in data:
                form = replace_tag_in_format(form,tag,data[tag])
        return form

    def get_tags(self,form:str = None) -> list:
        fmt = form
        if fmt is None:
            fmt =self.format
        out = get_tags(fmt)
        return out
    def replace_format(self,which:str,fmt:str)->None:
        """
            Replace one of the format strings

            allowd for which are
            long, short, datadict
        """
        allowed = ["long", "short", "datadict"]
        if which in allowed:
            setattr(self,f"_format_{which}",fmt)
            setattr(self,f"_active_format",fmt)
            self._active_format = replace_tag_in_format(self._active_format, 'loggername', self.logger_name)


    def compile_new(self,msg: str,frame:any, loglevel:LoggerLevel, data=None )->str:
        form = self.get_tags()
        conf = self._conf
        form = conf.default_long
        form_tags = self._check_tags(form)
        out=""
        for tag in form:
            if tag != 'loggername':
                f = tag.split(" ")[0] if len(tag.split(" ")) == 2 else tag
                func = FormTags.by_name(form_tags[tag])
                form_data = frame
                if f == "msg":
                    form_data = msg
                elif "loglevel" in f:
                    form_data = loglevel
                else:
                    form_data = frame
                res = func(form_data)
                # print(res)
                composite = FormatterTag(tag,res)

            else:
                composite = FormatterTag(tag,self.logger_name)

            # print(composite)
            if tag not in self._conf.package_members:
                composite.set_column_width(10)

            # print(composite)
            sep = self._conf.columns_separator
            if tag in self._conf.package_members:
                sep = self._conf.module_separator
            if tag =='loglevel':
                print(composite)
            tmp = f"{composite.compile()}{sep}"
            out += tmp

        return out






    def compile(self,msg: str,frame:any, loglevel:LoggerLevel, data=None )->str:
        out_msg = ""
        # composite=self.format
        form = self.get_tags()
        # if not self._show_data:
        #     form.remove('data')
        #     composite = composite[:-8]

        form_tags = self._check_tags(form)

        for tag in form:
            res:str = ""
            f = tag.split(" ")[0] if len(tag.split(" ")) == 2 else tag
            func = FormTags.by_name(form_tags[tag])
            form_data = frame
            if f == "msg":
                form_data = msg

            elif f == "data":
                # sp = composite.split("::")
                cnt = []
                limit = -2 if not self._short else -1
                # cnt.extend([" " for x in range(len(composite)-2)])
                spacer = "".join(cnt[:-6])
                fmt = replace_tag_in_format(self._format_datadict,'function',FormTags.FUNCTION(frame))
                # print("FFFFF",FormTags.FUNCTION(frame))
                # print("FFFFF",fmt)
                ff = f"{spacer}{fmt}"
                form_data=[data,ff]

            elif "loglevel" in f:
                form_data = loglevel
            else:
                form_data = frame
            # if f != data:
            res = func(form_data)
            # print(res)
            composite = FormatterTag(tag,res)

            # print(res)
            # composite = replace_tag_in_format(composite,tag,res)


        return  composite