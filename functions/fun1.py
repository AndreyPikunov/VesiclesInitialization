from python_packages.functions.forses import *


def fun1(var): # put Variable here
    
    F = var*0
    mass = 10.0 # mass
    betta = 0.5 # friction coefficient
    
    
    for i in range(F.N):
        
        # x - coordinate
        F.X[i] = var.vx(i)
        # y - coordinate
        F.X[i + F.N] = var.vy(i)
        
        # x - velocity
        force_x = flx(var, i, l0=0.66, kl = 0.3) + \
        fsx(var, i, s0=314.0, ks = 200.0)  + \
        flx_2(var, i, l0=1.32, kl = 10.0) + \
        fbx(var, i, kb=0.5) # kb = 0.05
        
        F.X[i + 2*F.N] = (1/mass)*force_x - betta*var.vx(i)
        
        # y - velocity
        force_y = fly(var, i, l0=0.66, kl = 0.3) + \
        fsy(var, i, s0=314.0, ks = 200.0)  + \
        fly_2(var, i, l0=1.32, kl = 10.0) + \
        fby(var, i, kb=0.5)
        
        F.X[i + 3*F.N] = (1/mass)*force_y - betta*var.vy(i)
        
    return F
