from python_packages.solvers.solver import *


class EulerMethod(Solver):
    
    def __init__(self, **kwargs):
        super().__init__(name = "EulerMethod", **kwargs)
    
    def evolve(self, X, t_step = None, **kwargs):
        if t_step == None:
            t_step = self.t_step
        
        return X + t_step * self.function(X, **kwargs)
