"""Handlers for logs, providing a shorthand for `logging` module."""
import logging
import sys

from . import utils
from . import journal

utils.ensure_dir(utils.log_dir)

class LogHandler(object):
    """Class to handler logs."""
    
    def __init__(
        self,
        name="Main",
        save=False, echo=True,
        msg="{asctime} {levelname:8} @{lineno:3}: {message}", level=logging.DEBUG,
        fmt="{dire}{debug}Log-{date}{second}-{ctr:03}.log",
        log=print,
    ):
        """Initialize a log handler."""
        
        self.title = name
        self.save, self.echo = save, echo
        self.fmtr, self.level = logging.Formatter(msg, style="{"), level
        self.fmt = fmt
        if "redirect".startswith(log):
            self.log = self
        else:
            self.log = log
        
        self.ctr = 0
        self.name = utils.name_function
    
    def __call__(self, *args, **kwargs):
        """Wrapper to `logger.info(...)` for shorthand."""
        self.logger.info(*args, **kwargs)
    
    def new_logger(self, info="### Remember to leave description message here ###"):
        """Initialize a logger."""
        
        self.logger = logging.getLogger(self.title)
        
        if self.echo:
            self.con_hdl = logging.StreamHandler(sys.stdout)
            self.con_hdl.setFormatter(self.fmtr)
            self.logger.addHandler(self.con_hdl)
        
        if self.save:
            filename = self.name(self.fmt, self.ctr, utils.log_dir)
            self.file_hdl = logging.FileHandler(filename)
            self.file_hdl.setFormatter(self.fmtr)
            self.logger.addHandler(self.file_hdl)
        
        self.logger.setLevel(self.level)
    
        if self.log is not None:
            if self.save:
                self.log("Log {} opened".format(filename))
            journal.logger.info("OPEN: Log {}".format(filename))
            self.log("Logger started...")
        
        if info is not None:
            self.log(info)
        
    def close_logger(self):
        """Terminate logging and remove formatters."""
        
        if self.log is not None:
            self.log("Terminating logger...")
        
        if self.echo:
            self.logger.removeHandler(self.con_hdl)
        
        if self.save:
            self.logger.removeHandler(self.file_hdl)
