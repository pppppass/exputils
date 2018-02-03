# font.py
"""Font setting, related to Matplotlib."""
import matplotlib


def font_set(backend="default", family="serif", tex=False):
    """Set the font configuration."""
    if backend != "default":
        matplotlib.use(backend)
    params = {
        "font.family": family,
        "text.usetex": tex
    }
    matplotlib.rcParams.update(params)


def font_use_pgf():
    """Use pgf backend, in order to invoke TeX and `pgf` package for further
    typesetting."""
    font_set(backend="pgf", tex=True)


def font_use_inline():
    """Use default configuration for inlne plots in Jupyter Notebook, that is,
    default backend and sans-serif font."""
    font_set(family="sans-serif")

def font_use_headless():
    """Use Agg backend, for headless terminal without an adequate GUI."""
    font_set(backend="Agg", family="sans-serif")
