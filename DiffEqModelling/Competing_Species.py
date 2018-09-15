from scipy import array, linspace
from scipy import integrate
from matplotlib.pyplot import *

def vector_field(X, t, r1, K1, c1, r2, K2, c2):
    # Competing Species differential equations model
    # from Section 9.4 of Boyce & DiPrima
    # The differential equations are
    #
    #    dR
    #    -- = r1*R*(1-R/K1) - c1*R*S
    #    dt
    #
    #    dS
    #    -- = r2*S*(1-S/K2) - c2*R*S
    #    dt
    R = X[0] # Rabbits density
    S = X[1] # Sheep density
    return array([r1*R*(1-R/K1) - c1*R*S,  r2*S*(1-S/K2) - c2*R*S])

# set up our initial conditions
R0 = 10.
S0 = 20.
X0 = array([R0, S0])

# Parameters
r1 = .3    # rabbit growth rate
r2 = .2    # sheep growth rate
c1 = .2    # inhibition of rabbits due to competition
c2 = .1    # inhibition of sheep due to competition
K1 = 30. # carrying capacity of rabbits
K2 = 20. # carring capacity of sheep

# choose the time's we'd like to know the approximate solution
t = linspace(0., 60., 100)

# and solve
X = integrate.odeint(vector_field, X0, t, args=(r1,K1,c1,r2,K2,c2))

# now, plot the solution curves
figure(1)
plot(t, X[:,0], 'bx-', linewidth=2)
plot(t, X[:,1], 'g+-', linewidth=2)
axis([0,60,0,31])
xlabel('Time (days)')
ylabel('Number')

legend(['Rabbits', 'Sheep'],loc=2)

savefig('CompetingSpecies2.png')
show()