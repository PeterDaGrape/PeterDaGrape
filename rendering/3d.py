import PIL
import math
import matplotlib.pyplot as plt
import numpy as np

ax = plt.figure().add_subplot(projection='3d')


class Vertice:
    def __init__(self, vertice):

        self.x = vertice[0]
        self.y = vertice[1]
        self.z = vertice[2]



class Edge:
    def __init__(self, vertice_1, vertice_2):
        self.theta_edge = np.linspace(0, 1, 2)


        self.edge_x = vertice_1.x - (vertice_1.x - vertice_2.x) * self.theta_edge
        self.edge_y = vertice_1.y - (vertice_1.y - vertice_2.y) * self.theta_edge
        self.edge_z = vertice_1.z - (vertice_1.z - vertice_2.z) * self.theta_edge

        self.vertice_1 = vertice_1
        self.vertice_2 = vertice_2

        self.vector = self.vertice_1.x - self.vertice_2.x, self.vertice_1.y - self.vertice_2.y
        


        ax.plot(self.edge_x, self.edge_y, self.edge_z, label='edge')
    def point_x(self, t):
        return self.vertice_1.x - (self.vertice_1.x - self.vertice_2.x) * t
    def point_y(self, t):
        return self.vertice_1.y - (self.vertice_1.y - self.vertice_2.y) * t


class Face:
    def __init__(self, vertice_1, vertice_2, vertice_3):
        pass

        

class Object:
    def __init__(self, name, vertice_in, connections):
        self.vertices = []
        self.name = name
        for vertice in vertice_in:
            self.vertices.append(Vertice(vertice))
            plt.plot(*vertice, marker="o", markersize=5, color="red")


        self.edges = []

        for connection in connections:
            vertice_1 = self.vertices[connection[0]]
            vertice_2 = self.vertices[connection[1]]
            self.edges.append(Edge(vertice_1, vertice_2))

        self.faces = []


            


class Camera():
    def __init__(self, position, angle, pitch, field_of_view, resolution, max_dist):

        self.x = position[0]
        self.y = position[1]
        self.angle = math.radians(angle)
        self.pitch = math.radians(pitch)
        self.field_of_view = math.radians(field_of_view)
        self.resolution = resolution
        self.max_t = max_dist
    def scan(self, objects):
        increments = self.field_of_view / self.resolution


        array = []
        scan_horizontal = self.pitch + self.field_of_view / 2 + increments

        for horizontal_num in range(self.resolution + 1):
            scan_horizontal -= increments
            scan_angle = self.angle + self.field_of_view / 2 + increments

            parametric_z_coeff = math.sin(scan_horizontal)
            for scan_num in range(self.resolution + 1):

                scan_angle -= increments
                camera_theta = np.linspace(0, self.max_t, 2)

                parametric_x_coeff = math.sin(scan_angle)
                parametric_y_coeff = math.cos(scan_angle)

                cam_scan_line_x = parametric_x_coeff * camera_theta
                cam_scan_line_y = parametric_y_coeff * camera_theta 
                cam_scan_line_z = parametric_z_coeff * camera_theta

                colour = 'black'
                has_collided = False

                for object in objects:
                    distances = [math.inf]

                    intersection, coordinate, distance = self.find_intersection(object, parametric_x_coeff, parametric_y_coeff)

                    if intersection:
                        colour = 'red'
                        has_collided = True
                        distances.append(distance)


                distance = min(distances)
                if distance == math.inf:
                    distance = 0
                distance = round(distance)


                    
                ax.plot(cam_scan_line_x, cam_scan_line_y, cam_scan_line_z, label='Camera scan',color=colour)


        return array
    def find_intersection(self, object, x_coeff, y_coeff):
        
        t_values = []
        coordinates = []
        intersection = False
        distances = []
        for edge in object.edges:

            try:
                t_value = (x_coeff * edge.vertice_1.y - y_coeff * edge.vertice_1.x) / (x_coeff * (edge.vertice_1.y - edge.vertice_2.y) - y_coeff * (edge.vertice_1.x - edge.vertice_2.x))
            except:
                t_value = math.inf
            

            if t_value >= 0 and t_value <= 1:
                intersection = True

                coordinate = (edge.point_x(t_value), edge.point_y(t_value))

                coordinates.append(coordinate)

                distance = math.sqrt(coordinate[0] ** 2 + coordinate[1] ** 2)
                distances.append(distance)

        
                t_values.append(t_value)
            else:
                distances.append(math.inf)
                coordinates.append((math.inf, math.inf))

        distance = min(distances)

        closest_index = distances.index(distance)

        return intersection, coordinates[closest_index], distance
            
          



camera = Camera((0, 0), 0, 0, 110, 5, 8)
object = Object('square', ((2, 2, 2), (3, 2, 2), (3, 3, 2), (2, 3, 2), (2, 2, 3), (3, 2, 3), (3, 3, 3), (2, 3, 3)), ((0,4), (1,5),(2,6),(3,7), (0,1),(1,2),(2,3),(3,0), (4, 5),(5,6),(6,7), (7,4)))

objects = [object]

print(camera.scan(objects))

plt.show()
