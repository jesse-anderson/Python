#Nonlinear_Equations[Newton_Raphson]
#If this method doesn't work use the secant method(TBD)
#Jesse Anderson 2021
#
#
from IPython import get_ipython
get_ipython().magic('reset -sf') 
#
from scipy.optimize import fsolve #https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fsolve.html
from numpy import sqrt #https://numpy.org/doc/stable/reference/generated/numpy.sqrt.html
from sympy import pprint, symbols
#

def Eqns(p):
    x,y,z,t,u,v = p
    #equations written as F(x)=0, basic set up
    eqn1 = ((x**2 + 2)/sqrt(y)) - 1.1 #((x^2 + 2)/SQRT(y))-1.1
    eqn2 = ((x*y)/2) - 15 #as shown
    eqn3 = (y - 4) + (z*(t**2)) #(y-4)+(z*(t^2))
    eqn4 = x+y + (z/t) #As shown
    eqn5 = ((x*y)-(z*t))*u #As shown
    eqn6 = v - 30 #program check
    #prints solution to eqn 1-6
    return eqn1, eqn2, eqn3, eqn4, eqn5, eqn6
    #
a,b,c,d,e,f = fsolve(Eqns,[1,1,1,1,1,1]) #solves the equations using fsolve()
##
##Pretty output, useless for computatio
##
x,y,z,t,u,v = symbols('x y z t u v')
print('\nEquation 1:\n')
pprint(((x**2 + 2)/(y**(1/2)) - 1.1))
print('\nEquation 2:\n')
pprint(((x*y)/2) - 15)
print('\nEquation 3:\n')
pprint((y - 4) + (z*(t**2)))
print('\nEquation 4:\n')
pprint(x+y + (z/t))
print('\nEquation 5:\n')
pprint(((x*y)-(z*t))*u)
print('\nEquation 6:\n')
pprint(v - 30)
##
##
print('\nSolution is: '
      '\nx =', a,
      '\ny=', b,
      '\nz=', c,
      '\nt= ', d,
      '\nu=',e,
      '\nv=', f) # this could be prettier but users can reorder as needed
