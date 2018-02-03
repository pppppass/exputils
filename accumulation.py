# accumulation.py
"""A simple example of sequence accumulation"""

import time
import abc

import numpy

import numexp


class PAccumulation(numexp.Problem):
    """Accumulation problem class."""

    def __init__(self, *args, **kwargs):
        # Use `kwargs` to set attributes
        super(PAccumulation, self).__init__(*args, **kwargs)

        self.tags |= {"acc"}

    def title(self):
        # Versatile title
        title = "Accumulation problem, sized {}".format(self.n)
        return title

# Define some functions to generate specific problems


def accumulation_random(length=10000000, seed=0):
    """Randomly generate an accumulation problem."""

    # Always use a seed keyword to handle randomness
    numpy.random.seed(seed)

    n = length
    seq = numpy.random.randn(length)

    prob = PAccumulation(n=n, seq=seq)
    return prob

# Define a base class for some similar methods


class MAccumulate(numexp.Method, metaclass=abc.ABCMeta):
    """Abstract base class for accumlation methods"""

    def __init__(self, *args, **kwargs):
        super(MAccumulate, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def title(self):
        """Abstract method, returns the title of the accumulation method"""
        pass

    def run(self, problem, statistics=False):
        # Ignore `statistics` for convenience, which may control whether
        # statistical information, namely `out`, is given out

        # Attach the problem
        self.prob = problem

        # Time the method
        elapsed, _ = numexp.tictoc(self.invoke)

        # Handle statistical iniformation
        out = {
            "size": self.prob.n,
            "sigma": self.prob.x,
            "solve": elapsed,
        }

        return problem, out

    @abc.abstractmethod
    def invoke(self):
        """Abstract method, truely perform the method."""
        pass


class MForAccumulate(MAccumulate):
    """Method class, accumulating using `for`."""

    def __init__(self, *args, **kwargs):
        super(MForAccumulate, self).__init__(*args, **kwargs)

        # Set tags
        self.tags |= {"for"}

    def title(self):
        title = "Accumulate with `for`"
        return title

    def invoke(self):
        seq = self.prob.seq
        res = 0.
        for v in seq:
            res += v
        res = float(res)
        self.prob.x = res


class MSumAccumulate(MAccumulate):
    """Method class, accumulating using `sum`."""

    def __init__(self, *args, **kwargs):
        super(MSumAccumulate, self).__init__(*args, **kwargs)

        self.tags |= {"sum"}

    def title(self):
        title = "Accumulate with `sum`"
        return title

    def invoke(self):
        seq = self.prob.seq
        res = sum(seq)
        res = float(res)
        self.prob.x = res


class MNumpyAccumulate(MAccumulate):
    """Method class, accumulating using `numpy.sum`."""

    def __init__(self, *args, **kwargs):
        super(MNumpyAccumulate, self).__init__(*args, **kwargs)

        self.tags |= {"numpy"}

    def title(self):
        title = "Accumulate with `numpy.sum`"
        return title

    def invoke(self):
        seq = self.prob.seq
        res = numpy.sum(seq)
        res = float(res)
        self.prob.x = res


class ESet(numexp.Evaluator):
    """Evaluator to set the optimal solution."""

    def __init__(self, *args, **kwargs):
        super(ESet, self).__init__(*args, **kwargs)

        self.tags |= {"set"}

    def title(self):
        title = "Set the solution"
        return title

    def evaluate(self, problem, method, tags=None):
        elapsed, (_, out) = numexp.tictoc(method.run, problem, statistics=True)
        # Set the optimal solution and time
        problem.xx = problem.x
        problem.tx = elapsed
        del problem.x


class ETest(numexp.Evaluator):
    """Evaluator to test methods."""

    def __init__(self, export, logs=print, *args, **kwargs):
        super(ETest, self).__init__(*args, **kwargs)

        self.tags |= {"test"}
        # Function to export statistical information
        self.exp = export
        self.logs = logs

    def title(self):
        title = "Test"
        return title

    def evaluate(self, problem, method, tags=None):
        if tags is None:
            tags = set()

        elapsed, (_, out) = numexp.tictoc(method.run, problem, statistics=True)

        # Collect some other information
        out["tags"] = tags | problem.tags | method.tags | self.tags
        out["problem"] = problem.title()
        out["method"] = method.title()
        out["evaluator"] = self.title()

        # Record the ending time for filtering
        out["end"] = time.time()
        out["total"] = elapsed

        if hasattr(problem, "tx"):
            out["ratio"] = elapsed / problem.tx

        # Export statistical information
        self.exp(out)

        # Print statistical information
        if self.logs is not None:
            self.logs("Statistical information starts")
            for key, val in out.items():
                self.logs("{}: {!s}".format(key, val))
            self.logs("Statistical information ends")

        # Clean the temporary solution
        del problem.x

        return out
