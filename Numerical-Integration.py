#For integrals in general refer to: https://docs.scipy.org/doc/scipy/reference/integrate.html 
#
##Numerical Integration
#Jesse Anderson 2021
#
from IPython import get_ipython
get_ipython().magic('reset -sf') 
#
from scipy.integrate import quad #https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html
from numpy import exp #https://numpy.org/doc/stable/reference/generated/numpy.exp.html
from sympy import pprint, symbols, init_session, init_printing, Integral
def Function1(x): #define the function you are integrating
    y= x**2
    return y
#evaluates above integral from number to number, 0->3
Quad_routine = quad(Function1,0,3) #function, lower bound, upper bound
#prints integral and estimated error.
print('\nIntegral of x^2 from 0 to 3')
#
init_session(quiet=True)
init_printing()
x= symbols('x')
pprint(Integral(x**2,(x,0,3)))
#
print('Result is ',Quad_routine[0], 'with error ', Quad_routine[1],'\n') #confirmed correct
#
##Improper integrals
#
#Redoing the imports here because this is meant to be sectional code but I'm lumping it together to make my future easier
from scipy.integrate import quad #https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html
from numpy import inf #https://numpy.org/devdocs/reference/constants.html
from sympy import pprint, symbols, init_session, init_printing, Integral
#
def Function2(x):
    y=1/(x**3+6)
    return y
#evaluates integral from 0 to infinity
integral2 = quad(Function2,0,inf) #function, lower bound, upper bound
#prints integral and estimated error.
print('Integral of 1/((x^3+6 from 0 to infinity')
#
init_session(quiet=True)
init_printing()
x = symbols('x')
pprint(Integral(1/((x**3+6)),(x,0,inf)))
#
print('Result is ',integral2[0], 'with error ', integral2[1],'\n') #confirmed correct
#
#Double Numerical Integrals **don't mess up order of integration!!!!
#
from scipy.integrate import dblquad #https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.dblquad.html#scipy.integrate.dblquad
from sympy import pprint, symbols, init_session, init_printing, Integral
#x,y is the order of integration
Function3 = lambda x,y: x**2 + y**2 #defined function as x^2 + y^2 dydx
#outer and inner limits, inner is integrated first(0->1), then outer(0->2)
integrateDouble = dblquad(Function3, 0, 1, lambda x: 0, lambda x: 2) #INT 0->2 INT 0-> 1 (x^2 + y^2) dydx
#prints integral and estimated error.
print('Double integral of x^2 dydx with bounds outer from 0 to 1 and inner from 0 to 2 ')
#
init_session(quiet=True)
init_printing()
x,y = symbols('x y')
pprint(Integral(Integral(x*y**2,(y,0,2)),(x,0,1)))
#
print('Result is ', integrateDouble[0], 'with error ', integrateDouble[1],'\n') #confirmed correct
#
#######Stupid limits(variables)
#
from scipy.integrate import dblquad#https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.dblquad.html#scipy.integrate.dblquad
from sympy import pprint, symbols, init_session, init_printing, Integral
#integrate x^2*y dxdy limits x=y to (y^2)+1 inner and 0 to 1 outer
#integration order is outer then inner
integrate_variable = dblquad(lambda x,y : x**2 + y**2,0,1, lambda y: y, lambda y: y*y+6)
#prints integral and estimated error.
print('Double integral of x^2 + y^2 dydx with bounds outer from 0 to 1 and inner from y to (y^2)+6 ') 
#
init_session(quiet=True)
init_printing()
x,y = symbols('x y')
pprint(Integral(Integral(x**2+y**2,(y,y,y**2+6)),(x,0,1)))
#
print('Result is ', integrate_variable[0], 'with error', integrate_variable[1],'\n') #confirmed correct
#
##Reverse Order dydx
#
from scipy.integrate import dblquad #https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.dblquad.html#scipy.integrate.dblquad
from sympy import pprint, symbols, init_session, init_printing, Integral
#note y,x are i same order as dy and dx
#limts order is outer then inner
integrate_reverse = dblquad(lambda y,x : x**2 + y**2,0,1,lambda x:0, lambda x: exp(x**2))
print('Double integral of x^2+y^2 dydx with bounds outer from 0 to 1 and inner from 0 to e^x^2')
#
init_session(quiet=True)
init_printing()
x,y,e = symbols('x y e')
pprint(Integral(Integral(x**2+y**2,(y,0,e**x**2)),(x,0,1)))
#
print('Result is ',integrate_reverse[0], 'with error', integrate_reverse[1],'\n') #confirmed correct
#
