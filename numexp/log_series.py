# log_series.py
"""Class for log series, using `logging` modulue"""
import logging
import sys

from .utils import default_filename_generator

default_formatter = logging.Formatter(
    "{asctime} {levelname:8} @ {lineno:3}: {message}", style="{"
)


class LogSeries(object):
    """Class for a series of logs."""

    def __init__(
        self,
        name, formatter=default_formatter, level=logging.DEBUG,
        echo=True, save=False,
        logs=print, generator=".log",
    ):
        self.name, self.formatter, self.level = name, formatter, level
        self.echo, self.save = echo, save

        if type(generator) is str:
            if generator.startswith("."):
                generator = default_filename_generator(
                    prefix="Log", extension=generator
                )
            else:
                generator = default_filename_generator(
                    pattern=generator
                )
        self.fn_iter = iter(generator)

        if logs == "redirect":
            logs = self
        self.logs = logs

    def __call__(self, *args, **kwargs):
        """Wrap to `logger.info(...)` for shorthand."""
        self.logger.info(*args, **kwargs)

    def new(self):
        """Initialize the logger and the log file."""
        self.logger = logging.getLogger(self.name)

        if self.echo:
            self.consh = logging.StreamHandler(sys.stdout)
            self.consh.setFormatter(self.formatter)
            self.logger.addHandler(self.consh)

        if self.save:
            fn = next(self.fn_iter)
            self.fileh = logging.FileHandler(fn)
            self.fileh.setFormatter(self.formatter)
            self.logger.addHandler(self.fileh)

        self.logger.setLevel(self.level)
        
        if self.logs is not None:
            if self.save:
                self.logs("{} opened".format(fn))
            self.logs("Logger started")

    def close(self):
        """Terminate logging and remove attributes."""
        if self.logs is not None:
            self.logs("Terminating logger")
                
        if self.echo:
            self.logger.removeHandler(self.consh)
            del self.consh

        if self.save:
            self.logger.removeHandler(self.fileh)
            del self.fileh

        del self.logger