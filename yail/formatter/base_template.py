##############################################################################
#  Template for customizing
# - Tokens are separated by semi-colon (:)
# - settings are separated by pipes (|)
# - tags and their options are separated by spaces ( )
#
##############################################################################
import os

path_to_file = os.path.abspath(__file__)
print(path_to_file)
msg_length:int = 180
logger_name_length:int = 8

default_long: str = f"date iso:logger name|8 c:loglevel name|8:package mcf args|33 l:msg|{msg_length}"
default_short: str = f"date today|26:logger name|20:loglevel name|10"

log_debug: str = f"date iso:logger name|8 c:loglevel name|8:lineno pad4|13 c:package mcf argsval|38 l:msg|{msg_length}:data"
log_info: str = f"date iso:logger name|8 c:loglevel name|8:package mcf args|33 l:msg|{msg_length}"
log_warning: str = f"date iso:logger name|8 c:loglevel name|8:package mcf args|33 l:msg|{msg_length}"
log_error: str = f"date iso:logger name|8 c:loglevel name|8:lineno pad4|13 c:package mcf args|33 l:msg|{msg_length}"
log_critical: str = f"date iso:logger name|8 c:loglevel name|8:lineno pad4|13 c:package mcf argsval|33 l:msg|{msg_length}"
log_fatal: str = f"date iso:logger name|8 c:loglevel name|8:lineno pad4|13 c:package mcf argsval|33 l:msg|{msg_length}"
