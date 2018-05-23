import numpy as np
import matplotlib.pyplot as plt
import math

import sys
sys.path.append('/PATH/TO/VESINIT/PACKAGE')

import vesinit.shapes as shp
import vesinit.solvers as slv
import vesinit.functions as fnc
import vesinit.tools as tls
###########################

#### V E S I C L E ####
vesicle = np.loadtxt('vesicle_shape.txt')

sh_x = (vesicle[:,0])*0.5 #deform a bit
sh_y = (vesicle[:,1])

v_x = sh_x*0.0
v_y = sh_x*0.0

V = shp.Variable(sh_x, sh_y, v_x, v_y)

#### O B S T A C L E ####
vert = np.array([[-10,-10],
                [-10,10],
                [-15,0]])
pol = shp.Polygon(vert)


#### S I M U L A T I O N ####
AdaptiveEM = slv.EulerMethod(ADAPTIVE = True,
                     function = fnc.fun_with_obstacles)
out = AdaptiveEM.simulate( X = V, walls = [pol], SILENT = False)
print("Area_initial =", fnc.geometry.area(V.x(),V.y()) ,"| Area_final =", fnc.geometry.area(out[-1].x(), out[-1].y()) )

#### P R I N T I N G ####
for i in range(len(out)):
    out_i = out[i]
    plt.clf() 
    pol.draw()
    plt.plot(out_i.x(),out_i.y(),'.-r')
    plt.savefig("pic{0:04d}.png".format(i))

print("D O N E")
