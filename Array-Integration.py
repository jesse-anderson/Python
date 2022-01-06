#Array Integration
#Jesse Anderson 2021
#use when you have x,y data and nothing else
#also called numerical quadratures
#calculation below assume linearity and splines for smoothness
#revisit this since its confusing and if I have to implement anywhere its gonna be a pain
#
#Please note movegui being used to move figures to proper position via tkinter, omit movegui if errors occur
from IPython import get_ipython
get_ipython().magic('reset -sf') 
#
from scipy.integrate import quad #https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html
from scipy.interpolate import interp1d #https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html
from numpy import array #https://numpy.org/doc/stable/reference/generated/numpy.array.html
from numpy import arange #https://numpy.org/doc/stable/reference/generated/numpy.arange.html
from movegui import movegui
#
import matplotlib.pyplot as plt 
plt.close('all')
#
#Temp of vapor, Degrees C
x1 = array([100,130,170,190,230,270,320,370]) #data
#
#Density of saturated steam,volume gas, m^3/kg
#https://www.ohio.edu/mechanical/thermo/property_tables/H2O/H2O_TempSat1.html
#https://www.ohio.edu/mechanical/thermo/property_tables/H2O/H2O_TempSat2.html
y1 = array([1.6718, 0.66800, 0.24259, 0.15636, 0.07150, 0.03562, 0.01547, 0.00495]) #data
#
#linear interpolation for graph
f = interp1d(x1,y1, kind ='linear') #interpolates x/y data w/ type being linear interpolation
xnew = arange(100,375,30) #returns evenly spaced values between 100 and 375 w/ 30 steps
ynew = f(xnew) # f(x)
#
#cubic interpolation for graph
f = interp1d(x1,y1, kind ='cubic') #interpolates x/y data w/ type being cubic interpolation
xnew2 = arange(100,375,30)
ynew2 = f(xnew)
#
#integral boxes for second plot
f = interp1d(x1,y1, kind ='nearest') #rough integral estimation see https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html 
xnew3 = arange(100,375, 30)
ynew3 = f(xnew3)
#
#1- mean density assuming LINEARITY
#takes integral of the values between 100 and 200 assuming linearity
Int_linearity = quad(lambda x: interp1d(x1,y1,'linear')(x),100,200)
#
#prints integral value and error
print('Linear integral is ',Int_linearity[0],' with error ',Int_linearity[1])
#
#gives mean if its assumed to be linear
Mean_lin = Int_linearity[0] / (200-100)
#
#2 - mean density assuming SMOOTHNESS
Int_splines = quad(lambda x: interp1d(x1, y1, 'cubic')(x), 100, 200)
#
#Prints integral assuming its smooth
print('Spline integral is ', Int_splines[0], ' with error ', Int_splines[1])
#
#calculates mean if its assumed to be linear
Mean_splines = Int_splines[0] / (200-100)
#
#Prints Mean linear and splines value
print('Mean_Linear value =',Mean_lin, 'kg/m^3')
print('Mean_splines value =',Mean_splines, 'kg/m^3')
#
#Plots data for the sake of visualization
plt.figure() #initialize figure window
plt.plot(x1,y1, 'o', xnew, ynew, '-', xnew2, ynew2, '--') #plot 3 different sets of points for interpolation
plt.title("Temp of vapor vs Density") #graph title
plt.xlabel("Temp of vapor, Degrees C")#x label
plt.ylabel("Density of saturated steam kg/m^3")#y label
plt.legend(['data', 'linear', 'cubic'], loc ='best') #legend put in best open space
plt.show()
movegui("northwest")
#
plt.figure() #create another figure window
movegui("northeast")
plt.plot(x1,y1,'o', xnew3, ynew3, ':') #plot fit for integral using central point
plt.title("Temp of vapor vs Density") #graph title
plt.xlabel("Temp of vapor, Degrees C") #x label
plt.ylabel("Density of saturated steam kg/m^3") #y label
plt.legend(['data', 'nearest integration'], loc ='best') # x legend
plt.show() #finally shows graphs, important that this statement is at the end

