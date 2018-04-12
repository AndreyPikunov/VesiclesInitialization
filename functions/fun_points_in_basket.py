from python_packages.functions.forses import *
from python_packages.shapes.segment import *
from python_packages.tools.load_constants_from_file import *

def fun_points_in_basket(var, **kwargs):
    
    if kwargs.get("walls") != None:
        walls = kwargs.get("walls")
    else:
        print("walls are not given!"+"\n"+"EXIT")
        return
    
    if kwargs.get("constants") == None:   
        
        constants = load_constants_from_file("constants_for_fun_points_in_basket.txt")
        print("constants are not specified"+"\n"+"load from 'constants_for_fun_points_in_basket.txt'")
        
    else:
        constants = kwargs.get("constants")

        mass = constants['mass']
        betta = constants['betta']

        lr = constants['lr']
        kr = constants['kr']

        lp = constants['lp']
        kp = constants['kp']
    
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
        
        ########     W A L L S ###########################
        for j in range(walls.vertices_number-1):
            segment_current = Segment(walls.vertices[j], walls.vertices[j+1])
            frx_, fry_ = fr(var, i, segment_current, lr, kr)
            frx = frx + frx_
            fry = fry + fry_   

        ########     B O D Y - B O D Y ###################
        (fpx, fpy) = (0.0, 0.0)
        for j in range(F.N):
            if i!=j:
                fpx_, fpy_ = fp(var.x(i), var.y(i),
                                var.x(j), var.y(j),
                                lp, kp)
                fpx = fpx + fpx_
                fpy = fpy + fpy_      
        
        (force_x, force_y) = (frx + fpx, fry + fpy)
                      
        # x - velocity
        F.X[i + 2*F.N] = (1/mass)*force_x - betta*var.vx(i)
        
        # y - velocity
        F.X[i + 3*F.N] = (1/mass)*force_y - betta*var.vy(i)
        
    return F