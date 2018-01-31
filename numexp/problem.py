class Problem(object):
    def __init__(self, tags=set(), **kwargs):
        self.tags = tags
        for key, val in kwargs.items():
            setattr(self, key, val)
