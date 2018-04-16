from . import forces
from .. import shapes
from .. import tools


def fun_with_obstacles(var, walls = None, constants = None, **kwargs):
    """
    Vesicle in a space with an obstacle.

    Nodes of vesicle are being acted by forces of stretching (fl),
    swelling (fs), bending (fb) and repulsive force from obstacle (fr).

    Parameters
    ----------
    var : `Variable`
        Initial x, y coordinates and vx, vy velocities of nodes.
    walls : list of `Polygon`, `optional`
        Obstacle. Default = None (free space).
    constants: `dict`, `optional`
        Constants for fp and fr.
        If not given, loaded from "constants_for_fun_with_obstacles.txt"
    **kwargs
        Arbitrary keyword arguments.

    Returns
    -------
    F : `Variable`
        Evolved x, y coordinates and vx, vy velocities of nodes.
    """
    

    if constants == None:   
        
        constants = tools.load_constants_from_file("constants_for_fun_with_obstacles.txt")
        print("constants are not specified"+"\n"+"load from 'constants_for_fun_with_obstacles.txt'")
        
    else:
        
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
        
        
        ##########   W A L L S #############################
        (frx, fry) = (0.0, 0.0)     
        
        if len(walls) != 0:
            for wall in walls:
                for j in range(wall.vertices_number-1):
                    segment_current = shapes.Segment(wall.vertices[j], wall.vertices[j+1])
                    frx_, fry_ = forces.fr(var, i, segment_current, lr, kr)
                    frx = frx + frx_
                    fry = fry + fry_

            
        ########## STRETCHING, SWELLING, BENDING ###########
        flx, fly = forces.fl(var, i, l0, kl)
        fsx, fsy = forces.fs(var, i, s0, ks)
        fbx, fby = forces.fb(var, i, kb)
        
        (force_x, force_y) = (flx + fsx + fbx + frx , fly + fsy + fby + fry)
                      
        # x - velocity
        F.X[i + 2*F.N] = (1/mass)*force_x - betta*var.vx(i)
        
        # y - velocity
        F.X[i + 3*F.N] = (1/mass)*force_y - betta*var.vy(i)
        
    return F