import numpy as np
from scipy import integrate, optimize
import matplotlib.pyplot as plt

G1, G2, k1, k2, alpha1, alpha2, N0 = np.array([3.0, 2.0, 1.0, 1.0, 0.5, 0.5, 3.0])
def f(Y, t):
    y1, y2 = Y
    return [G1*(N0 - (alpha1*y1) - (alpha2*y2))*y1 - k1*y1, G2*(N0 - (alpha1*y1) - (alpha2*y2))*y2 - k2*y2]

m1, m2 = np.array([10, 10])
y1 = np.linspace(-m1, m1, 20)
y2 = np.linspace(-m2, m2, 20)

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
     

Q = plt.quiver(Y1, Y2, u, v, color='r')

plt.xlabel('$n_1$')
plt.ylabel('$n_2$')
plt.xlim([-m1, m1])
plt.ylim([-m2, m2])
plt.show()