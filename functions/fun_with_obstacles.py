from python_packages.functions.forses import *
from python_packages.shapes.segment import *
from python_packages.tools.load_constants_from_file import *

def fun_with_obstacles(var, **kwargs):
    
    if kwargs.get("walls") != None:
        walls = kwargs.get("walls")
    else:
        print("walls are not given!"+"\n"+"EXIT")
        return

    if kwargs.get("constants") == None:   
        
        constants = load_constants_from_file("constants_for_fun_with_obstacles.txt")
        print("constants are not specified"+"\n"+"load from 'constants_for_fun_with_obstacles.txt'")
        
    else:
        constants = kwargs.get("constants")
        
        mass = constants['mass']
        betta = constants['betta']

        lr = constants['lr']
        kr = constants['kr']
        
        kl = constants['kl']
        l0 = constants['l0']
        
        ks = constants['ks']
        s0 = constants['s0']
        
        kb = constants['kb']
    
        
    F = var*0
    
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
            frx_, fry_ = fr(var, i, segment_current, lr, kr)
            frx = frx + frx_
            fry = fry + fry_      
        '''
        l0 = 0.66    k = 0.3
        s0 = 314.0   ks = 2000.0
        kb = 0.05 
        '''        
        flx, fly = fl(var, i, l0, kl)
        fsx, fsy = fs(var, i, s0, ks)
        fbx, fby = fb(var, i, kb)
        
        (force_x, force_y) = (flx + fsx + fbx + frx , fly + fsy + fby + fry)
                      
        # x - velocity
        F.X[i + 2*F.N] = (1/mass)*force_x - betta*var.vx(i)
        
        # y - velocity
        F.X[i + 3*F.N] = (1/mass)*force_y - betta*var.vy(i)
        
    return F