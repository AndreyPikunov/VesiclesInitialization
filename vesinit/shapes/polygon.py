import numpy as np
import matplotlib.pyplot as plt
import math

from .. import functions

class Polygon:
    
    def __init__(self, vertices): # vertices show go in a proper order
        
        self.vertices_number = len(vertices) + 1 # WE HAVE ONE DOUBLE NODE 
        self.vertices = np.array( np.vstack((vertices, vertices[0,:])) )
    
    
    def perimeter(self):
        return functions.geometry.perimeter(self.vertices[:,0], self.vertices[:,1])
    
    def area(self):
        return functions.geometry.area(self.vertices[:,0], self.vertices[:,1])
    
    def reduced_area(self):
        area_max = (1 / (4 * math.pi)) * self.perimeter**2
        return self.area() / area_max
    
    def centroid(self):
        return functions.geometry.centroid(self.vertices[0:-1, 0], self.vertices[0:-1, 1])
                        
    def resize(self, ratio):
        xc, yc = self.centroid()
        (vert_x, vert_y) = (self.vertices[:,0] - xc , self.vertices[:,1] - yc)
        (vert_x, vert_y) = (vert_x*ratio, vert_y*ratio)
        (vert_x, vert_y) = (vert_x + xc, vert_y + yc)
        vertices_new = np.array([vert_x, vert_y]).transpose()    
        return Polygon(vertices_new[:-1,:])    
    
    ''' TODO
    def margin(self, value):
        pass
    '''    
        
    def make_nodes(self, nodes_number):
        
        l0 = self.perimeter() / nodes_number
        
        nodes = np.empty((0,2))
        
        i = 0 # vertices
        
        x_current = 0.0
        y_current = 0.0
                          
        delta = l0
        
        while i < (self.vertices_number-1):
            
            # x = x0 + q * alpha
            # y = y0 + p * alpha
            q = self.vertices[i+1,0] - self.vertices[i,0]
            p = self.vertices[i+1,1] - self.vertices[i,1]
            
            norma = math.sqrt(q**2 + p**2)
            q = q / norma
            p = p / norma

            x_current = self.vertices[i,0] + q * (delta - l0) #PSEUDO STEP BACK
            y_current = self.vertices[i,1] + p * (delta - l0)
            
            
            #  -> & <- | => inside
            #  -> & -> | => outside
            while ((self.vertices[i,0] - (x_current + q*l0)) * (self.vertices[i+1,0] - (x_current + q*l0)) + \
            (self.vertices[i,1] - (y_current + p*l0)) * (self.vertices[i+1,1] - (y_current + p*l0))) <= 0: # inside segment
                
                x_current = x_current + q*l0
                y_current = y_current + p*l0
                
                nodes = np.vstack((nodes, [[x_current, y_current]]))
                
                delta = 0.0
                                  
            if ((self.vertices[i,0] - (x_current + q*l0)) * (self.vertices[i+1,0] - (x_current + q*l0)) + \
            (self.vertices[i,1] - (y_current + p*l0)) * (self.vertices[i+1,1] - (y_current + p*l0))) > 0: # going outside
                
                delta = l0 - functions.geometry.length(x_current, y_current, self.vertices[i+1,0], self.vertices[i+1,1])
            
            i = i + 1
        
        return Polygon(nodes) # FIX BUG moves origin node by 1
    
    
    def draw(self): 
        plt.axis('equal')
        plt.plot(self.vertices[:,0],self.vertices[:,1],'-ks')
        plt.plot(self.vertices[0,0], self.vertices[0,1],'ow')
        #plt.show()