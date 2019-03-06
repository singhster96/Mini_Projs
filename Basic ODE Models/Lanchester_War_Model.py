import numpy as np
import matplotlib.pyplot as plt

g = 0.50
r = 0.45

def f(Y, t):
    y1, y2 = Y
    return [-g*y2, -r*y1]

m1, m2 = np.array([15, 12])
y1 = np.linspace(0.0, m1, 20)
y2 = np.linspace(0.0, m2, 20)

Y1, Y2 = np.meshgrid(y1, y2)

t = 0

u, v = np.zeros(Y1.shape), np.zeros(Y2.shape)

NI, NJ = Y1.shape

for i in range(NI):
    for j in range(NJ):
        x = Y1[i, j]
        y = Y2[i, j]
        yprime = f([x, y], t)
        u[i,j] = yprime[0]
        v[i,j] = yprime[1]
     

Q = plt.quiver(Y1, Y2, u, v, color='r', width = 0.001)

plt.xlabel('$A$')
plt.ylabel('$B$')
plt.xlim([0, max(m1, m2)-1])
plt.ylim([0, max(m1, m2)-1])
plt.plot(y1, ((g/np.sqrt(r*g))*y1), color = 'b')
plt.show()