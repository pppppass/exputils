"""Local utilities."""
import datetime

def NameFunction(fmt, ctr):
    """Function to generate a series of filenames."""
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    second = now.strftime("%H%M%S")
    st = fmt.format(ctr=ctr, date=date, second=second)
    return st
