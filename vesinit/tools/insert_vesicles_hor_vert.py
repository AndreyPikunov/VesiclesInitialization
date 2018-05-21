import numpy as np
import matplotlib.pyplot as plt
import math

from .. import functions


def load_initial_shape(file_name = 'initial_vesicle_shape.txt'):
    
    sh = np.loadtxt(file_name)

    sh[:,0] = sh[:,0] - np.mean(sh[:,0])
    sh[:,1] = sh[:,1] - np.mean(sh[:,1])

    sh_x = sh[:,0]
    sh_y = sh[:,1]

    return (sh_x, sh_y)


def draw_initial_shape(sh_x, sh_y):
    fig = plt.figure()
    ax = plt.axes()
    plt.axis('equal');
    plt.plot(sh_x,sh_y, '.')


def vessel_area(A):
    return np.sum(A)

def hematocrit(A, sx, sy):
    
    total_rbc_area = 0
    for i in range(len(sx)):
        total_rbc_area = total_rbc_area + functions.geometry.area(sx[i,:], sy[i,:])
    
    return abs(round( total_rbc_area/vessel_area(A) , 2) * 100)


def get_rbc_size(sh_x, sh_y):
    
    w = np.ptp(sh_x)
    h = np.ptp(sh_y)
    
    w = math.ceil(w) + 1 # maybe + 1 safety?
    h = math.ceil(h) + 1
    
    return (w,h)


def load_mask(file_name):
    return np.loadtxt(file_name)

def draw_mask(mask):
    plt.imshow(mask.transpose(), cmap='gray')


def insert_vesicles(sh_x, sh_y, mask = np.full((100,100), True), VERT = True):
   
    (w, h) = get_rbc_size(sh_x, sh_y)
    
    b = np.array(mask, dtype = bool)
    l = [] # [ X_coordinate, Y_coordinate, Inclination ]
    
    inclination = 0.0
    
    if VERT==True:
        (w,h) = (h,w)
        inclination = 3.1416/2.0
        
    for i in range(w//2, b.shape[0] - w//2): #x
        for j in range(h//2, b.shape[1] - h//2):
            if b[i - w//2 : i + w//2 , j - h//2 : j + h//2].all():
                l.append([i, j , inclination])
                b[i - w//2 : i + w//2 , j - h//2: j + h//2].fill(False)
   
    return (l, b)


def insert_vesicles_max(sh_x, sh_y, mask = np.full((100,100), True)):
    '''inserts maximum number of vesicles possible - vert then horiz'''
    
    (l, b) = insert_vesicles(sh_x, sh_y, mask)
    (l_, b) = insert_vesicles(sh_x, sh_y, b, False)
    return (l+l_, b)


def draw_scene(mask, sx, sy):
    
    fig = plt.figure()#(figsize=(18,12))
    draw_mask(mask)
    plt.plot(sx.transpose(),sy.transpose())
    plt.show()
    
    print('Number of vesicles = ', len(sx))
    print('Hematocrit = ', hematocrit(mask, sx, sy))


def create_shapes(l, sh_x, sh_y):
    
    sx = np.empty((len(l),len(sh_x)), dtype=float)
    sy = np.empty((len(l),len(sh_y)), dtype=float)
    
    for i in range( len(l) ):
        
        if l[i][2]==0:         
            sx[i, :] = sh_x + l[i][0]
            sy[i, :] = sh_y + l[i][1]
            
        if l[i][2]==3.1416/2.0:
            sx[i, :] = sh_y + l[i][0]
            sy[i, :] = sh_x + l[i][1]
            
    return (sx, sy)


def save_coordinates(file_name, l):
    
    f = open(file_name+'.txt', 'w')

    for i in range(len(l)):
        f.write(str(l[i][0])+".0 "+str(l[i][1])+" "+str(l[i][2])+"\n")

    f.close()
