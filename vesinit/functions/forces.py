import math
import numpy as np
from . import geometry


def fl(var, i, l0 = 0.66, kl = 0.3):
    """stretching force"""
    
    l_after = geometry.length(var.x(i), var.y(i), var.x(i+1), var.y(i+1))
    l_before = geometry.length(var.x(i), var.y(i), var.x(i-1), var.y(i-1))
    
    f_after_x = -kl*(l_after - l0)/(l_after * l0**2) * (var.x(i) - var.x(i+1))
    f_before_x = -kl*(l_before - l0)/(l_before * l0**2) * (var.x(i) - var.x(i-1))
    
    flx = f_after_x + f_before_x
    
    f_after_y = -kl*(l_after - l0)/(l_after * l0**2) * (var.y(i) - var.y(i+1))
    f_before_y = -kl*(l_before - l0)/(l_before * l0**2) * (var.y(i) - var.y(i-1))
    
    fly = f_after_y + f_before_y
    
    return flx, fly


def fs(var, i, s0 = 314.0, ks = 2000.0):
    """swelling force"""
    
    s = geometry.area(var.x(), var.y()) 
    fsx = -0.5*ks*(abs(s) - s0)/(s0**2) * (var.y(i+1) - var.y(i-1)) * np.sign(s)
    fsy = -0.5*ks*(abs(s) - s0)/(s0**2) * (var.x(i-1) - var.x(i+1)) * np.sign(s)
    return fsx, fsy

####_ANGULAR_FORSES##################

def fb(var, i, kb = 0.05): # was copied from C++ code
    """bending force"""
    
    dx1 = var.x(i+1) - var.x(i)       # x1 - x
    dx2 = var.x(i) - var.x(i-1);      # x - x2
    dx3 = var.x(i+2) - var.x(i+1);    # x3 - x1
    dx4 = var.x(i-1) - var.x(i-2);    # x2 - x4
    dy1 = var.y(i+1) - var.y(i)       # y1 - y
    dy2 = var.y(i) - var.y(i-1);      # y - y2
    dy3 = var.y(i+2) - var.y(i+1);    # y3 - y1
    dy4 = var.y(i-1) - var.y(i-2);    # y2 - y4

    # length
    l1 = math.sqrt(dx1*dx1 + dy1*dy1);
    l2 = math.sqrt(dx2*dx2 + dy2*dy2);
    l1_inv = 1.0 / l1;
    l2_inv = 1.0 / l2;
    l3_inv = 1.0 / math.sqrt(dx3*dx3 + dy3*dy3);
    l4_inv = 1.0 / math.sqrt(dx4*dx4 + dy4*dy4);

    temp = 0.0

    # trigonometrics
    costheta1 = (dx1*dx2 + dy1*dy2) * l1_inv * l2_inv;
    costheta2 = (dx3*dx1 + dy3*dy1) * l1_inv * l3_inv;
    costheta3 = (dx2*dx4 + dy2*dy4) * l2_inv * l4_inv;

    # trigonometrics derivatives
    temp = 1.0 + costheta1;
    kkb1 = kb / (temp*temp);
    temp = 1.0 + costheta2;
    kkb2 = kb / (temp*temp);
    temp = 1.0 + costheta3;
    kkb3 = kb / (temp*temp);
    l13_inv = l1_inv*l1_inv*l1_inv;
    l23_inv = l2_inv*l2_inv*l2_inv;
    dcos1dx = \
        (dx1 - dx2) * l1_inv * l2_inv + (dx1*dx2 + dy1*dy2)*dx1 * l13_inv * l2_inv - \
        (dx1*dx2 + dy1*dy2)*dx2 * l1_inv * l23_inv;
    dcos2dx = -dx3 * l3_inv * l1_inv + (dx3*dx1 + dy3*dy1)*dx1 * l3_inv * l13_inv;
    dcos3dx = dx4 * l2_inv * l4_inv - (dx2*dx4 + dy2*dy4)*dx2 * l23_inv * l4_inv;
    dcos1dy = \
        (dy1 - dy2) * l1_inv * l2_inv + (dx1*dx2 + dy1*dy2)*dy1 * l13_inv * l2_inv - \
        (dx1*dx2 + dy1*dy2)*dy2 * l1_inv * l23_inv;
    dcos2dy = -dy3 * l3_inv * l1_inv + (dx3*dx1 + dy3*dy1)*dy1 * l3_inv * l13_inv;
    dcos3dy = dy4 * l2_inv * l4_inv - (dx2*dx4 + dy2*dy4)*dy2 * l23_inv * l4_inv;

            #bending force

    fbx = kkb1*dcos1dx + kkb2*dcos2dx + kkb3*dcos3dx;
    fby = kkb1*dcos1dy + kkb2*dcos2dy + kkb3*dcos3dy;
    return fbx, fby


