"""Handlers for results, mainly for off-line plotting and model saving."""
import pickle

import numpy

from exputils import utils
from exputils import journal

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
        
        self.content = [[] for i in range(size)]
        self.update()
    
    def update(self, index=None):
        """Update filenames."""
        if index is None:
            self.file = [self.name(self.fmt, i, utils.result_dir) for i in range(self.size)]
        else:
            self.file[index] = self.name(self.fmt, index, utils.result_dir)
    
    def push(self, index, obj):
        """Push an object into the object list."""
        self.content[index].append(obj)
    
    def numpy(self, index):
        """Convert some content into `numpy.ndarray`."""
        self.content[index] = numpy.array(self.content[index])
    
    def save(self, index):
        """Save some content."""
        with open(self.file[index], "wb") as file:
            pickle.dump(self.content[index], file)
        filename = self.file[index]
        if self.log is not None:
            self.log("Result {} saved".format(filename))
        journal.logger.info("SAVE: Result {}".format(filename))

    def export(self, func, index):
        """Use a specific function to export some content."""
        filename = self.file[index]
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
