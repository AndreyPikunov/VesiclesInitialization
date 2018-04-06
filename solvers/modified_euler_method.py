from python_packages.solvers.solver import *


class ModEulerMethod(Solver):
    
    def __init__(self):
        Solver.__init__(self,name="ModEulerMethod")
    
    def function(self, X):
        pass
    
    def evolve(self, X, t_step = None):
        if t_step == None:
            t_step = self.t_step
        
        #print(type(t_step))
        #print(type(self.function(X)))
        #print(type(X))
        
        return X + t_step * self.function( X + 0.5*t_step*self.function(X))
