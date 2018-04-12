from matplotlib import pyplot
import mpl_toolkits.mplot3d

class FigureHandler(object):
    def __init__(
        self,
        fig=None, ax=None,
        save=False, echo=True,
        size=(6, 4), fmt="Figure-{time}-{ctr:03}.png",
        log=print,
    ):
        self.fig, self.ax = fig, ax
        self.save, self.echo = save, echo
        self.size, self.fmt = size, fmt
        self.log = log

        self.name_gen = NameGenerator(fmt)
        self.name_iter = iter(self.name_gen)

    def new_figure(self):
        self.fig = pyplot.figure(size=size)

    def new_axes(self):
        self.ax = self.add_subplot(1, 1, 1)

    def export(self):
        filename = next(self.name_iter)
        pyplot.savefig(fn)
        if self.log is not None:
            self.log("Figure {} saved".format(filename))

    def finish(self):
        if self.save:
            self.export()
        if self.echo:
            pyplot.show()

    def close(self):
        pyplot.close(self.fig)

    def fast(self, func, *args, **kwargs):
        self.new_figure()
        self.new_axes()
        func(self, *args, **kwargs)
        self.finish()
        self.close()
