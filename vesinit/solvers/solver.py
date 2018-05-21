import numpy as np
from .. import tools


class Solver():
    """
    Abstract solver, base class for `EulerMethod` and `ModifiedEulerMethod`.

    """
    
    def __init__(self, t_step = 0.1, t_end = 100.0, frames = 100,
                 ADAPTIVE = False, parameters = [0.01, 0.9, 0.3, 2.0],
                 function = None,
                 name = "DummySolver"):
        
        """
        Note
        ----
        Can be initialized without a function for future simulation,
        if it's so, function must be given in `simulate()`.

        Parameters
        ----------
        t_step : float, `optional`.
            Simulation time-step.
            If `ADAPTIVE` = True, given t_step will be takes as initial t_step.
        t_end : float, `optional`.
            End-time of simulation.
        frames : int, `optional`.
            Number of snapshots.
            Varies if `ADAPTIVE`.
        ADAPTIVE: bool, `optional`.
            Switches `Solver` to adaptive mode (adapting time_step).
            Set by False by default.
        parameters: list of length 4, `optional`.
            Parameters for time-step adaptation:
                [0] = tolerance
                [1] = margin
                [2] = decrement
                [3] = increment
            Default = [0.01, 0.9, 0.3, 2.0]
        function = `function`, `optional`.
            Function for `simulate()` and `evolve()`.
            None by default.
        name: str, `optional`.
            Used for subclasses.
        """

        self.t_step = t_step
        
        self.t_end = t_end
            
        self.frames = frames
            
        self.ADAPTIVE = ADAPTIVE
            
        self.parameters = parameters # [tolerance, margin, decrement, increment]  

        self.function = function # Can be None
        
        self.name = name
        
    
    def adapt(self, t_step, delta, params): # adapts time step 
        """Adapts time_step.
        t_step_new = t_step * marg * min( max(tol/delta, decr) , incr )
            marg - margin
            tol - tolerance
            decr - decrement
            incr - increment"""
        
        tol = params[0] # tolerance
        marg = params[1] # magrin from tolerance
        decr = params[2] # maximal decrement
        incr = params[3] # maximum increment
        if delta != 0:
            return t_step * marg * min( max(tol/delta, decr) , incr )
        else:
            return t_step * marg * incr

    
    def evolve(self, X, t_step = None):
        """Evolve X for one time-step.
        Owerwritten in subclasses"""
        pass
  
    
    def simulate(self, X, output = None, t_step_list = None,
                 t_step = None, t_end = None, frames = None, SILENT = False,
                 ADAPTIVE = None, parameters = None,
                 function = None, **kwargs):
        
        """Does simulation from 0.0 to time-end using given `self.function`.
        
        Note
        ----
        Almost all Parameters are the same as in __init__.
        
        For comfort checks constants and walls for `function`.

        Parameters
        ----------
        output: list, `optional`.
            Frames of X (variable of interest).
            Saves progress even if kernel is interrupteed.
        t_step_list: list, `optional`.
            List of values of time-step.
            Usefull only for `ADAPTIVE` mode.
        SILENT: bool, `optional`.
            If False (default), prints time-current / time-end.
        **kwargs
            Arbitrary keywords arguments.
            Used for `function` calls.

        Returns
        -------
        output: list
            Frames of X (variable of interest).

        """
        
            
        if t_step == None:
            t_step = self.t_step             
        
        if t_end == None:
            t_end = self.t_end
            
        if frames == None:
            frames = self.frames

        if ADAPTIVE == None:
            ADAPTIVE = self.ADAPTIVE   
            
        if parameters == None:        
            parameters = self.parameters
                    
        if function != None:
            self.function = function # be careful, will rewrite self.function!!
            
        if self.function == None:
            print("function is not given! "+"\n"+"use Method.function = some_function "+"\n"+"EXIT")
            return None  
        
        ######### F O R    F U N C T I O N S ##################################################################
        if kwargs.get("constants") == None:       
            
            if str(self.function).split()[1] == "fun_points_in_basket":
                print("constants are not specified"+"\n"+"load from 'constants_for_fun_points_in_basket.txt'")
                constants = tools.load_constants_from_file("constants_for_fun_points_in_basket.txt")
                kwargs["constants"] = constants # REWRITING
                
            elif str(self.function).split()[1] == "fun_with_obstacles":
                print("constants are not specified"+"\n"+"load from 'constants_for_fun_with_obstacles.txt'")   
                constants = tools.load_constants_from_file("constants_for_fun_with_obstacles.txt")
                kwargs["constants"] = constants # REWRITING
                
        if kwargs.get("constants") != None:
            constants = kwargs.get("constants")
            for key in sorted(list(constants.keys())):
                print('{0:10}{1}'.format(key, constants[key]))
            
        if (kwargs.get("walls") != None) and (len(kwargs.get("walls"))!=0):          
            print(len(kwargs.get("walls")), "obstacles initialized")
        else:
            print("0 obstacles initialized - free space")
            
        ########################################################################################################
            
        print(self.__str__())  
            
        t = 0.0 # Current time
        t_print = 0.0 # Time to catch snapshot
        
        if output == None:
            output = [X] # initial state
        
        while (t<=t_end):
            
            if ADAPTIVE == True:
                
                X1 = self.evolve(X,
                                 t_step, **kwargs)
                
                X2 = self.evolve(self.evolve(X, 0.5*t_step, **kwargs),
                                 0.5*t_step, **kwargs)

                delta = float(np.linalg.norm(X1[:] - X2[:])) # [:] for instance of Variable class.
                       #float from np.float64                # TODO!!!! FOR ANY VECTORS   

                t_step = self.adapt(t_step, delta, parameters)
            
            X = self.evolve(X, t_step, **kwargs)
            
            if (t_print + t_step >= (t_end / frames) ):
              
                self.make_snapshot(X, output)
                t_print = 0.0
                
                if (SILENT==False):
                    print("{0:.5f} / {1}".format(t,t_end))
                   
            t_print = t_print + t_step      
            t = t + t_step
            
            if t_step_list!=None:       
                t_step_list.append(t_step)              
            
        return output

    
    def make_snapshot(self, X, output):
        output.append( X )       
 

    def __str__(self):
        
        s = ""           
        s = s + self.name + "\n"
        s = s + "t_step = " + str(self.t_step) + "\n"
        s = s + "t_end = " + str(self.t_end) + "\n"
        s = s + "frames = " + str(self.frames) + "\n"
        
        if self.function != None:   
            s = s + "function = " + self.function.__name__
        else:
            s = s + "function is not given"
        
        if self.ADAPTIVE == True:
            s = "Adaptive" + s + "\n"
            s = s + "parameters = [tol, marg, decr, incr] = " + str(self.parameters)      
        
        return s