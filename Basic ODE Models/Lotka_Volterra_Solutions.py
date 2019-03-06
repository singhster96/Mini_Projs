# Solutions to the Dimensionless Lotka-Volterra Model

from numpy import *
from scipy import integrate, optimize
from matplotlib.pyplot import *

# Parameters
alpha = 1.2
y0 = 5. # Initial predator population
x0 = 10. # Initial prey population
tmax = 40. # Max time for run
ic = array([x0, y0]) 
t = linspace(0., tmax, 2000)

# We now define the vector field 
def f(X, t):
    return array([ X[0]*(1 - X[1]), alpha * X[1]* (X[0] - 1) ])
x = integrate.odeint(f, ic, t)


plot(t, x[:,0], 'g-', linewidth=2, label = 'Prey')
plot(t, x[:,1], 'r-', linewidth=2, label = 'Predator')
title('Dimensionless Lotka-Volterra Model ' + r'($\alpha = 1.2$)', 
       y = 1.04, fontsize = 'x-large')
xlabel(r'$\tau$', fontsize = 'x-large')
ylabel(r'$u, v$', fontsize = 'x-large')
xlim(0, tmax)
legend(loc = 'best')
savefig('Lotka-Volterra.png')
show()

