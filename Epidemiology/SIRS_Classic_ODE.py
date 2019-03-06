from scipy.integrate import odeint
from numpy import arange
import matplotlib.pyplot as plt

def SIRS(state,t):
    
  # Initialization of States
  S = state[0]
  I = state[1]
  R = state[2]

  # Appropriate Constants
  beta = 0.25 # Rate of infection; needs to be divided by N in the system of ODEs
  gamma = 0.2 # Proportion leaving infected to become resistant
  rho = 0.1 # Proportion leaving resistant to become susceptible.
  N = S + I + R
  # compute state derivatives
  dS = (rho*R) - ((beta/N)*S*I)
  dI = ((beta/N)*S*I) - (gamma*I)
  dR = (gamma*I) - (rho*R)

  # return the state derivatives
  return [dS, dI, dR]

state0 = [33, 33, 33]
t = arange(0.0, 100, 0.01)

state = odeint(SIRS, state0, t)

# Plots

susceptible = state[:, 0]
infected = state[:, 1]
resistant = state[:, 2]

fig = plt.figure(figsize=(15,5))
fig.subplots_adjust(wspace = 0.5, hspace = 0.3)
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

ax1.plot(susceptible, 'b-', label = "Susceptible")
ax1.plot(infected, 'r-', label = "Infected")
ax1.plot(resistant, 'g-', label = "Resistant")
ax1.set_title("Sample Dynamics of SIRS Model in Time")
ax1.set_xlabel("Time")
ax1.grid()
ax1.legend(loc = 'best', fontsize = 'small')



ax2.plot(susceptible, infected, color = "purple", label = 'S-I Phase')
ax2.plot(susceptible, resistant, color = "cyan", label = 'S-R Phase')
ax2.plot(infected, resistant, color = "yellow", label = 'I-R Phase')
ax2.set_title("SIRS Sample Phase Space")
ax2.legend(loc = 'best', fontsize = 'small')
ax2.grid()

extent = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
fig.savefig('timedynamics5.png', bbox_inches=extent.expanded(1.3, 1.3))
extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
fig.savefig('phase5.png', bbox_inches=extent.expanded(1.2, 1.2))

plt.show()