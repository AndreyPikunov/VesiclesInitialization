from python_packages.solvers.solver import *


class ModEulerMethod(Solver):
    
    def __init__(self, **kwargs):
        super().__init__(name = "ModifiedEulerMethod", **kwargs)
    
    def evolve(self, X, t_step = None, **kwargs):
        if t_step == None:
            t_step = self.t_step
            
        arg1 = X + 0.5*t_step*self.function(X , **kwargs)
        return X + t_step * self.function( arg1,  **kwargs)
