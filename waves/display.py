import matplotlib.pyplot as plt
import numpy as np
import math

num_points = 30000
num_seconds = 2

def calculate_points(frequency, amplitude):
    points_y = []

    for p in range(num_points):


        displacement = amplitude * math.sin((2*math.pi) * (p / num_points) / (1 / frequency) * num_seconds)
        points_y.append(displacement)
    
    return points_y

def superpose_points(points):

    


    sum_points = []
    for i in range(num_points):
        added_displacement = 0
        for set in points:
            added_displacement += set[i]

        sum_points.append(added_displacement)
    return sum_points




points1 = calculate_points(2, 2)



points_y = (points1)

points_x = []

for p in range(num_points):
    value = num_seconds * p / num_points
    points_x.append(value)






plt.plot(points_x, points_y)
plt.show()

