from python_packages.functions.forses import *
#from python_packages.shapes.line import *
from python_packages.shapes.segment import *


def fun_with_obstacles(var, walls): # put Variable here
    
    F = var*0
    mass = 10.0 # mass
    betta = 1.0 # friction coefficient    1.0
    
    for i in range(F.N):
        
        # x - coordinate
        F.X[i] = var.vx(i)
        # y - coordinate
        F.X[i + F.N] = var.vy(i)
        
        
        (frx, fry) = (0.0, 0.0)        
        '''
        lr = 1.0
        kr = 1.0
        '''  
        for j in range(walls.vertices_number-1):
            segment_current = Segment(walls.vertices[j], walls.vertices[j+1])
            #print(fr(var, i, segment_current, lr = 1.0, kr = 1.0))
            frx_, fry_ = fr(var, i, segment_current, lr = 1.0, kr = 1.0)
            frx = frx + frx_
            fry = fry + fry_      
        '''
        l0 = 0.66    k = 0.3
        s0 = 314.0   ks = 2000.0
        kb = 0.05 
        '''        
        flx, fly = fl(var, i, l0=0.66, kl = 3.0)
        fsx, fsy = fs(var, i, s0=314.0, ks = 200.0)
        fbx, fby = fb(var, i, kb=5.0)
        
        (force_x, force_y) = (flx + fsx + fbx + frx , fly + fsy + fby + fry)
                      
        # x - velocity
        F.X[i + 2*F.N] = (1/mass)*force_x - betta*var.vx(i)
        
        # y - velocity
        F.X[i + 3*F.N] = (1/mass)*force_y - betta*var.vy(i)
        
    return F