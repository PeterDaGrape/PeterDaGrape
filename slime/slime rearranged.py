import random
import numpy as np
import math
from PIL import Image
import os

w = 2560
h = 1600
rad_factor = 1


colours = [(255, 255, 255)]

agent_speed = 1



class Agent:
    def __init__(self):
        
        spawn_radius = int(min(h) * rad_factor / 2)  # Adjust the radius as needed

        random_circle_x = -1
        random_circle_y = -1

        while math.sqrt(random_circle_x**2 + random_circle_y**2) > spawn_radius:
            random_circle_x = random.randint(-spawn_radius, spawn_radius)
            random_circle_y = random.randint(-spawn_radius, spawn_radius)
        self.x = w // 2 + random_circle_x
        self.y = h // 2 + random_circle_y

        self.agent_angle = math.atan2(self.y - h // 2, self.x - w // 2) - math.pi / 2
        self.agent_angle += (random.random()-0.5) * math.pi


        self.colour = colours[random.randint(0, len(colours)-1)]


        self.vel_x = agent_speed * math.sin(self.agent_angle)
        self.vel_y = agent_speed * math.cos(self.agent_angle)
    
    def update(self):
        self.collision()
        self.move()


    def move(self):

        self.vel_x = agent_speed * math.sin(self.agent_angle)
        self.vel_y = agent_speed * math.cos(self.agent_angle)

        self.x += self.vel_y
        self.y -= self.vel_y
    
    def collision(self):
        update = True

        
        if self.x > w:
            self.x = w - 1
            angle = random.randint(180, 360)
        elif self.x < 0:
            self.x = 1
            angle = random.randint(0, 180)
        elif self.y > h:
            self.y = h - 1
            angle = random.randint(270, 450)
        elif self.y < 0:
            self.y = 1
            angle = random.randint(90, 270)
        else:
            update = False

        if update:
            if angle >= 360:
                angle -= 360
            self.agent_angle = math.radians(angle)


agents = []
for i in range(1000):
    agents.append(Agent())

while True:
    for agent in agents:
        agent.update()
