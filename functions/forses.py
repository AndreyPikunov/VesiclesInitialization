from math import sqrt

from python_packages.functions.geometry import * 


######_SPRING_FORSES_################

def flx(var, i, l0 = 0.66, kl = 0.3):
    l_after = length(var.x(i), var.y(i), var.x(i+1), var.y(i+1))
    l_before = length(var.x(i), var.y(i), var.x(i-1), var.y(i-1))
    f_after = -kl*(l_after - l0)/(l_after * l0**2) * (var.x(i) - var.x(i+1))
    f_before = -kl*(l_before - l0)/(l_before * l0**2) * (var.x(i) - var.x(i-1))
    return f_after + f_before

def fly(var, i, l0 = 0.66, kl = 0.3):
    l_after = length(var.x(i), var.y(i), var.x(i+1), var.y(i+1))
    l_before = length(var.x(i), var.y(i), var.x(i-1), var.y(i-1))
    f_after = -kl*(l_after - l0)/(l_after * l0**2) * (var.y(i) - var.y(i+1))
    f_before = -kl*(l_before - l0)/(l_before * l0**2) * (var.y(i) - var.y(i-1))
    return f_after + f_before

####_AREA_FORSES#####################

def fsx(var, i, ks = 200.0, s0 = 314.0):
    s = area(var.x(), var.y()) 
    return -0.5*ks*(s - s0)/(s0**2) * (var.y(i-1) - var.y(i+1))

def fsy(var, i, ks = 200.0, s0 = 314.0):
    s = np.abs( area(var.x(), var.y()) )
    return -0.5*ks*(s - s0)/(s0**2) * (var.x(i+1) - var.x(i-1))

####_ANGULAR_FORSES################## kb = 0.05 for Ca = 10, u_max = 0.0025

def fbx(var, i, kb = 0.05, theta0 = 0.0):
    
        dx1 = var.x(i+1) - var.x(i)       # x1 - x
        dx2 = var.x(i) - var.x(i-1);      # x - x2
        dx3 = var.x(i+2) - var.x(i+1);    # x3 - x1
        dx4 = var.x(i-1) - var.x(i-2);    # x2 - x4
        dy1 = var.y(i+1) - var.y(i)       # y1 - y
        dy2 = var.y(i) - var.y(i-1);      # y - y2
        dy3 = var.y(i+2) - var.y(i+1);    # y3 - y1
        dy4 = var.y(i-1) - var.y(i-2);    # y2 - y4

        # length
        l1 = sqrt(dx1*dx1 + dy1*dy1);
        l2 = sqrt(dx2*dx2 + dy2*dy2);
        l1_inv = 1.0 / l1;
        l2_inv = 1.0 / l2;
        l3_inv = 1.0 / sqrt(dx3*dx3 + dy3*dy3);
        l4_inv = 1.0 / sqrt(dx4*dx4 + dy4*dy4);

        temp = 0.0

        # trigonometrics
        costheta1 = (dx1*dx2 + dy1*dy2) * l1_inv * l2_inv;
        costheta2 = (dx3*dx1 + dy3*dy1) * l1_inv * l3_inv;
        costheta3 = (dx2*dx4 + dy2*dy4) * l2_inv * l4_inv;

        # trigonometrics derivatives
        temp = 1.0 + costheta1;
        kkb1 = kb / (temp*temp);
        temp = 1.0 + costheta2;
        kkb2 = kb / (temp*temp);
        temp = 1.0 + costheta3;
        kkb3 = kb / (temp*temp);
        l13_inv = l1_inv*l1_inv*l1_inv;
        l23_inv = l2_inv*l2_inv*l2_inv;
        dcos1dx = \
            (dx1 - dx2) * l1_inv * l2_inv + (dx1*dx2 + dy1*dy2)*dx1 * l13_inv * l2_inv - \
            (dx1*dx2 + dy1*dy2)*dx2 * l1_inv * l23_inv;
        dcos2dx = -dx3 * l3_inv * l1_inv + (dx3*dx1 + dy3*dy1)*dx1 * l3_inv * l13_inv;
        dcos3dx = dx4 * l2_inv * l4_inv - (dx2*dx4 + dy2*dy4)*dx2 * l23_inv * l4_inv;
        dcos1dy = \
            (dy1 - dy2) * l1_inv * l2_inv + (dx1*dx2 + dy1*dy2)*dy1 * l13_inv * l2_inv - \
            (dx1*dx2 + dy1*dy2)*dy2 * l1_inv * l23_inv;
        dcos2dy = -dy3 * l3_inv * l1_inv + (dx3*dx1 + dy3*dy1)*dy1 * l3_inv * l13_inv;
        dcos3dy = dy4 * l2_inv * l4_inv - (dx2*dx4 + dy2*dy4)*dy2 * l23_inv * l4_inv;
        
                #bending force
        return kkb1*dcos1dx + kkb2*dcos2dx + kkb3*dcos3dx;
        

