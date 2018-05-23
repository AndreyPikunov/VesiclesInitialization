from .. import functions
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
            
        norma = math.sqrt(self.a**2 + self.b**2) # normilizing for safety!
        self.a = self.a / norma
        self.b = self.b / norma
        self.c = self.c / norma
            
        
    def is_contain(self, x, y):
        """USE ONLY FOR POINTS ON (INSIDE) THE LINE ax+by+c=0 !!!
        o------x--------------o"""
        return (self.point1[0] - x) * (self.point2[0] - x) + (self.point1[1] - y) * (self.point2[1] - y) <= 0
    
    def vector_from_segment_to_point(self, x, y):     
        return functions.geometry.vector_from_line_to_point(self.a, self.b, self.c, x, y)
    
    def vector_from_point1(self, x, y):
        return functions.geometry.vector_from_pnt1_to_pnt2(self.point1[0], self.point1[1], x, y)
    
    def vector_from_point2(self, x, y):
        return functions.geometry.vector_from_pnt1_to_pnt2(self.point2[0], self.point2[1], x, y)
    
    def point_on_segment(self, x, y):             
        return functions.geometry.point_on_line(self.a, self.b, self.c, x, y)
    
    def is_point_on_segment(self, x, y):
        x_, y_ = self.point_on_segment(x,y)
        return self.is_contain(x_, y_)