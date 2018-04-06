from python_packages.solvers.solver import *
from python_packages.solvers.modified_euler_method import *


import numpy as np

#params = (tol, marg, decr, incr)

class AdaptiveModEulerMethod(ModEulerMethod):
    
    def __init__(self):
        Solver.__init__(self,name="AdaptiveModEulerMethod")
        
    def adapt(self, t_step, delta, params):
        tol = params[0]
        marg = params[1]
        decr = params[2]
        incr = params[3]
        delta = delta + 0.0000000001 #to avoid division by 0
        return float (t_step * marg * min( max(tol/delta, decr) , incr )  ) # FIX smtimes returns np.float64     
        
    def simulate(self, X, output, params = (1.0, 0.9, 0.3, 2.0), t_step = None, t_end = None, frames = None, SILENT = True):
        
        if t_step == None:
            t_step = self.t_step
        if t_end == None:
            t_end = self.t_end
        if frames == None:
            frames = self.frames           
        
        t = 0.0
        t_print = 0.0
        t_list = []
            
        while (t<=t_end):
            
            X1 = self.evolve(X, t_step)
            X2 = self.evolve(self.evolve(X, 0.5*t_step), 0.5*t_step)
            
            delta = np.linalg.norm(X1 - X2) # [:] for instance of Variable class
            
            t_step = self.adapt(t_step, delta, params)
            #print("adsadas   ",t_step)
            #input()
            
            X = self.evolve(X, float(t_step))
            
            if (t_print >= (t_end / float(frames)) ):
                
                #print(t_print,"/",(t_end / float(frames)))
                
                self.make_snapshot(X, output)
                t_print = 0.0
                
                if (SILENT==False):
                    print(t,"/",t_end, "/ TIME_STEP =", t_step)
                   
            t_print = t_print + t_step      
            t = round(t + t_step , 7) # TODO, avoiding error!
            
            t_list.append(t_step)
            
        return X , t_list
    