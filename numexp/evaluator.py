class Evaluator(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def evaluate(self, problem, method, tags=set()):
        raise NotImplementedError(
            "The function `evaluate` in class `Evaluator` is not implemented"
        )
