# result_series.py
"""Class for result series, using shelves."""

import shelve

from .utils import default_filename_generator


class ResultSeries(object):
    """Class for a series of results. It is strongly recommended to use fixed
    name for the result database."""

    def __init__(
        self,
        logs=print, generator="",
    ):
        self.logs = logs

        if type(generator) is str:
            if generator.startswith("."):
                generator = default_filename_generator(
                    prefix="Result", extension=generator
                )
            else:
                generator = default_filename_generator(
                    pattern=generator
                )
        self.fn_iter = iter(generator)

    def bind(self):
        """Bind the filename to the database."""
        self.fn = next(self.fn_iter)

    def unbind(self):
        """Unbind the filename."""
        del self.fn

    def reset(self):
        """Reset the database, namely reset the counter."""
        with shelve.open(self.fn) as db:
            db["counter"] = 0

        if self.logs is not None:
            self.logs("File {} reset".format(self.fn))

    def write(self, data):
        """Write a new entry to the database."""
        with shelve.open(self.fn) as db:
            ctr = db["counter"]
            db["item" + str(ctr)] = data
            db["counter"] = ctr + 1

            if self.logs is not None:
                self.logs("The {}th item in {} updated".format(ctr, self.fn))

    def generator(self):
        """A generator to go through the database."""
        with shelve.open(self.fn) as db:
            ctr = db["counter"]
            for key, val in db.items():
                if key != "counter":
                    yield val

    def sequence(self):
        """Sequence of all the entries in the database."""
        gen = self.generator()
        return list(gen)

    def apply(self, *args):
        """Apply a sequence of functions to the database, useful for table
        formatting."""
        ret = self.sequence()
        for lamda in args:
            ret = lamda(ret)
        return ret