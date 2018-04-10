import numpy as np
import matplotlib.pyplot as plt
import math

from python_packages.functions import *

class Polygon:
    
    def __init__(self, vertices): # vertices show go in a proper order
        
        self.vertices_number = len(vertices) + 1 # WE HAVE ONE DOUBLE NODE 
        self.vertices = np.array(
            [np.hstack((vertices[:,0], vertices[0,0])),\
             np.hstack((vertices[:,1], vertices[0,1]))])
        self.vertices = self.vertices.transpose()
        
    
    def perimeter(self):
        return perimeter(self.vertices[:,0], self.vertices[:,1])
    
    def area(self):
        return area(self.vertices[:,0], self.vertices[:,1])
 

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
                
                delta = l0 - length(x_current, y_current, self.vertices[i+1,0], self.vertices[i+1,1])
            
            i = i + 1
        
        return Polygon(nodes)
    
    def draw(self): 
        plt.axis('equal')
        plt.plot(self.vertices[:,0],self.vertices[:,1],'-ks')
        plt.plot(self.vertices[0,0], self.vertices[0,1],'or')
        #plt.show()