def fr(var, i, segm, lr = 1.0, kr = 1.0):
    """repulsive force from obstacle
    obstacle = Segment o---------o
    potential = hyperbola + step"""
    
    (lx, ly) = (None, None)
    vctr = segm.vector_from_segment_to_point(var.x(i), var.y(i))
    
    if (segm.is_point_on_segment(var.x(i), var.y(i))==True) and \
       geometry.vector_length( vctr[0], vctr[1] ) < lr:
        lx, ly = vctr
    
    if segm.is_point_on_segment(var.x(i), var.y(i))==False:
        
        vctr1 = segm.vector_from_point1(var.x(i), var.y(i)) 
        vctr2 = segm.vector_from_point2(var.x(i), var.y(i))
        
        if geometry.vector_length( vctr1[0], vctr1[1] ) < geometry.vector_length( vctr2[0], vctr2[1] ):
            vctr = vctr1
        else:
            vctr = vctr2

        if geometry.vector_length( vctr[0], vctr[1] ) < lr:
            lx, ly = vctr    
    
    if (lx, ly) != (None, None):        
        norm = math.sqrt(lx**2 + ly**2)
        
        frx = kr * np.sign(lx) * (lr/norm)
        fry = kr * np.sign(ly) * (lr/norm)
        
        return frx, fry
    
    else:
        return 0.0, 0.0
    
    
    
def fr_attraction(var, i, segm, lr = 1.0, kr = 1.0):
    """repulsive-attractive force from obstacle
    obstacle = Segment o---------o
    potential = hyperbola + step + canal"""
    
    vctr = segm.vector_from_segment_to_point(var.x(i), var.y(i))
    
    if segm.is_point_on_segment(var.x(i), var.y(i))==True:
        lx, ly = vctr
    
    if segm.is_point_on_segment(var.x(i), var.y(i))==False:
        
        vctr1 = segm.vector_from_point1(var.x(i), var.y(i)) 
        vctr2 = segm.vector_from_point2(var.x(i), var.y(i))
        
        if geometry.vector_length( vctr1[0], vctr1[1] ) < geometry.vector_length( vctr2[0], vctr2[1] ):
            vctr = vctr1
        else:
            vctr = vctr2
        
        lx, ly = vctr
            
    norm = math.sqrt(lx**2 + ly**2)                       #     ^ \
                                                          #     | \ 
    sgn = np.sign(lr - geometry.vector_length(lx, ly) )   #     |  \
                                                          #     |   `-|
    frx = kr * np.sign(lx) * (lr/norm) * sgn              #     ------|--______------->
    fry = kr * np.sign(ly) * (lr/norm) * sgn              #     |     |_/ 
        
    return frx, fry
   
    

def fp(x1, y1, x2, y2, lp = 1.0, kp = 1.0):
    """repulsive force between two points
    potential = hyperbola + step"""
    
    (lx, ly) = (None, None)
    
    vctr = geometry.vector_from_pnt1_to_pnt2( x2, y2, x1, y1)
    if geometry.vector_length( vctr[0], vctr[1] ) < lp:  
        lx, ly = vctr   
    
    if (lx, ly) != (None, None):        
        norm = math.sqrt(lx**2 + ly**2)
        
        fpx = kp * np.sign(lx) * (lp/norm)
        fpy = kp * np.sign(ly) * (lp/norm)

        return fpx, fpy   
    
    else:
        return 0.0, 0.0