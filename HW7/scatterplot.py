from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = pyplot.figure()
ax = pyplot.axes(projection='3d')

ax.scatter(1, -1, 1, c='b')
ax.scatter(1, 0, 1, c='b')
ax.scatter(0, 0, -1, c='b')
ax.scatter(0, -1, 1, c='b')
ax.scatter(1, 1, 1, c='r')
ax.scatter(0, 1, 0, c='r')
ax.scatter(0, 0, 1, c='r')
ax.scatter(-1, 0, 1, c='r')

x = np.linspace(-1, 1, 10)
y = np.linspace(-1, 1, 10)

X, Y = np.meshgrid(x, y)
# Equation of the plane would be: -2x + 2y + z = 0
Z = (0 + 2*X - 2*Y)

ax.plot_surface(X, Y, Z)

ax.set_xlabel('f1-axis')
ax.set_ylabel('f2-axis')
ax.set_zlabel('f3-axis')


pyplot.show()

