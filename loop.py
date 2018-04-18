"""Hook for loops."""

class LoopHook(object):
    """Class to hook loops."""
    
    def __init__(self, start=0):
        """Initialize a loop hook."""
        self.ctr = start
        
    def step(self):
        """Step the counter."""
        self.ctr += 1
    
    def do(self, func, *args, **kwargs):
        """Invoke a function directly."""
        func(*args, **kwargs, hook=self)
    
    def do_div(self, num, func, *args, **kwargs):
        """Invoke a function according if a given number divides the counter."""
        if self.ctr % num == 0:
            func(*args, **kwargs, hook=self)
