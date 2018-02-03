import datetime

import matplotlib.pyplot
import mpl_toolkits.mplot3d


def figure_name_generator_default(counter, extension=""):
    counter += 1
    now = datetime.datetime.now()
    time_st = now.strftime("%Y%m%d-%H%M%S")
    st = "Figure-{0}-{1:03}".format(time_st, counter) + extension
    return st, counter


class FigureHandler(object):
    def __init__(
        self,
        figure=None, axis=None,
        echo=True, export=False, extension=".png",
        log=print, filename=figure_name_generator_default
    ):
        self.fig, self.ax = figure, axis
        self.echo, self.exp, self.ext = echo, export, extension
        self.log, self.fn = log, filename
        self.ctr = 0

    def refresh(self, *args, **kwargs):
        self.fig = matplotlib.pyplot.figure(*args, **kwargs)

    def subplot(self, *args, **kwargs):
        self.ax = self.fig.add_subplot(*args, **kwargs)

    def new(self):
        self.refresh()
        self.subplot(1, 1, 1)

    def save(self, *args, **kwargs):
        fn, self.ctr = self.fn(self.ctr, self.ext)
        matplotlib.pyplot.savefig(fn, *args, **kwargs)
        if self.log is not None:
            self.log("{} saved".format(fn))

    def display(self, *args, **kwargs):
        matplotlib.pyplot.show(*args, **kwargs)

    def show(self):
        if self.exp:
            self.save()
        if self.echo:
            self.display()

    def close(self):
        matplotlib.pyplot.close(self.fig)

    def aspect(self, aspect, *args, **kwargs):
        self.ax.set_aspect(aspect, *args, **kwargs)

    def colorbar(self, mappable, *args, **kwargs):
        self.fig.colorbar(mappable, *args, **kwargs)

    def fast(self, function, *args, **kwargs):
        self.new()
        function(self, *args, **kwargs)
        self.show()
        self.close()