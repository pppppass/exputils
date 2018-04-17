"""Handlers for figures, mainly handling complicated routines of Matpoltlib."""
from matplotlib import pyplot
import mpl_toolkits.mplot3d

from . import utils

class FigureHandler(object):
    """Class to handle figures."""
    
    def __init__(
        self,
        fig=None, ax=None,
        save=False, echo=True,
        size=(6., 4.),
        fmt="Figure-{second}-{ctr:03}.png",
        log=print,
    ):
        """Initialize a figure handler."""
        
        self.fig, self.ax = fig, ax
        self.save, self.echo = save, echo
        self.size, self.fmt = size, fmt
        self.log = log
        
        self.ctr = 0
        self.name = utils.NameFunction

    def new_fig(self):
        """Allocate a new figure."""
        self.fig = pyplot.figure(figsize=self.size)

    def new_ax(self):
        """Add a single subplot."""
        self.ax = self.fig.add_subplot(1, 1, 1)

    def save_fig(self):
        """Save the figure to file according to settings."""
        filename = self.name(self.fmt, self.ctr)
        pyplot.savefig(filename)
        if self.log is not None:
            self.log("Figure {} saved".format(filename))
        self.ctr += 1

    def disp_fig(self):
        """Display a figure by either saving or showing."""
        if self.save:
            self.save_fig()
        if self.echo:
            pyplot.show()

    def close_fig(self):
        """Close the figure."""
        pyplot.close(self.fig)

    def fast(self, func, *args, **kwargs):
        """Fast wrapper to invoke a plotting routine."""
        self.new_figure()
        self.new_axes()
        func(self, *args, **kwargs)
        self.finish()
        self.close()
    
    def set_box(self, left=1.0, right=0.0, bottom=1.0, up=0.0, grid=None, aspect=None):
        """Configure the view port."""
        
        if left < right:
            self.ax.set_xlim(left, right)
        if bottom < up:
            self.ax.set_ylim(bottom, up)
        
        if grid is not None:
            self.ax.grid(grid)
        
        if aspect is not None:
            self.ax.set_aspect(aspect)
