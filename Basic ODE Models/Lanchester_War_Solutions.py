# Lanchester War Model Solutions
# The following program plots the size of two armies following the Lanchester Model of warfare.
# It takes input parameters g, r, and y0, which are the "force multipliers" of the two armies,
# and the initial size of the second army. Then it calculates the minimum size needed for the 
# first army to win. Further, it displays the time at which the second army will die out if the
# initial condition for the first army is met.

from numpy import *
from scipy import integrate
from matplotlib.pyplot import *

g = 0.45
r = 0.46
y0 = 100.
x0 = np.ceil(np.sqrt(g/r)* y0)

ic = array([x0, y0])
c1 = (0.5)*(ic[0] - (g*ic[1] / np.sqrt(g*r)))
c2 = (0.5)*(ic[0] + (g*ic[1] / np.sqrt(g*r)))
t_int = log(c2/c1)/(2*sqrt(g*r))
t = linspace(0, t_int*1.3, 365)

def f(X, t):
    return array([ -g*X[1], -r*X[0] ])

x = integrate.odeint(f, ic, t)


plot(t, x[:,0], 'b-', linewidth=2, label = 'Army A')
plot(t, x[:,1], 'r-', linewidth=2, label = 'Army B')
xlabel('Time', fontsize = 'large')
ylabel('Army Size', fontsize = 'large')
ylim(0,max(ic[0], ic[1]))
xlim(0, t_int*1.3)
title('Lanchester War Model')
legend(loc = 'best')
savefig('War.png')
show()

print("Army B dies out at time: ", t_int)
