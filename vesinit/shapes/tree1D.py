import math
import numpy as np
import matplotlib.pyplot as plt

class Tree1D:
     
    def __init__(self, depth = 4, l_1 = 300, b = 0.2, phi_1 = 1.0, c = 0.66, CROP = True):
        
        self.depth = depth
        
        self.x = np.zeros(2**self.depth, dtype=int) # coordinates of nodes
        self.y = np.zeros(2**self.depth, dtype=int)
        
        self.l_1 = l_1
        self.b = b
        
        self.phi_1 = phi_1
        self.c = c
        
        self.CROP = CROP
        
        
        
        (self.x[0], self.y[0]) = (0, 0) # feeding point

        (self.x[1], self.y[1]) = (self.x[0] + self.length(1), self.y[0])

        for i in range(1+1,self.depth+1):
            for j in range(1,2**(i-1)+1):
                
                n_n = self.node_number(i,j)
                p_n = self.parent_number(i,j)
                
                self.x[n_n] = self.x[p_n] + round(self.length(i) * math.cos(self.phi(i)))
                self.y[n_n] = self.y[p_n] + round((2*(0.5 - j%2)) * self.length(i) * math.sin(self.phi(i))) # 2*(j%2-0.5) - child up or down 

        # cropping tree for future miraging

        if CROP:

            self.x = self.x - self.length(1)/2 # avoiding twofold length of artery and vein BY combining them
            (self.x[0], self.y[0]) = (0, 0) # return feeding point

            i = self.depth
            for j in range(1,2**(i-1)+1): # avoiding twofold length of smallest capillars
                
                n_n = self.node_number(i,j)
                p_n = self.parent_number(i,j)
                
                self.x[n_n] = self.x[p_n] + round(self.length(i) * math.cos(self.phi(i))/2)
                self.y[n_n] = self.y[p_n] + round((2*(0.5 - j%2)) * self.length(i) * math.sin(self.phi(i))/2) # 2*(j%2-0.5) - child up or down 

            self.y = self.y + abs( self.y[ self.node_number(self.depth,1) ]  ) + 30 # +30 for safety

            self.x = self.x.astype(int)
            self.y = self.y.astype(int)

        #print("Hey, I'm the Tree!!1")


        
        
    def node_number(self, i,j): # i - depth level, j - number of the node of the i-th level
        return int(2**(i-1)+(j-1))

    
    def parent_number(self, i,j): 
        return int(self.node_number( (i-1), math.ceil(j/2) ))

    
    def length(self, i): # length of vessel of the i-th generation
        if (i==1):
            return self.l_1
        else:
            return (2**(-self.b))*self.length(i-1)
        
        
    def phi(self, i): # angle of branching of the i-th generetion
        
        if (i==1):
            return self.phi_1
        else:
            return (self.c * self.phi(i-1))
        
        
    def save(self, file_name = 'new_tree_1D'):
        
        f = open(file_name+'.txt', 'w')

        f.write("depth "+str(self.depth)+"\n")
        
        f.write("l_1 "+str(self.l_1)+"\n")
        f.write("b "+str(self.b)+"\n")
        
        f.write("phi_1 "+str(self.phi_1)+"\n")
        f.write("c "+str(self.c)+"\n")
        
        f.write("CROP "+str(self.CROP)+"\n")
    
        f.write("x y"+"\n")
        for i in range(len(self.x)):
            f.write(str(self.x[i])+" "+str(self.y[i])+"\n")

        f.close()
        print("saved.")
        
        
    def load(self, file_name):
        
        f = open(file_name, 'r')
        
        self.depth = int(f.readline().split()[1])
        
        self.l_1 = float(f.readline().split()[1])     
        self.b = float(f.readline().split()[1])
        
        self.phi_1 = float(f.readline().split()[1])
        self.c = float(f.readline().split()[1])
        
        self.CROP = bool(f.readline().split()[1])
        
        self.x = np.zeros(2**self.depth, dtype=int) # coordinates of nodes
        self.y = np.zeros(2**self.depth, dtype=int)
        
        x_y = f.readline() # nothing
        print(x_y)
        
        i = 0
        for line in f:
            x = int(line.split()[0])
            y = int(line.split()[1])
            (self.x[i], self.y[i]) = (x, y)
            i = i+1
              
        print('loaded.')
            
    
    def draw(self):
        fig = plt.figure()
        ax = plt.axes()
        plt.axis('equal');
        plt.plot(self.x, self.y, '.')