def fby(var, i, kb = 0.05, theta0 = 0.0):
    
    dx1 = var.x(i+1) - var.x(i)       # x1 - x
    dx2 = var.x(i) - var.x(i-1);      # x - x2
    dx3 = var.x(i+2) - var.x(i+1);    # x3 - x1
    dx4 = var.x(i-1) - var.x(i-2);    # x2 - x4
    dy1 = var.y(i+1) - var.y(i)       # y1 - y
    dy2 = var.y(i) - var.y(i-1);      # y - y2
    dy3 = var.y(i+2) - var.y(i+1);    # y3 - y1
    dy4 = var.y(i-1) - var.y(i-2);    # y2 - y4

    # length
    l1 = sqrt(dx1*dx1 + dy1*dy1);
    l2 = sqrt(dx2*dx2 + dy2*dy2);
    l1_inv = 1.0 / l1;
    l2_inv = 1.0 / l2;
    l3_inv = 1.0 / sqrt(dx3*dx3 + dy3*dy3);
    l4_inv = 1.0 / sqrt(dx4*dx4 + dy4*dy4);

    temp = 0.0

    # trigonometrics
    costheta1 = (dx1*dx2 + dy1*dy2) * l1_inv * l2_inv;
    costheta2 = (dx3*dx1 + dy3*dy1) * l1_inv * l3_inv;
    costheta3 = (dx2*dx4 + dy2*dy4) * l2_inv * l4_inv;

    # trigonometrics derivatives
    temp = 1.0 + costheta1;
    kkb1 = kb / (temp*temp);
    temp = 1.0 + costheta2;
    kkb2 = kb / (temp*temp);
    temp = 1.0 + costheta3;
    kkb3 = kb / (temp*temp);
    l13_inv = l1_inv*l1_inv*l1_inv;
    l23_inv = l2_inv*l2_inv*l2_inv;
    dcos1dx = \
        (dx1 - dx2) * l1_inv * l2_inv + (dx1*dx2 + dy1*dy2)*dx1 * l13_inv * l2_inv - \
        (dx1*dx2 + dy1*dy2)*dx2 * l1_inv * l23_inv;
    dcos2dx = -dx3 * l3_inv * l1_inv + (dx3*dx1 + dy3*dy1)*dx1 * l3_inv * l13_inv;
    dcos3dx = dx4 * l2_inv * l4_inv - (dx2*dx4 + dy2*dy4)*dx2 * l23_inv * l4_inv;
    dcos1dy = \
        (dy1 - dy2) * l1_inv * l2_inv + (dx1*dx2 + dy1*dy2)*dy1 * l13_inv * l2_inv - \
        (dx1*dx2 + dy1*dy2)*dy2 * l1_inv * l23_inv;
    dcos2dy = -dy3 * l3_inv * l1_inv + (dx3*dx1 + dy3*dy1)*dy1 * l3_inv * l13_inv;
    dcos3dy = dy4 * l2_inv * l4_inv - (dx2*dx4 + dy2*dy4)*dy2 * l23_inv * l4_inv;    
    
    return kkb1*dcos1dy + kkb2*dcos2dy + kkb3*dcos3dy;

def flx_2(var, i, l0 = 1.32, kl = 0.3):
    l_after = length(var.x(i), var.y(i), var.x(i+2), var.y(i+2))
    l_before = length(var.x(i), var.y(i), var.x(i-2), var.y(i-2))
    f_after = -kl*(l_after - l0)/(l_after * l0**2) * (var.x(i) - var.x(i+2))
    f_before = -kl*(l_before - l0)/(l_before * l0**2) * (var.x(i) - var.x(i-2))
    return f_after + f_before

def fly_2(var, i, l0 = 1.32, kl = 0.3):
    l_after = length(var.x(i), var.y(i), var.x(i+2), var.y(i+2))
    l_before = length(var.x(i), var.y(i), var.x(i-2), var.y(i-2))
    f_after = -kl*(l_after - l0)/(l_after * l0**2) * (var.y(i) - var.y(i+2))
    f_before = -kl*(l_before - l0)/(l_before * l0**2) * (var.y(i) - var.y(i-2))
    return f_after + f_before
