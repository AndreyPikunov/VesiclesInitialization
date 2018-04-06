from python_packages.solvers.solver import *


class EulerMethod(Solver):
    
    def __init__(self):
        Solver.__init__(self,name="EulerMethod")
    
    def function(self, X):
        pass
    
    def evolve(self, X, t_step = None):
        if t_step == None:
            t_step = self.t_step
        
        return X + t_step * self.function(X)
