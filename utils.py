import datetime

def NameGenerator(fmt=""):
    ctr = 0
    while True:
        now = datetime.datetime.now()
        time_str = now.strftime("%Y%m%d-%H%M%S")
        st = fmt.format(ctr=ctr, time=time_str)
        yield st
        ctr += 1
