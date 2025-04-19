import inspect
from .logic import LoggerLevel,LoggerMessage

class BaseLogger:
    """
        Base interactive cached Logger class

        Needs LoggerCache & Formatter, Parent should be a loggermanager
        #
        Exposes log functions for the different levels
    """
    parent: any
    _log_level: LoggerLevel
    _name:str
    _block_loglevel:bool = False
    _mute_console: bool = False
    _mute_all: bool = False
    _solo: bool = False


    def __init__(self,name:str, parent:any, log_level,block_loglevel:bool=False):
        self._log_level = log_level
        self._name = name
        self.parent = parent
        self._block_loglevel = block_loglevel

    def __base_log_functions(self, loglevel:LoggerLevel,frame:any ,info:str, data:any, external_frame:any = None):
        """
            Backend for all logging functions, eg info(), debug ()

            PARAMETERS:
                - loglevel: LoggerLevel
                - formatter: LoggerFormatter
            RETURN:
                - None
        """
        act_fram = frame
        if external_frame is not None:
            act_fram = external_frame

        # msg = self.formatter.compile(msg=info,frame=act_fram,loglevel=loglevel,data=data)
        # msg = f'{module_name}.{qual_name}'
        # print(msg)
        msg_obj = LoggerMessage(logger_name=self.name, log_level=loglevel,msg=info,frame=act_fram,data=data)
        self.__base_output_function(msg_obj)

    def __base_output_function(self,data:LoggerMessage)->None:
        self.parent.process(data)


    @property
    def log_level(self)->LoggerLevel:
        return self._log_level

    @property
    def solo(self)->bool:
        return self._solo

    @property
    def mute_all(self)->bool:
        return self._mute_all

    @property
    def console(self)->bool:
        return self._mute_console

    @property
    def name(self) -> str:
        return self._name

    @property
    def handler(self):
        return self._handler

    def log(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with self.log_level

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = self.log_level
        # frame = external_frame
        # if frame is None:
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)

    def debug(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.DEBUG
        # frame = external_frame
        # if frame is None:
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)

    def info(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.INFO
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel, frame, info, loggger_msg_data, external_frame)

    def warning(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.WARNING
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)

    def error(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.ERROR
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)

    def critical(self, info:str, loggger_msg_data:any = None, external_frame:any = None) -> None:
        """
            Convenience function to call __base_log_functions with predefinded log level.

            PARAMETER:
                - info: str = mesg to log
                - loggger_msg_data: any = Restricted to int, str, lists

            RETURNS:
                - None

        """
        loglevel = LoggerLevel.CRITICAL
        frame = inspect.currentframe().f_back
        self.__base_log_functions(loglevel,frame,info,loggger_msg_data, external_frame)
