# problem.py
"""Problem class."""

import abc

class Problem(object, metaclass=abc.ABCMeta):
    """Abstract base class `Problem`, from which other problem classes should
    be derived."""
    def __init__(self, tags=None, **kwargs):
        if tags is None:
            self.tags = set()
        else:
            self.tags = tags
        for key, val in kwargs.items():
            setattr(self, key, val)

    @abc.abstractmethod
    def title(self):
        """Abstract method, et the title of the problem."""
        pass