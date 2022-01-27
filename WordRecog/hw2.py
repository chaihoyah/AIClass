import numpy as np
from scipy.optimize import minimize
import gd

# Least Squares function
def LeastSquares(x,A,b):
    return np.linalg.norm(np.dot(A,x)+b)**2


# gradient of Least Squares function
def grad_LeastSquares(x,A,b):
    return 2*np.dot(np.dot(A,x)+b,A)

# size of matrix A (m by n) and b (m by 1)
m=100
n=10

# create matrices for least squares function
A=np.random.normal(size=(m,n))
b=np.random.normal(size=m)

# initial point
x0=np.random.normal(size=n)

# built-in minimize function
res=minimize(fun=LeastSquares,x0=x0,args=(A,b))
print('solution from minimize: message: ', res.message)
print('solution from minimize: success:', res.success)
print('solution from minimize: solution x:', res.x)

# your implementation of gradient descent
x=gd.min_gd(fun=LeastSquares,x0=x0,grad=grad_LeastSquares,args=(A,b))
print('solution from min_gd:', x)

# show error between built-in and your solutions
print('error :',np.linalg.norm(x-res.x))
