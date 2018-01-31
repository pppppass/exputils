import numpy
import scipy.stats
import scipy.sparse

import numexp


class ProblemLasso(numexp.problem.Problem):
    def __init__(self, **kwargs):
        super(ProblemLasso, self).__init__(**kwargs)


def lasso_random(observed=512, solving=1024, regularizer=1e-3, density=0.1, seed=1):
    A = numpy.random.randn(observed, solving)
    distrb = scipy.stats.norm()
    u = scipy.sparse.random(solving, 1, density=density, data_rvs=distrb.rvs).A
    b = A.dot(u)

    x0 = numpy.random.rand(solving, 1)

    prob = ProblemLasso(
        m=observed, n=solving,
        A=A, u=u, b=b,
        x0=x0,
        mu=regularizer,
        name="LASSO, randomly generated",
    )
    return prob
