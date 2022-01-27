import numpy as np
import scipy.optimize as opt

################################################
### part 1: unconstrained LP
################################################

# quadratic obj
def quad_obj(x,Q,b):
  return x.T@Q@x + b.T@x # NOTE(1): YOU NEED TO COMPLETE HERE

# size of matrix A and b
n=4

# generate random positive definite matrix Q
A=np.random.normal(size=(n,n))
Q=np.identity(n)+A.T@A

b=np.random.normal(size=n)

# random initial point
x0=np.random.normal(size=n)

# for part 1, we will use h1_qp function for solving QP
def h1_qp(f0,Q,b,x0):
  return opt.minimize(fun=f0,args=(Q,b),x0=x0)

res= h1_qp(f0=quad_obj,Q=Q,b=b,x0=x0)
print('optimization results from minimize function: ', res)

################################################
### part 2: constrained LP
################################################

# inequality constraints Ax<=b
A= np.array([[1/6,1/15], [1/7,1/8] ,[1/18,1/5]]) # NOTE(2): YOU NEED TO COMPLETE HERE
b= np.array([1,1,1]) # NOTE(3): YOU NEED TO COMPLETE HERE
# objective vector
c=np.random.randint(1,50,size=2) # NOTE(4): YOU NEED TO COMPLETE HERE

print(c)
# NOTE(5): DEFINE ANY FUNCTIONS OR VARIABLES IF YOU NEED
def lp_obj(x, c):
  return -c.T@x

# initial point
x0=np.random.normal(size=len(c))

# for part 2, we will use h1_lp function for solving LP
def h1_lp(f0,c,x0,A,b):
  # f0 is objective function
  # c is objective vector, that is, we miminize c^Tx
  # x0 is initial point
  # A: constraint matrix Ax<=b
  # b: constraint vector Ax<=b
  con=opt.LinearConstraint(A,0,b)
  bnd=opt.Bounds(0,np.inf)
  return opt.minimize(fun=f0,args=(c), x0=x0, constraints=con, bounds=bnd) # NOTE(6): YOU NEED TO COMPLETE HERE (YOU MAY ALSO USE opt.linprog INSTEAD OF opt.minimize)

# test your h1_lp function
reslp = h1_lp(f0=lp_obj , c=c, x0=x0, A=A, b=b) # NOTE(7): YOU NEED TO COMPLETE HERE

print('optimization results: ', reslp)