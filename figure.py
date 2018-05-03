"""Handlers for figures, mainly handling complicated routines of Matpoltlib."""
from matplotlib import pyplot
import mpl_toolkits.mplot3d

from exputils import utils
from exputils import journal

utils.ensure_dir(utils.figure_dir)

class FigureHandler(object):
    """Class to handle figures."""
    
    def __init__(
        self,
        fig=None, ax=None,
        save=False, echo=True,
        size=(6., 4.),
        fmt="{dire}{debug}Figure-{date}{second}-{ctr:03}.png",
        log=print,
    ):
        """Initialize a figure handler."""
        
        self.fig, self.ax = fig, ax
        self.save, self.echo = save, echo
        self.size, self.fmt = size, fmt
        self.log = log
        
        self.ctr = 0
        self.name = utils.name_function

    def new_fig(self, size=None):
        """Allocate a new figure."""
        if size is not None:
            self.fig = pyplot.figure(figsize=size)
        else:
            self.fig = pyplot.figure(figsize=self.size)

    def new_ax(self, *args, **kwargs):
        """Add a single subplot."""
        if len(args) > 0 or len(kwargs) > 0:
            self.ax = self.fig.add_subplot(*args, **kwargs)
        else:
            self.ax = self.fig.add_subplot(1, 1, 1)

    def save_fig(self):
        """Save the figure to file according to settings."""
        filename = self.name(self.fmt, self.ctr, utils.figure_dir)
        pyplot.savefig(filename)
        if self.log is not None:
            self.log("Figure {} saved".format(filename))
        journal.logger.info("SAVE: Figure {}".format(filename))
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
        self.new_fig()
        self.new_ax()
        func(*args, **kwargs, fh=self)
        self.disp_fig()
        self.close_fig()
    
    def set_box(self, left=None, right=None, bottom=None, up=None, grid=None, aspect=None, axis=None, title=None):
        """Configure the view port."""
        
        if left is not None and right is not None:
            self.ax.set_xlim(left, right)
        if bottom is not None and up is not None:
            self.ax.set_ylim(bottom, up)
        
        if grid is not None:
            self.ax.grid(grid)
        
        if aspect is not None:
            self.ax.set_aspect(aspect)
        
        if axis is not None:
            if axis:
                self.ax.set_axis_on()
            else:
                self.ax.set_axis_off()

        if title is not None:
            self.ax.set_title(title)
    
    def set_accs(self, title=None, tight=None):
        """Set some accessories."""
        if tight is not None:
            if tight:
                self.fig.tight_layout()
        if title is not None:
            self.fig.suptitle(title)
