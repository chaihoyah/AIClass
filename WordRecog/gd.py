import numpy as np
import time
def min_gd(fun,x0,grad,args=()):
    is_finished= False
    a = 0.3
    b = 0.8
    e = 0.00001
    while not is_finished:
        t = 1
        while(True):
            dx = grad(x0,*args)
            if fun(x0-t*dx,*args) > fun(x0,*args)-a*t*np.dot(dx.T,dx):
                t=t*b
            else:
                break
        x0 = x0-t*dx
        if np.linalg.norm(grad(x0,*args)) <= e:
            is_finished= True
    return x0
