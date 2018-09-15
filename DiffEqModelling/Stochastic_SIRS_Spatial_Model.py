import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

nn = 75 # Grid size
dt = 0.01 # time incrementation
beta0 = 2.75 # initial infection rate
tauI0 = 0.3 # initial infection period
tauR0 = 1.0 # initial (constant) resistance period
mu = 0.01 # infection rate / probability
dbeta = 0.01
dtauI = 0.01 # change in infection rate/period upon mutation
t = 0.0 # start time
T = 600. # end time; increase to observe convergence

state = np.zeros((nn, nn))# Initializie state with infectious cells
state[2, 2] = 1
state[73, 73] = 1

t_infect = np.zeros((nn, nn)) # How long the cell has been infected
t_resist = np.zeros((nn, nn)) # How long the cell has been resistant
beta_geno = np.zeros((nn, nn)) # Genotype of infection rate
tauI_geno = np.zeros((nn, nn)) # Genotype of infection period


# We first give all infected cells the same genotype
for rr in range(0, nn):
    for cc in range(0, nn):

        if state[rr, cc] == 1:
            beta_geno[rr, cc] = beta0
            tauI_geno[rr, cc] = tauI0


# The following function finds all the neighbors of a cell for a given matrix
# and given indices (x, y)
def nbrs(mat, x, y ):
    results = []
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            newx = x+dx
            newy = y+dy
            if (dx == 0 and dy == 0):
                continue
            if (newx >= 0 and newx < len(mat) and newy >= 0 and newy < len(mat)):
                results.append( mat[newx, newy] )
    return results


# Make a color map for the state transitions
# White -> Susceptible
# Red -> Infected
# Blue -> Resistant
cmap = colors.ListedColormap(['white', 'red', 'blue'])
bounds=[0, 1, 2, 3]
norm = colors.BoundaryNorm(bounds, cmap.N)
img = plt.imshow(state, interpolation='nearest', origin='upper',
                    cmap=cmap, norm=norm)            
plt.savefig('tmp_0001.png')
plt.close()


pic_counter = 1
fileName = 'tmp_' 


infection_rates = [beta0] # List of average infection rates
infection_times = [tauI0] # List of average infection periods

# Evolution
while t <= T:

    t += dt
    pic_counter += 1
    newstate = np.copy(state) # Temporary newstate matrix to allow update at each time step
    
    for rr in range(0, nn):
        for cc in range(0, nn):
            
            # 1) Check if cell is susceptible
            if state[rr, cc] == 0:
                i = nbrs(state, rr, cc).count(1) # If susceptible, observe nbrs

                if i >= 1: # If one or more nbrs is infected
                    beta = sum(nbrs(beta_geno, rr, cc)) # Add up infection rate of all nbrs
                    p_inf = 1 - np.exp(-i * beta * dt)  # Calculate "exponential" probability of infection
                    dec_inf = np.random.binomial(1, p_inf) # Determine if cell will be infected
                    
                    if dec_inf == 1: 
                    # If infected, determine genotype of newly infected cell by weighing the 
                    # infection rates and infection periods.
                        newstate[rr, cc] = 1
                        b = nbrs(beta_geno, rr, cc)
                        tau = nbrs(tauI_geno, rr, cc)
                        wts = b / sum(b)
                        
                        choice = np.random.choice(b, 1, p = wts)
                        beta_geno[rr, cc] = choice
                        tauI_geno[rr, cc] = tau[b.index(choice)]
            
            # 2) Check if cell is infected
            elif state[rr, cc] == 1:

                if t_infect[rr, cc] <= tauI_geno[rr, cc]: # If infection period is not over
                    t_infect[rr, cc] += dt # Update how long cell has been infected
                    mut_flip1 = np.random.binomial(1, mu) # Flip to determine if mutation occurs

                    if mut_flip1 == 1: 
                    # If mutation occurs, flip to determine direction of change
                        mut_flip2 = np.random.binomial(1, p = 0.50, size = (1, 2))

                        if (mut_flip2[:, 0] == 0) and (mut_flip2[:, 1] == 0):
                            # (rate goes down, period goes down)
                            beta_geno[rr, cc] -= dbeta
                            tauI_geno[rr, cc] -= dtauI

                        elif (mut_flip2[:, 0] == 0) and (mut_flip2[:, 1] == 1):
                            # (rate goes down, period goes up)
                            beta_geno[rr, cc] -= dbeta
                            tauI_geno[rr, cc] += dtauI

                        elif (mut_flip2[:, 0] == 1) and (mut_flip2[:, 1] == 0) :
                            # (rate goes up, period goes down)
                            beta_geno[rr, cc] += dbeta
                            tauI_geno[rr, cc] -= dtauI

                        elif (mut_flip2[:, 0] == 1) and (mut_flip2[:, 1] == 1):
                            # (rate goes up, period goes up)
                            beta_geno[rr, cc] += dbeta
                            tauI_geno[rr, cc] += dtauI
                            
                        infection_rates.append(np.true_divide(beta_geno.sum(), (beta_geno != 0).sum()))
                        infection_times.append(np.true_divide(tauI_geno.sum(), (tauI_geno != 0).sum()))
                    
                elif t_infect[rr, cc] > tauI_geno[rr, cc]: # If infection period is over
                    newstate[rr, cc] = 2 # Update state to resistant
                    t_infect[rr, cc] = 0 # Reset infected time
                    # Reset infection rate and infection period genotype
                    beta_geno[rr, cc] = 0
                    tauI_geno[rr, cc] = 0

            # 3) Check if cell is resistant
            elif state[rr, cc] == 2:

                if t_resist[rr, cc] <= tauR0: # If resistance period is not over
                    t_resist[rr, cc] += dt

                else: # If resistance period is over
                    newstate[rr, cc] = 0 # Make cell susceptible again
                    t_resist[rr, cc] = 0 

    state = np.copy(newstate) # State update
    
    
    # Save each transition plot; leave as comment when analyzing mutation behavior alone.
    #img = plt.imshow(state, interpolation='nearest', origin='upper', 
    #                      cmap=cmap, norm=norm)   
    #plt.savefig(fileName + '%04d.png' %pic_counter)

#plt.plot(infection_rates, infection_times)
#plt.xlabel('Infection Rate')
#plt.ylabel('Infection Period')
R = [8*a*b for a,b in zip(infection_rates, infection_times)]
plt.plot(R)
plt.show()