"""Set configurations about fonts in Matplotlib. The module must be import
before Pyplot."""
import matplotlib


def font_set(backend=None, family="sans-serif", tex=False):
    """General function to set fonts."""

    if backend is not None:
        matplotlib.use(backend)

    params = {
        "font.family": family,
        "text.usetex": tex
    }

    matplotlib.rcParams.update(params)


def font_use_tex():
    """Use default backend with TeX enabled for flexible switch between .pgf
    files or inline display."""
    font_set(family="serif", tex=True)


def font_use_default():
    """Use default configuration for simple inline display."""
    font_set()


def font_use_pgf():
    """Use pgf backend for high quality .pgf files adapted for TeX typesetting.
    Note that this configuation cannot handle inline displays."""
    font_set(backend="pgf", family="serif", tex=True)


def font_use_agg():
    """Use Agg backend for headless terminals without adequate GUI."""
    font_set(backend="Agg")
