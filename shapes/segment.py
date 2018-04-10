from python_packages.functions.geometry import * 
from python_packages.shapes.line import *
import math

class Segment:
    
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        
        if (self.point1[0]==self.point2[0]) and (self.point1[1]!=self.point2[1]): #vertical
            self.a = 1.0
            self.b = 0.0
            self.c = -self.point1[0]
        
        if (self.point1[0]!=self.point2[0]) and (self.point1[1]==self.point2[1]): #horizontal
            self.a = 0.0
            self.b = 1.0
            self.c = -self.point1[1]
                                                 
        if (self.point1[0]!=self.point2[0]) and (self.point1[1]!=self.point2[1]):
            self.a = -(self.point2[1] - self.point1[1])/(self.point2[0] - self.point1[0])
            self.b = 1
            self.c = -self.a * self.point1[0] - self.point1[1]
            
            norma = math.sqrt(self.a**2 + self.b**2) # Нормировка!
            self.a = self.a / norma
            self.b = self.b / norma
            self.c = self.c / norma
        
        
    def is_contain(self, x, y): # WORKS ONLY FOR POINTS ON LINE!!!!
        return (self.point1[0] - x) * (self.point2[0] - x) + (self.point1[1] - y) * (self.point2[1] - y) <= 0
    
    def vector_from_segment_to_point(self, x, y):     
        return vector_from_line_to_point(self.a, self.b, self.c, x, y)
    
    def point_on_segment(self, x, y):             
        return point_on_line(self.a, self.b, self.c, x, y)
    
    def is_point_on_segment(self, x, y):
        x_, y_ = self.point_on_segment(x,y)
        return self.is_contain(x_, y_)