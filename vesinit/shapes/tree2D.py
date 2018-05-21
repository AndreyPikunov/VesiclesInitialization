import numpy as np
import matplotlib.pyplot as plt

from imageio import imwrite

from .tree1D import *

class Tree2D(Tree1D):
    
    def __init__(self, basis_tree_1D = Tree1D(), r_cap = 10, a = 0.33): # 1D tree MUST BE CROPPED

        self.r_cap = r_cap
        self.a = a
        
        self.m = basis_tree_1D.x[-1]*2
        self.n = basis_tree_1D.y[-1] + 30 # +30 for safety
        
        self.A = np.zeros((self.m, self.n) , dtype=bool)

        self.depth = basis_tree_1D.depth
        
        self.x = basis_tree_1D.x # coordinates of nodes
        self.y = basis_tree_1D.y

        for i in range(1, self.depth+1):
            for j in range(1,2**(i-1)+1):
                n_n = self.node_number(i,j)
                p_n = self.parent_number(i,j)
                self.draw_line_between(n_n, p_n, i)

    
    def radius(self, i): # r_cap - radius of the smallest cappilar
        if (i>=self.depth+1):
            return self.r_cap
        else:
            return int(round(((2**(self.a))*self.radius(i+1))))
    
    def radius_current(self, i, ratio): # for drawing decreasing vessel, 0<= ratio <=1 
        if (i==self.depth+1): #capillar
            return int(round(self.radius(i))) # no decreasing
        else:
            return int(round(self.radius(i) - ratio*(self.radius(i) - self.radius(i+1))))
        
    def l(self, x1,y1, x2,y2): # distance between two points
        return ( (x1-x2)**2 + (y1-y2)**2 )**(1/2)

    def create_structure_element(self,rad): #rad = radius of vessel in pixels;
                                            #structure element is kinda brush shape, here it is circle
                                            
        E = np.zeros((2*rad,2*rad) , dtype=bool)
        for i in range(2*rad):
            for j in range(2*rad):
                if ( (i+0.5-rad)**2 + (j+0.5-rad)**2 <= (rad**2)): # +0.5 because of shift of meshes of circle and array
                    E[i,j] = True                
        return E


    def draw_line_between(self, child, parent, level): # draw line from parent to child on i-th level

        slope = (self.y[child] - self.y[parent])/(self.x[child] - self.x[parent])
        intercept = self.y[child] - slope * self.x[child]
        L = self.l(    self.x[child], self.y[child],     self.x[parent], self.y[parent]   ) # distance between parent and child


        #print("draw line between (", x[child], ", ", y[child], ") and (", x[parent], ", ", y[parent], ")")

        if (abs(slope)<=1): # draw alongwise X-axis
            for ix in range(self.x[parent], self.x[child]+1):
                iy = int(round(slope*ix + intercept))

                #print("      Points: ", ix, iy)

                l_current = self.l(self.x[parent], self.y[parent], ix,iy)
                r_current = self.radius_current(level, l_current/L)

                element = self.create_structure_element(r_current)

                yl = iy - r_current
                yr = iy + r_current

                if ix>=r_current:
                    xl = ix - r_current
                    xr = ix + r_current
                    self.A[xl:xr, yl:yr] = self.A[xl:xr, yl:yr] + element

                else:
                    self.A[ix, yl:yr].fill(True) # FIX IT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        else: # draw alongwise Y-axis
            for iy in range(self.y[parent], self.y[child]+1): # <- IF WE ARE GOING DOWN?!?!??!?!?!              
                ix = int(round((iy - intercept)/slope))

                #print("      Points: ", ix, iy)

                l_current = self.l(self.x[parent], self.y[parent], ix,iy)
                r_current = self.radius_current(level, l_current/L)

                element = self.create_structure_element(r_current)

                xl = ix - r_current
                xr = ix + r_current

                if iy>=r_current:
                    yl = iy - r_current
                    yr = iy + r_current
                    self.A[xl:xr, yl:yr] = self.A[xl:xr, yl:yr] + element

                else:
                    self.A[xl:xr, iy].fill(True)  

                    
    
    def reflect(self):
        for i in range(self.m//2):
            self.A[self.m-1 - i, :] = self.A[i,:]

            
    def save_2D_tree(self, file_name = 'new_tree'):

        np.savetxt(file_name+'_MASK.txt', self.A)

        imwrite(file_name+'.bmp', self.A.transpose()^True)

        '''
        #MAKING HEART
        A_1 = np.array(self.A)
        A_1[100:-100 , :].fill(False)
        imageio.imwrite(file_name+'_1.bmp', True^A_1.transpose())

        A_2 = np.array(A_1)
        A_2.fill(True) # If Array is False everywhere saving is impossible
        A_2[0,0] = False
        imageio.imwrite(file_name+'_2.bmp', A_2.transpose())
        '''
        
    def draw(self):
        fig = plt.figure(figsize=(18,12))
        plt.imshow(self.A.transpose(), cmap=plt.cm.BuPu_r)
