from python_packages.solvers.solver import *


class ModEulerMethod(Solver):
    
    def __init__(self, **kwargs):
        super().__init__(name = "ModifiedEulerMethod", **kwargs)
    
    def function(self, X):
        pass
    
    def evolve(self, X, walls = [], t_step = None):
        if t_step == None:
            t_step = self.t_step
            
        #print(self.function(X , walls))
            
        arg1 = X + 0.5*t_step*self.function(X , walls)
        return X + t_step * self.function( arg1 , walls)
