############## O L D  C L A S S, #######################

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from math import sqrt

class Vesicle:
    
    def __init__(self, list_of_nodes = [], kl = 1, l0 = 1, ks = 1, s0 = 1, kb = 1, theta0 = 0): #TODO  change list_of_nodes=[]
        
        self.number_of_nodes = len(list_of_nodes)
        
        self.node = np.empty( (self.number_of_nodes, 2) , dtype=float)
        
        for i in range(self.number_of_nodes):
            self.node[i,0] = list_of_nodes[i].x
            self.node[i,1] = list_of_nodes[i].y
            
        self.kl = kl
        self.l0 = l0
        self.ks = ks
        self.s0 = s0
        self.kb = kb
        self.theta0 = theta0
        
        print("Initialized ",self.number_of_nodes,"-node vesicle.")
        
        
    def area(self):
        x = self.node[:,0]
        y = self.node[:,1]
        return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
    
    def length(self, i):
        return sqrt((self.node[i,0] - self.node[i+1,0])**2 + (self.node[i,1] - self.node[i+1,1])**2)
    
    def perimeter(self):
        p = 0.0
        for i in range(-1,self.number_of_nodes-1): # -1 for i=N=0 and i+1=N+1=1
            p = p + self.length(i)
        return p
    
    
    def draw(self):
        fig = plt.figure#(figsize=(18,12))
        plt.plot(self.node[:,0],self.node[:,1],'-or')
        plt.axis('equal')
        plt.show()
        
    def load(self, file_name = 'vesicle.txt'):
    
        f = open(file_name, 'r')

        self.kl = float(f.readline().split()[1])
        self.l0 = float(f.readline().split()[1])     
        self.ks = float(f.readline().split()[1])
        self.s0 = float(f.readline().split()[1])
        self.kb = float(f.readline().split()[1])
        self.theta0 = float(f.readline().split()[1])

        x_y = f.readline() # nothing
        
        num_lines = sum(1 for line in open(file_name))
        
        self.number_of_nodes = num_lines - 6 - 1 # 6 constants, 1 "x y" line
        
        self.node = np.empty( (self.number_of_nodes, 2) , dtype=float)

        i = 0
        for line in f:
            x = float(line.split()[0])
            y = float(line.split()[1])
            self.node[i,0] = x
            self.node[i,1] = y
            i = i + 1
        
        print("loaded ",self.number_of_nodes,"-node vesicle")
        
    def print_constants(self):
        print("kl = ",self.kl)
        print("l0 = ",self.l0)
        print("ks = ",self.ks)
        print("s0 = ",self.s0)
        print("kb = ",self.kb)
        print("theta0 = ",self.theta0)
        
        
        
###########################################        
    # F O R S E S
        
    def flx(self, i): # -a1*(xi-xi+1) - a2*(xi-xi-1)
        li = self.length(i)
        li_1 = self.length(i-1)
        a1 = self.kl*(li-self.l0)/(li*self.l0**2)
        a2 = self.kl*(li_1-self.l0)/(li_1*self.l0**2)
        return -a1*(self.node[i,0]-self.node[i+1,0]) - a2*(self.node[i,0]-self.node[i-1,0]) # FIX i+1 for i=N
    
    def fly(self, i): # -a1*(yi-yi+1) - a2*(yi-yi-1)
        li = self.length(i)
        li_1 = self.length(i-1)
        a1 = self.kl*(li-self.l0)/(li*self.l0**2)
        a2 = self.kl*(li_1-self.l0)/(li_1*self.l0**2)
        return -a1*(self.node[i,1]-self.node[i+1,1]) - a2*(self.node[i,1]-self.node[i-1,1])

    
    def fsx(self, i): # -a*|yi-1 - yi+1|
        s = self.area()
        a = 0.5*self.ks*(s-self.s0)/(self.s0**2)
        return -a*abs(self.node[i-1,1] - self.node[i+1,1])
    
    def fsy(self, i): # -a*|xi-1 - xi+1|
        s = self.area()
        a = 0.5*self.ks*(s-self.s0)/(self.s0**2)
        return -a*abs(self.node[i-1,0] - self.node[i+1,0])
    
    
    def fbx(self, i): # TODO
        return 0.0
    
    def fby(self,i): # TODO
        return 0.0
    
    
    
    
#############################################################
        # F O R    S O L V E R
   
        
    def create_X(self):
        
        self.X = np.array(self.node[:,0])
        self.X = np.append(self.X, self.node[:,1], axis = 0)
        self.X = np.append(self.X, np.zeros(self.number_of_nodes*2, dtype=float), axis = 0)
