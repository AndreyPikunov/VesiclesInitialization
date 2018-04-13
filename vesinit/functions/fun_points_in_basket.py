from . import forces
from .. import shapes
from .. import tools


def fun_points_in_basket(var, walls = None, constants = None, **kwargs):
    """
    Massive points flying in a space with an obstacle.

    Points interact between each other with point-to-point force (fp)
    and with obstacle with repulsive force (fr).

    Parameters
    ----------
    var : `Variable`
        Initial x, y coordinates and vx, vy velocities of points.
    walls : `Polygon`, `optional`
        Obstacle. Default = None (free space).
    constants: `dict`, `optional`
        Constants for fp and fr.
        If not given, loaded from "constants_for_fun_points_in_basket.txt"
    **kwargs
        Arbitrary keyword arguments.

    Returns
    -------
    F : `Variable`
        Evolved x, y coordinates and vx, vy velocities of points.
    """

    
    if constants == None:   
        
        constants = tools.load_constants_from_file("constants_for_fun_points_in_basket.txt")
        print("constants are not specified"+"\n"+"load from 'constants_for_fun_points_in_basket.txt'")
        
    else:

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

        
        ########     W A L L S ###########################
        (frx, fry) = (0.0, 0.0)
        
        if walls != None:
            
            for j in range(walls.vertices_number-1):
                segment_current = shapes.Segment(walls.vertices[j], walls.vertices[j+1])
                frx_, fry_ = forces.fr(var, i, segment_current, lr, kr)
                frx = frx + frx_
                fry = fry + fry_   

        ########     B O D Y - B O D Y ###################
        (fpx, fpy) = (0.0, 0.0)
        for j in range(F.N):
            if i!=j:
                fpx_, fpy_ = forces.fp(var.x(i), var.y(i),
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