from python_packages.functions.forses import *
from python_packages.shapes.line import *
from python_packages.shapes.segment import *


def fun_with_obstacles(var, walls): # put Variable here
    
    F = var*0
    mass = 10.0 # mass
    betta = 1.0 # friction coefficient    
    
    for i in range(F.N):
        
        # x - coordinate
        F.X[i] = var.vx(i)
        # y - coordinate
        F.X[i + F.N] = var.vy(i)
        
        
        frx = 0.0
        fry = 0.0
        
        for j in range(walls.vertices_number-1):
            segment_current = Segment(walls.vertices[j], walls.vertices[j+1])
            frx = frx + f_repul_x(var, i, segment_current, lr = 3.0, kr = 1.0)
            fry = fry + f_repul_y(var, i, segment_current, lr = 3.0, kr = 1.0)
        
        '''
        l0 = 0.66    k = 0.3
        s0 = 314.0   ks = 2000.0
        kb = 0.05
        '''
        
        # x - velocity
        force_x = flx(var, i, l0=0.66, kl = 3.0) + fsx(var, i, s0=314.0, ks = 200.0) + fbx(var, i, kb=0.5) + frx
        F.X[i + 2*F.N] = (1/mass)*force_x - betta*var.vx(i)
        
        # y - velocity
        force_y = fly(var, i, l0=0.66, kl = 3.0) + fsy(var, i, s0=314.0, ks = 200.0) + fby(var, i, kb=0.5) + fry
        F.X[i + 3*F.N] = (1/mass)*force_y - betta*var.vy(i)
        
    return F