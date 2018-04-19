"""Local utilities."""
import datetime
import os

debug_flag = False

def name_function(fmt, ctr, dire):
    """Function to generate a series of filenames."""
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    second = now.strftime("%H%M%S")
    if debug_flag:
        debug = "_DEBUG_"
    else:
        debug = ""
    st = fmt.format(dire=dire, ctr=ctr, date=date, second=second, debug=debug)
    return st

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

figure_dir = "Figures/"
log_dir = "Logs/"
result_dir = "Results/"

jrnl_config = dict(
    title="Journal",
    name="Journal.log",
    msg="{asctime} {levelname:8} @{lineno:3}: {message}",
)
jrnl = None
