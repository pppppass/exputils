# method.py
"""Method class."""

import abc


class Method(object, metaclass=abc.ABCMeta):
    """Abstract base class `Method`, from which other method classes should
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
        """Abstract method, which returns the title of the method."""
        pass

    @abc.abstractmethod
    def run(self, problem, statistics=False):
        """Abstract method, which performs the method onto the problem."""
        pass