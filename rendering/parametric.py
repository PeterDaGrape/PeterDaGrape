import matplotlib.pyplot as plt
import numpy as np




points = [(3,6), (7,8)]




#ax = plt.figure().add_subplot(projection='3d')
ax = plt.figure().add_subplot()
t = np.linspace(0, 1, 100)


x = points[0][0] - (points[0][0] - points[1][0]) * t
y = points[0][1] - (points[0][1] - points[1][1]) * t


ax.plot(x, y, label='parametric curve')

for point in points:
    plt.plot(*point, marker="o", markersize=5, color="red")

tcam = np.linspace(0, 10, 100)

xcam = 0.6 * tcam
ycam = 0.9 * tcam
ax.plot(xcam, ycam, label='Camera scan')


ax.legend()




plt.show()