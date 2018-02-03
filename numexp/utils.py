# utils.py
"""Utilities."""

import time
import datetime


def tictoc(function, *args, **kwargs):
    """Time some function, emulating MATLAB's tic() and toc()."""
    start = time.time()
    ret = function(*args, **kwargs)
    end = time.time()
    elapsed = end - start
    return elapsed, ret


def default_filename_generator(
    prefix="", extension="",
    pattern="{prefix}-{date}-{time}-{counter:03}{extension}",
    limit=1000
):
    """A generator for a series of filenames."""
    for i in range(limit):
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")
        kw = dict(
            prefix=prefix, extension=extension,
            date=date_str, time=time_str,
            counter=i
        )
        yield pattern.format(**kw)