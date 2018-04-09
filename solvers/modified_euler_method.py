from python_packages.solvers.solver import *


class ModEulerMethod(Solver):
    
    def __init__(self, **kwargs):
        super().__init__(name = "ModifiedEulerMethod", **kwargs)
    
    def function(self, X):
        pass
    
    def evolve(self, X, t_step = None):
        if t_step == None:
            t_step = self.t_step
        return X + t_step * self.function( X + 0.5*t_step*self.function(X))
