# evaluator.py
"""Evaluator class."""

import abc


class Evaluator(object, metaclass=abc.ABCMeta):
    """Abstract base class `Evaluator`, from which other evaluator classes
    should be derived."""

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
    def evaluate(self, problem, method, tags=None):
        """Abstract method, which evaluate the method on the problem."""
        pass