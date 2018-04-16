"""Local utilities."""
import datetime

def NameFunction(fmt, ctr):
    """Function to generate a series of filenames."""
    now = datetime.datetime.now()
    second = now.strftime("%Y%m%d")
    milli = now.strftime("%H%M%S")
    st = fmt.format(ctr=ctr, second=second, milli=milli)
    return st
