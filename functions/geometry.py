import numpy as np
from math import sqrt

def length(x1,y1,x2,y2):
    return sqrt( (x1-x2)**2 + (y1-y2)**2 )
    
def area(x,y):
    x = np.array(x)
    y = np.array(y)
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def perimeter(x,y):
    pass
