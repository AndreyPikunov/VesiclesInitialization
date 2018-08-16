import numpy as np
import math

def length(x1,y1,x2,y2):
    return math.sqrt( (x1-x2)**2 + (y1-y2)**2 )


def vector_length(x,y):
    return length(x, y, 0.0, 0.0)

    
def area(x,y): # CAN BE NEGATIVE, IMPORTANT!
    x = np.array(x)
    y = np.array(y)
    return 0.5*(np.dot(y,np.roll(x,1))-np.dot(x,np.roll(y,1)))


def perimeter(x,y):
    per = 0.0
    for i in range(-1,len(x)-1):
        per = per + length(x[i],y[i],x[i+1],y[i+1])
    return per


def centroid(x, y):
    return np.mean(x), np.mean(y)


def perpendicular_distance(a, b, c, x0, y0):
    """distance from point (x0, y0) to a line (ax + by + c = 0)"""
    
    nominator = a*x0 + b*y0 + c # CAN BE NEGATIVE, IMPORTANT!
    denominator = math.sqrt(a**2 + b**2)
    return nominator/denominator


def perpendicular_distance_unnormalized(a, b ,c ,x0, y0):
    """unnormilized distance from point (x0, y0) to a line (ax + by + c = 0)"""
    return a*x0 + b*y0 + c
    
    
def point_on_line(a, b, c, x0, y0):
    """projection of point (x0, y0) on line (ax + by + c = 0)"""
    
    nominator1 = b*(b*x0 - a*y0) - a*c
    nominator2 = a*(-b*x0 + a*y0) - b*c
    denominator = a**2 + b**2
    return nominator1/denominator, nominator2/denominator # x and y


def vector_from_line_to_point(a, b, c, x0, y0):
    """vector from point (x0, y0) to line (ax + by + c = 0)"""
    
    nom = a*x0 + b*y0 + c
    denom = math.sqrt(a**2 + b**2)
    return (a/denom)*(nom/denom), (b/denom)*(nom/denom)
    
    
def vector_from_pnt1_to_pnt2(x1,y1, x2,y2):
    return x2-x1, y2-y1