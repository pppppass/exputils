class Method(object):
    def __init__(self, tags=set(), **kwargs):
        self.tags = tags
        for key, val in kwargs.items():
            setattr(self, key, val)

    def run(self, problem, statistics=False):
        raise NotImplementedError("The function `run` in class `Method` is not implemented")
