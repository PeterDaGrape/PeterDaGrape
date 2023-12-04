import matplotlib.pyplot as plt
import numpy as np

ax = plt.figure().add_subplot(projection='3d')

# Define the parametric functions
def x(t):
    return 2*t +3

def y(t):
    return 3*t + 1

def z(t):
    return 5 + t

# Create an array of t values
t = np.linspace(-2, 2, 100)

# Plot the parametric curve
ax.plot(x(t), y(t), z(t), label='parametric curve')

# Plot the plane
u, v = np.meshgrid(t, t)
ax.plot_surface(x(u), y(v), z(u), alpha=0.5, color='green', label='parametric plane')

# Add labels and legend
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Show the plot
plt.show()