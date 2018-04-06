class Solver():
    
    def __init__(self, t_step = 1.0, t_end=100.0, frames=10, name=None):
        self.t_step = t_step
        self.t_end = t_end
        self.frames = frames  
        self.name = name if name!=None else "DummySolver"
    
    def function(self, X):
        pass
    
    def evolve(self, X, t_step = None):
        pass
    
    def simulate(self, X, output, t_step = None, t_end = None, frames = None, SILENT = True):
        
        if t_step == None:
            t_step = self.t_step
        if t_end == None:
            t_end = self.t_end
        if frames == None:
            frames = self.frames
        
        t = 0.0
        t_print = 0.0
 
        
        while (t<=t_end):
            
            X = self.evolve(X, t_step)
            
            if (t_print >= (t_end / float(frames)) ):
                
                #print(t_print,"/",(t_end / float(frames)))
                
                self.make_snapshot(X, output)
                t_print = 0.0
                
                if (SILENT==False):
                    print(t,"/",t_end)
                   
            t_print = t_print + t_step      
            t = round(t + t_step , 7) # TODO, avoiding error!
            
            
        return t_list #X
    
    def make_snapshot(self, X, output):
        output.append( X )       
    
    def __str__(self):
        return self.name + "\n" \
        "t_step = " + str(self.t_step) + "\n" + \
        "t_end = " + str(self.t_end) + "\n" + \
        "frames = "+ str(self.frames)