import os
import pprint as pp
import tempfile

from casatools import logsink
from casatasks import casalog   

# <- the default logsink instance casatask uses
#   not logfile after the initallization of casalog 
os.system('rm -rf '+casalog.logfile())
casalog.setlogfile('/dev/null')

import logging

logger = logging.getLogger('ism3d')

def logger_config(logfile=None,
                  loglevel='INFO', logfilelevel='INFO',
                  reset=True):
    """
    set up a customized logger,e.g.,
        >>>ism3d.logger_config(logfile='logs/test_ism3d.log',
                loglevel=logging.WARNING,
                logfilelevel=logging.INFO)
    note: this will merge the logging output from ism3d and casa6 into a single log file.
    loglevel='INFO'/'WARN'/'DEBUG'
    """

    if reset:
        logger.handlers = []

    # note: we don't touch the root logger level here
    logger.setLevel(logging.DEBUG)

    #   file logging handler

    if logfile is not None:
        logdir = os.path.dirname(logfile)
        if (not os.path.exists(logdir)) and (logdir != ''):
            os.makedirs(logdir)
        logfile_handler = logging.FileHandler(logfile, mode='a')
        #format="%(asctime)s "+"{:<40}".format("%(name)s.%(funcName)s")+" [%(levelname)s] ::: %(message)s"
        # logfile_formatter=MultilineFormatter(format)
        logfile_formatter = CustomFormatter()
        logfile_handler.setFormatter(logfile_formatter)
        logfile_handler.setLevel(logfilelevel)
        logger.addHandler(logfile_handler)

    #   console logging handleris

    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    # console_formatter=CustomFormatter()
    # console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    #   config casa logsink
    #   https://casa.nrao.edu/docs/CasaRef/logsink-Tool.html#logsink.version.html
    #   https://casa.nrao.edu/Release3.3.0/docs/UserMan/UserMansu43.html

    casalogger_config(logfile=logfile,loglevel=loglevel,onconsole=True)
    
    return

def casalogger_config(logfile=None,loglevel='INFO',onconsole=True,
                      reset=False):
    """
    Set CASA log file
    use reset=True when you don't want the last casa log file (which could be autmatically created when import casataks)
    """
    if  logfile is None:
        #fd, casalogfile= tempfile.mkstemp(suffix='.log')
        casalogfile='/dev/null'   
    else:
        casalogfile=logfile
        
    if  reset==True:
        if  'null' not in casalog.logfile():
            os.system('rm -rf '+casalog.logfile())
     
    casalog.setlogfile(casalogfile)
    casalog.showconsole(onconsole=onconsole)
    casalog.filter(loglevel)
    
    return

def casalogsink_config(logfile=None,loglevel='INFO',onconsole=True):
    """
    obselete
    casatools.logsink can create a casalogger instance
    import casatasks will initialize a casalogger instance
    the casa logger setup will be initilized with "import casataks"
    
    to prevent this, we need the casalogger configuration at the toolkit ahead of
    import casatasks  
    """
    if logfile is None:
        fd, logfile = tempfile.mkstemp(suffix='.log')
    # site-packages/casatools/__casac__/logsink.py
    casalogger = logsink(filename=logfile, enable_telemetry=False)
    casalogger.showconsole(onconsole=True)
    casalogger.filter(loglevel)
    
    return    
    

def logger_status():
    """
    print out the current status of ism3d logger
    """
    logger.info("\n-- ism3d logger:\n")
    logger.info(logging.getLogger('ism3d'))
    logger.info(logging.getLogger('ism3d').handlers)
    
    logger.info('\n-- casa logger:\n')
    logger.info(casalog.logfile())
        
    logger.info("\n-- root logger:\n")
    logger.info(pp.pformat(logging.Logger.manager.loggerDict))

    return


class CustomFormatter(logging.Formatter):
    """
    customized logging formatter which can handle mutiple-line msgs
    """
    def format(self, record: logging.LogRecord):
        save_msg = record.msg
        output = []
        datefmt = '%Y-%m-%d %H:%M:%S'
        s = "{} :: {:<32} :: {:<8} :: ".format(self.formatTime(record, datefmt),
                                               record.name+'.'+record.funcName,
                                               "[" + record.levelname + "]")
        for line in save_msg.splitlines():
            record.msg = line
            output.append(s+line)

        output = '\n'.join(output)
        record.msg = save_msg
        record.message = output

        return output