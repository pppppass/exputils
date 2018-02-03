# figure_series.py
"""Class for figure series, using Matplotlib."""

from matplotlib import pyplot

from .utils import default_filename_generator


class FigureSeries(object):
    """Class for a series of figures."""

    def __init__(
        self,
        echo=True, save=False,
        logs=print, generator=".png",
    ):
        self.echo, self.save = echo, save
        self.logs = logs

        if type(generator) is str:
            if generator.startswith("."):
                generator = default_filename_generator(
                    prefix="Figure", extension=generator
                )
            else:
                generator = default_filename_generator(
                    pattern=generator
                )
        self.fn_iter = iter(generator)

    def figure(self, *args, **kwargs):
        """Allocate a new figure."""
        self.fig = pyplot.figure(*args, **kwargs)

    def subplot(self, *args, **kwargs):
        """Add a new sub-plot."""
        self.ax = self.fig.add_subplot(*args, **kwargs)

    def fast_create(self):
        """Create a new canvas fast, that is, allocate a new figure and add
        a full-size sub-plot."""
        self.figure()
        self.subplot(1, 1, 1)

    def write(self, *args, **kwargs):
        """Write current figure to file."""
        fn = next(self.fn_iter)
        pyplot.savefig(fn, *args, **kwargs)
        if self.logs is not None:
            self.logs("{} saved".format(fn))

    def show(self, *args, **kwargs):
        """Show a figure by Matplotlib."""
        pyplot.show(*args, **kwargs)

    def emit(self):
        """Write and show the figure according to settings."""
        if self.save:
            self.write()
        if self.echo:
            self.show()

    def close(self):
        """Close a figure."""
        del self.ax

        pyplot.close(self.fig)
        del self.fig

    def fast_invoke(self, function, *args, **kwargs):
        """Invoke and plot a function fast, often use to perform quick
        plotting"""
        self.fast_create()
        function(self, *args, **kwargs)
        self.emit()
        self.close()

    def plot(self, *args, **kwargs):
        """Plot something."""
        self.ax.plot(*args, **kwargs)

    def aspect(self, aspect, *args, **kwargs):
        """Change the aspect."""
        self.ax.set_aspect(aspect, *args, **kwargs)

    def colorbar(self, mappable, *args, **kwargs):
        """Add a colorbar to current figure."""
        self.fig.colorbar(mappable, *args, **kwargs)