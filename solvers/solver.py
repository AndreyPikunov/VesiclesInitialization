import numpy as np

class Solver(): # TODO make it adaptive
    
    def __init__(self, **kwargs):
        
        if kwargs.get("name") != None:
            self.name = kwargs.get("name")
        else:
            self.name = "DummySolver"
            
        if kwargs.get("t_step") != None:
            self.t_step = kwargs.get("t_step")
        else:
            self.t_step = 0.1
        
        if kwargs.get("t_end") != None:
            self.t_end = kwargs.get("t_end")
        else:
            self.t_end = 100.0
            
        if kwargs.get("frames") != None:
            self.frames = kwargs.get("frames")
        else:
            self.frames = 100
            
        if kwargs.get("ADAPTIVE") != None:
            self.ADAPTIVE = kwargs.get("ADAPTIVE")
        else:
            self.ADAPTIVE = False
             
        self.parameters = [0.01, 0.9, 0.3, 2.0]
        if kwargs.get("parameters") != None:
            self.parameters[0] = kwargs.get("parameters")[0] # tolerance
            self.parameters[1] = kwargs.get("parameters")[1] # margin
            self.parameters[2] = kwargs.get("parameters")[2] # decrement
            self.parameters[3] = kwargs.get("parameters")[3] # increment
        
                                      
    
    def function(self, X):
        pass
    
    
    def adapt(self, t_step, delta, params): # adapts time step 
        tol = params[0] # tolerance
        marg = params[1] # magrin from tolerance
        decr = params[2] # maximal decrement
        incr = params[3] # maximum increment
        delta = delta + 0.0000000001 #to avoid division by 0
        return float (t_step * marg * min( max(tol/delta, decr) , incr )  ) # FIX sometimes returns np.float64     

    
    def evolve(self, X, t_step = None):
        pass
    
    def simulate(self, X, output, **kwargs):
 

        if kwargs.get("t_step") != None:
            t_step = kwargs.get("t_step")
        else:
            t_step = self.t_step
        
        if kwargs.get("t_end") != None:
            t_end = kwargs.get("t_end")
        else:
            t_end = self.t_end
            
        if kwargs.get("frames") != None:
            frames = kwargs.get("frames")
        else:
            frames = self.frames
            
        if kwargs.get("ADAPTIVE") == None:
            ADAPTIVE = self.ADAPTIVE
        else:
            ADAPTIVE = kwargs.get("ADAPTIVE")
                
        parameters = self.parameters
        if kwargs.get("parameters") != None:
            parameters[0] = kwargs.get("parameters")[0] # tolerance
            parameters[1] = kwargs.get("parameters")[1] # margin
            parameters[2] = kwargs.get("parameters")[2] # decrement
            parameters[3] = kwargs.get("parameters")[3] # increment
                    
        if kwargs.get("SILENT") != None:
            SILENT = kwargs.get("SILENT")
        else:
            SILENT = False
                
        ########## BOUNDARIES ####################
        walls = []
        if kwargs.get("walls") != None:
            walls = kwargs.get("walls")
            
        print(walls.vertices_number-1, "walls initialized")
            
        t = 0.0
        t_print = 0.0
        t_list = []
        
        while (t<=t_end):
            
            #print(t, t_end, t_step, parameters)
            
            if ADAPTIVE == True:
                
                X1 = self.evolve(X, walls, t_step)
                X2 = self.evolve(self.evolve(X, walls, 0.5*t_step), walls, 0.5*t_step)

                delta = np.linalg.norm(X1 - X2) # [:] for instance of Variable class TODO!!!! FOR ANY VECTORS

                t_step = self.adapt(t_step, delta, parameters)
            
            X = self.evolve(X, walls, t_step)
            
            if (t_print >= (t_end / float(frames)) ):
              
                self.make_snapshot(X, output)
                t_print = 0.0
                
                if (SILENT==False):
                    print(t,"/",t_end)
                   
            t_print = t_print + t_step      
            t = round(t + t_step , 7) # TODO, avoiding error! Could be a problem if t = 0.00000000xxxx -> 0.0
            t_list.append(t_step)
            
            
        return X, t_list

    
    def make_snapshot(self, X, output):
        output.append( X )       
 

    def __str__(self):
        
        s = ""           
        s = s + self.name + "\n"
        s = s + "t_step = " + str(self.t_step) + "\n"
        s = s + "t_end = " + str(self.t_end) + "\n"
        s = s + "frames = "+ str(self.frames)
        
        if self.ADAPTIVE == True:
            s = "Adaptive" + s + "\n"
            s = s + "parameters = [tol, marg, decr, incr] = " + str(self.parameters)      
        
        return s
