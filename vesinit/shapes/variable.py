import numpy as np

class Variable():
    
    def __init__(self, x_list=None, y_list=None, vx_list=None, vy_list=None,
                 polygon=None):

        if hasattr(x_list, '__len__')==True: # MANY POINTS
            self.N = len(x_list)
            self.X = np.array(x_list, dtype=float)
            self.X = np.append(self.X, y_list)
            self.X = np.append(self.X, vx_list)
            self.X = np.append(self.X, vy_list) 
            
        if hasattr(x_list, '__len__')==False: # 1 POINT
            self.X = np.array([x_list, y_list, vx_list, vy_list])
            
        if polygon!=None: # FROM POLYGON
            print("Created from polygon")
            x = (polygon.vertices[:-1,0])
            y = (polygon.vertices[:-1,1])
            vx = vy = x*0.0
            self.__init__(x_list=x, y_list=y, vx_list=vx, vy_list=vy, polygon=None)
     

    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, i):
        return self.X[i]
    
    def __add__(self, other):
        result = Variable([],[],[],[])
        result.X = self.X + other.X
        result.N = self.N
        return result
    
    def __sub__(self, other):
        result = Variable([],[],[],[])
        result.X = self.X - other.X
        result.N = self.N
        return result
        
    def __mul__(self, value):
        """FOR SCALARS ONLY"""
        result = Variable([],[],[],[])
        result.X = self.X * value
        result.N = self.N
        return result
    
    def __rmul__(self, value):
        """FOR SCALARS ONLY"""
        result = Variable([],[],[],[])
        result.X = self.X * value
        result.N = self.N
        return result        
        
        
    def x(self, i=None):
        if i==None:
            return self.X[0 : self.N]
        else:
            j = i % self.N
            return self.X[j]
    
    def y(self, i=None):
        if i==None:
            return self.X[self.N : 2*self.N]
        else:
            j = i % self.N
            return self.X[j+self.N]
        
    def vx(self, i=None):
        if i==None:
            return self.X[2*self.N : 3*self.N]
        else:
            j = i % self.N
            return self.X[j+2*self.N]
    
    def vy(self, i=None):
        if i==None:
            return self.X[3*self.N : 4*self.N]
        else: 
            j = i % self.N
            return self.X[j+3*self.N]
        