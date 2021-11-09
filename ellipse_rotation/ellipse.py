import numpy as np
import math
import matplotlib.pyplot as plt


def Srotate(angle,valuex,valuey,pointx,pointy):
    valuex = np.array(valuex)
    valuey = np.array(valuey)
    sRotatex = (valuex-pointx)*math.cos(angle) + (valuey-pointy)*math.sin(angle) + pointx
    sRotatey = (valuey-pointy)*math.cos(angle) - (valuex-pointx)*math.sin(angle) + pointy
    return sRotatex,sRotatey


def ellipserotate(angle,b_H,b_W,x_c,y_c,pointx,pointy):
    y_1 = []
    x_1 = np.arange(x_c-b_W/2,x_c+b_W/2,0.1)
    for x in x_1:
        y = math.sqrt(math.fabs((1-(x-x_c)**2/(b_W**2/4))*(b_H**2)/4))+y_c
        y_1.append(y)
    for x in x_1:
        y = -math.sqrt(math.fabs((1-(x-x_c)**2/(b_W**2/4))*(b_H**2)/4))+y_c
        y_1.append(y)
    x_1 = np.append(x_1,x_1)
    y_1 = np.array(y_1)
    x_2,y_2 = Srotate(math.radians(angle),x_1,y_1,pointx,pointy)
    x_min = np.min(x_2)
    y_min = np.min(y_2)
    x_max = np.max(x_2)
    y_max = np.max(y_2)
    return x_min,y_min,x_max,y_max
'''
if __name__ == '__main__':

    angle = 25
    b_W = 200
    b_H = 100
    x_c = 0
    y_c = 0
    pointx,pointy = 540,1920
    x_min,y_min,x_max,y_max,x_2,y_2 = ellipserotate(angle,b_H,b_W,x_c,y_c,pointx,pointy)
    plt.scatter(x_2,y_2)
    plt.scatter(x_min,y_min,marker = 'o' ,c='y')
    plt.show()
'''