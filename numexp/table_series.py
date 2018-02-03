# table_series.py
"""Class for table series, using LaTeX-style formatting."""

from .utils import default_filename_generator


class TableSeries(object):
    """Class for a series of tables."""

    def __init__(
        self,
        echo=True, save=False,
        logs=print, generator=".tbl",
    ):
        self.echo, self.save = echo, save
        self.logs = logs

        if type(generator) is str:
            if generator.startswith("."):
                generator = default_filename_generator(
                    prefix="Table", extension=generator
                )
            else:
                generator = default_filename_generator(
                    pattern=generator
                )
        self.fn_iter = iter(generator)

    def new(self, m, n):
        """Create a new table."""
        self.m, self.n = m, n
        self.cont = [["" for j in range(n)] for i in range(m)]

    def update(self, i, j, val):
        """Update a cell."""
        self.cont[i][j] = val

    def clean(self):
        """Remove a table."""
        del self.cont

    def convert(self):
        """Convert the current table into LaTeX-style TeX code."""
        col_fmt = "|c" * self.n + "|"

        st = ""
        st += "\\begin{{tabular}}{{{}}}\n".format(col_fmt)
        st += "\\hline\n"
        st += "".join([
            " & ".join(row) + "\\hline\n"
            for row in self.cont
        ])
        st += "\\end{tabular}\n"

        return st

    def write(self):
        """Save the code of table to a file."""
        fn = next(self.fn_iter)
        with open(fn, "w") as f:
            f.write(self.convert())
        if self.logs is not None:
            self.logs("{} saved".format(fn))

    def show(self):
        """Print the table."""
        self.logs(self.convert())

    def emit(self):
        """Save and print the table according to settings."""
        if self.save:
            self.write()
        if self.echo:
            self.show()