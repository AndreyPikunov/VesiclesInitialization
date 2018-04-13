from .solver import *

class ModEulerMethod(Solver):
    """
    SCHEME
    ------
    X_new = X_old + t*F( 0.5 * t * F(X_old) )
    """
    
    def __init__(self, **kwargs):
        super().__init__(name = "ModifiedEulerMethod", **kwargs)
    
    def evolve(self, X, t_step = None, **kwargs):
        
        if t_step == None:
            t_step = self.t_step
            
        arg1 = X + 0.5*t_step*self.function(X , **kwargs)
        
        return X + t_step * self.function( arg1,  **kwargs)
