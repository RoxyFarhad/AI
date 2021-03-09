import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(1, -1, -1, color='blue');
ax.scatter3D(1, 0, 1, color='blue');
ax.scatter3D(0, 0, -1, color='blue');
ax.scatter3D(0, -1, 1, color='blue');
ax.scatter3D(1, 1, 1, color='red');
ax.scatter3D(0, 1, 0, color='red');
ax.scatter3D(0, 0, 1, color='red');
ax.scatter3D(-1, 0, 1, color='red');

a,b,c,d = 1,1,1,0
x = np.linspace(-1,1,10)
y = np.linspace(-1,1,10)

X,Y = np.meshgrid(x,y)
Z = (d - a*X - b*Y) / c

# fig = plt.figure()
# ax = fig.gca(projection='3d')

surf = ax.plot_surface(X, Y, Z)
fig.set_size_inches(15,15)
plt.show()