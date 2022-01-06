#Symbolic Integration
#Jesse Anderson 2021
#Note ** is to the power of, while * is simply multiplication!
#Don't forget your plus C either idiot
#https://scipy-lectures.org/packages/sympy.html
#https://docs.sympy.org/latest/tutorial/calculus.html 
#
#
from IPython import get_ipython
get_ipython().magic('reset -sf') 
#
from sympy import Symbol #https://www.tutorialspoint.com/sympy/sympy_symbols.htm
from sympy import integrate #https://docs.sympy.org/latest/modules/integrals/integrals.html 
from sympy import *
from sympy import pprint, symbols, init_session, init_printing, Integral
#
#Pure symbolic indefinite integration +C territory
x =Symbol('x') #x as symbol
symbolicIntegral = integrate(4*x**5) #integration is performed 6*x^2
#
pprint(Integral(4*x**5))
print('Result is ',symbolicIntegral,'+ CONSTANT') #prints symbolic integral
#
#Symbolic Defined Integrals
#Jesse Anderson 2021
# from numpy import pi #https://numpy.org/doc/stable/reference/constants.html 
from numpy import inf #https://numpy.org/doc/stable/reference/constants.html
from sympy import pprint, symbols, init_session, init_printing, Integral
x=Symbol('x') #x as symbol
b=Symbol('b') #b as symbol
a=Symbol('a') #a a symbol
#

#integrate cos(x)+sin(x) btwn a(bottom) and b(top)
#plus sinx/x*0.5, 0 bottom, infinity top
symbolicDefiniteIntegral = integrate(cos(x)+sin(x),(x,a,b)) + integrate(sin(x)/(x*3),(x,0,inf))
#
pprint(Integral(cos(x)+sin(x),(x,a,b)) + Integral(sin(x)/(x*3),(x,0,inf)))
#
print('Result is ', symbolicDefiniteIntegral,'+ CONSTANT')
