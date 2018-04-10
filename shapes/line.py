import matplotlib.pyplot as plt
import numpy as np

class Line: # ax + by + c = 0 + normalizing
    
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
        norma = math.sqrt(self.a**2 + self.b**2) # Нормировка!
        self.a = self.a / norma
        self.b = self.b / norma
        self.c = self.c / norma
            
    def draw(self):
        
        if (self.a==0) and (self.b!=0): # horizontal
            plt.plot([-40,40],[-self.c/self.b, -self.c/self.b],':k')
            
        if (self.a!=0) and (self.b==0): # vertical
            plt.plot([-self.c/self.a, -self.c/self.a],[-40,40],':k')
            
        if (self.a!=0) and (self.b!=0): # other cases
            x = np.array([-40,40])
            y = (self.c - self.a * x) / self.b
            plt.plot(x,y,':k')