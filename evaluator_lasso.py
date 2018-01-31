import time

import numpy

import numexp


def error_function(x0, x):
    return numpy.linalg.norm(x0 - x) / (1. + numpy.linalg.norm(x0))


class EvaluatorSetOptimum(numexp.evaluator.Evaluator):
    def __init__(self, **kwargs):
        super(EvaluatorSetOptimum, self).__init__(**kwargs)
        self.name = "Set optimum solution"

    def evaluate(self, problem, method, tags={}):
        _, out = method.run(problem)
        problem.xx = problem.x
        del problem.x


class EvaluatorTest(numexp.evaluator.Evaluator):
    def __init__(self, export=None, clean=True, save=False, **kwargs):
        super(EvaluatorTest, self).__init__(**kwargs)
        self.name = "Test"
        self.export = export
        self.clean = clean
        self.save = save

    def evaluate(self, problem, method, tags={}):
        start = time.time()
        _, out = method.run(problem, statistics=True)
        end = time.time()
        elapsed = end - start

        err = problem.A.dot(problem.x) - problem.b
        approx = 1. / 2. * numpy.sum(err**2)
        reg = numpy.sum(numpy.abs(problem.x))
        loss = approx + problem.mu * reg

        if self.save:
            out["solution"] = problem.x

        out["problem"] = problem.name
        out["problem_repr"] = repr(problem)
        out["method"] = method.name
        out["method_repr"] = repr(method)
        out["evaluator"] = self.name
        out["evaluator_repr"] = repr(self)

        out["total_time"] = elapsed

        out["check"] = loss
        out["approximation"] = approx
        out["regularization"] = reg

        if hasattr(problem, "xx"):
            out["error_xx"] = error_function(problem.xx, problem.x)
        out["error_gt"] = error_function(problem.u, problem.x)

        if self.clean:
            del problem.x

        if self.export is not None:
            self.export(out)

        return out