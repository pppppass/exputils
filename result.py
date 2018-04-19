"""Handlers for results, mainly for off-line plotting and model saving."""
import pickle

import numpy

from . import utils
from . import journal

utils.ensure_dir(utils.result_dir)

class ResultHandler(object):
    """Class to handle results."""
    
    def __init__(
        self,
        size,
        fmt="{dire}{debug}Result-{date}{second}-{ctr:03}.pkl",
        log=print,
    ):
        """Initialize a result handler."""
        self.size = size
        self.fmt = fmt
        self.log = log
        
        self.name = utils.name_function
        
        self.cont = [[] for i in range(size)]
        self.update()
    
    def update(self, ind=None):
        """Update filenames."""
        if ind is None:
            self.file = [self.name(self.fmt, i, utils.result_dir) for i in range(self.size)]
        else:
            self.file[ind] = self.name(self.fmt, ind, utils.result_dir)
    
    def numpy(self, ind):
        """Convert some content into `numpy.ndarray`."""
        self.cont[ind] = numpy.array(self.cont[ind])
    
    def save(self, ind):
        """Save some content."""
        with open(self.file[ind], "wb") as file:
            pickle.dump(self.cont[ind], file)
        filename = self.file[ind]
        if self.log is not None:
            self.log("Result {} saved".format(filename))
        journal.logger.info("SAVE: Result {}".format(filename))

    def export(self, func, ind):
        """Use a specific function to export some content."""
        filename = self.file[ind]
        func(filename)
        if self.log is not None:
            self.log("Result {} saved".format(filename))
        journal.logger.info("SAVE: Result {}".format(filename))

def extract(filename):
    """Extract an object directly from .pkl file."""
    with open(filename, "rb") as file:
        obj = pickle.load(file)
    return obj

def load(filename, func):
    """Use a specific function to load some content."""
    with open(filename, "rb") as file:
        return func(file)
    