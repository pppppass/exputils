import time

import numpy

import mosek

import numexp


class MethodMosek(numexp.method.Method):
    def __init__(self, tags=set(), **kwargs):
        super(MethodMosek, self).__init__(tags, **kwargs)
        self.name = "MOSEK, iterior point method"

    def run(self, problem, statistics=False):
        self.prob = problem
        self.stat = statistics

        with mosek.Env() as self.env:
            with self.env.Task() as self.task:
                self.configure()
                self.model()
                self.invoke()
                self.recover()

        out = self.summarize()

        del self.env
        del self.task

        del self.prob
        del self.stat

        return problem, out

    def configure(self):
        self.task.putintparam(mosek.iparam.optimizer, mosek.optimizertype.intpnt)
    
    def model(self):
        start = time.time()

        m, n = self.prob.A.shape

        inf = 0.

        self.task.appendcons(2 * n + m)
        self.task.appendvars(2 * n + m)

        self.task.putqobj(range(2 * n, 2 * n + m),
                          range(2 * n, 2 * n + m), [1.] * m)

        self.task.putclist(range(n, 2 * n), [self.prob.mu] * n)

        self.task.putconboundlist(
            range(0, n),
            [mosek.boundkey.up] * n,
            [inf] * n, [0.] * n
        )
        self.task.putconboundlist(
            range(n, 2 * n),
            [mosek.boundkey.lo] * n,
            [0.] * n, [inf] * n
        )
        self.task.putconboundlist(
            range(2 * n, 2 * n + m),
            [mosek.boundkey.fx] * m,
            self.prob.b[:, 0], self.prob.b[:, 0]
        )

        self.task.putvarboundlist(
            range(2 * n + m),
            [mosek.boundkey.fr] * (2 * n + m),
            [inf] * (2 * n + m), [inf] * (2 * n + m)
        )
        for i in range(n):
            self.task.putarow(i, [i, n + i], [1., -1.])
            self.task.putarow(i + n, [i, n + i], [1., 1.])
        for i in range(m):
            self.task.putarow(i + 2 * n, range(n), self.prob.A[i, :])
            self.task.putaij(i + 2 * n, 2 * n + i, -1.)

        end = time.time()
        self.setup = end - start

    def invoke(self):
        self.task.optimize()

    def recover(self):
        m, n = self.prob.A.shape

        xx = [0.] * (2 * n + m)
        self.task.getxx(mosek.soltype.itr, xx)

        x = numpy.array(xx[:n]).reshape(n, 1)

        self.prob.x = x

    def summarize(self):
        if self.stat:
            out = {
                "loss": self.task.getprimalobj(mosek.soltype.itr),
                "vars": self.task.getintinf(mosek.iinfitem.opt_numvar),
                "iters": self.task.getintinf(mosek.iinfitem.intpnt_iter),
                "setup_time": self.setup,
                "solve_time": self.task.getdouinf(mosek.dinfitem.optimizer_time),
            }

            del self.setup

            return out
        else:
            return None
