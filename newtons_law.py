import math
import pygame
import random

w, h = 1400, 800

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((w, h))




class object:
    def __init__(self, index, type, radius, x, y, fx, fy):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = (math.pi * (radius ** 2)) * density
        self.type = type
        self.index = index
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

        self.fx = fx * density
        self.fy = fy * density
        

    def resultant(self, objects):

        if self.type == 'static':
            return 0

        self.move()

        self.fx = 0
        self.fy = 0

        for object in objects:


            if self.index == object.index:
                continue
            self.on_collision = collision(self, object)
         
            try:
                force = -(constant * self.mass * object.mass) / (math.sqrt(((self.x - object.x) ** 2) + ((self.y - object.y) ** 2))) ** 2
            except:

                force = 0

            if self.on_collision:
                force = 0
            bearing = math.atan2((self.x - object.x), (self.y - object.y))
     
            self.fx += math.sin(bearing) * force
            self.fy += math.cos(bearing) * force



            
    def move(self):
        self.ax = self.fx / self.mass
        self.ay = self.fy / self.mass

        self.vx += self.ax
        self.vy += self.ay

        self.x += self.vx
        self.y += self.vy

def collision(obj1, obj2):


    if math.sqrt(((obj1.x - obj2.x)**2) + ((obj1.y - obj2.y)**2)) < obj1.radius + obj2.radius:
 

        return True
    else:
        return False

constant = 6.67430 * (10 ** -11)


density = 10000000000

objects = []

objects.append(object(-1, 'static', 50, 3 * w / 4,  h / 2, 0, 0))
objects.append(object(-2, 'static', 50, w / 4,  h / 2, 0, 0))
objects.append(object(0, 'dynamic', 10, w / 2,  3 * h / 4, 0, 0))

drawing = False
'''
for i in range(50):
    objects.append(object(i, 'dynamic', 1, random.randint(0, w), random.randint(0, h), 0, 0))
'''

while True:

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            startpos = pygame.mouse.get_pos()
            new_object = object(len(objects), 'dynamic', 15, startpos[0], startpos[1], 0, 0)
            drawing = True
        

        if event.type == pygame.MOUSEBUTTONUP:
            endpos = pygame.mouse.get_pos()
            new_object.fx = (startpos[0] - endpos[0]) * (new_object.mass / 50)
            new_object.fy = (startpos[1] - endpos[1]) * (new_object.mass / 50)

            objects.append(new_object)
            drawing = False
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

    for obj in objects:

        pygame.draw.circle(screen, (255, 255, 255), (obj.x, obj.y), obj.radius)
        if obj.index >= 0:
            pygame.draw.line(screen, (255, 255, 255), (obj.x, obj.y), ((obj.x + (obj.fx / density)), (obj.y + (obj.fy / density))))

            obj.resultant(objects)

    if drawing:
        location = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), (new_object.x, new_object.y), (location[0], location[1]))
        pygame.draw.circle(screen, (255, 255, 255), (new_object.x, new_object.y), new_object.radius)
   
    clock.tick(60)
    pygame.display.flip()
    screen.fill((0,0,0))