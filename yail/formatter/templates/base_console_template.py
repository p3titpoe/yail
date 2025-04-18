##############################################################################
#  Template for customizing
# - Tokens are separated by semi-colon (:)
# - settings are separated by pipes (|)
# - tags and their options are separated by spaces ( )
#
##############################################################################
import os

# from yail import critical
from yail.formatter.columns import ColumnSetup

__doc__="Base Console Template"
##########################
#Default Column Setup
##########################


datecolumn = ColumnSetup(htype='date',align="l",width=0,setts=['iso'])
datacolumn = ColumnSetup(htype='data',align="l",width=0,setts=[])
linenocolumn = ColumnSetup(htype='lineno',align="l",width=10,setts=['pad4'])
loggercolumn = ColumnSetup(htype='logger',align="l",width=10,setts=['name'])
loglevelcolumn = ColumnSetup(htype='loglevel',align="l",width=10,setts=['name'])
msgcolumn = ColumnSetup(htype='msg',align="l",width=60,setts=[])
packagecolumn = ColumnSetup(htype='package',align="l",width=32,setts=['mcf',None])

columns_separator = "| "

##########################
#MESSAGE FORMATS
##########################

#You can define custom columns if you need more control
today_date = ColumnSetup(htype='date',align="c", filler=" ",width=19,setts=['today'])

default_long = [datecolumn, loggercolumn, loglevelcolumn, packagecolumn, msgcolumn]
default_short = [today_date, loggercolumn, loglevelcolumn, msgcolumn]

#DEBUG MSG
debug_package = ColumnSetup(htype='package',align="l",width=32,setts=['mcf','argsval'])
log_debug = [datecolumn, loggercolumn, loglevelcolumn, linenocolumn, debug_package,msgcolumn,datacolumn]

#INFO MSG
log_info = [today_date, loggercolumn, loglevelcolumn, linenocolumn, packagecolumn, msgcolumn]

#WARNING MSG
log_warning = [today_date, loggercolumn,  loglevelcolumn, linenocolumn, packagecolumn,msgcolumn,datacolumn]

#ERROR MSG
log_error = [datecolumn, loggercolumn, loglevelcolumn, linenocolumn, debug_package,msgcolumn,datacolumn]

#CRITICAL MSG
critical_package = ColumnSetup(htype='package',align="l",width=42,setts=['pmcf','argsval'])
log_critical = [datecolumn, loggercolumn, loglevelcolumn, linenocolumn, critical_package,msgcolumn,datacolumn]



