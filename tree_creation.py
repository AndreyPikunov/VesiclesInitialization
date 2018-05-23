import matplotlib.pyplot as plt
import math

import sys
sys.path.append('/PATH/TO/VESINIT/PACKAGE')

import vesinit.shapes as shp
###########################


#### 1D  T R E E ####
tr_1D = shp.Tree1D(depth=3,
                  l_1=300,
                  b=0.2,
                  phi_1=math.pi/12,
                  c=1.4)

#### 2D  T R E E ####
tr_2D = shp.Tree2D(basis_tree_1D=tr_1D,
                  r_cap = 20,
                  a = 0.33)
tr_2D.reflect()
tr_2D.save_2D_tree('new')

print("D O N E")



