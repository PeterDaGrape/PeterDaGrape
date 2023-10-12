import math
import pygame
import random
w, h = 800, 800

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((w, h))

class object:
    def __init__(self, index, radius, x, y, fx, fy):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = (math.pi * (radius ** 2)) * density

        self.index = index

        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = 0

        self.fx = fx * density
        self.fy = fy * density
        

    def resultant(self, objects):
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
        '''
        if self.x > w:
            self.x = 0
        if self.y > h:
            self.y = 0
        if self.x < 0:
            self.x = w
        if self.y < 0:
            self.y = h
        '''

        


def collision(obj1, obj2):


    if math.sqrt(((obj1.x - obj2.x)**2) + ((obj1.y - obj2.y)**2)) < obj1.radius + obj2.radius:
 

        return True
    else:
        return False



        


constant = 6.67430 * (10 ** -11)


density = 10000000000

objects = []


obj1 = object(0, 40, w / 4, h / 2, 0, -10000)
obj2 = object(1, 40, 3*w / 4, h / 2, 0, 10000)
obj3 = object(3, 10, w / 2, 7 * h / 8, 0, -1000)
obj4 = object(4, 10, w / 2, 1 * h / 8, 0, 1000)




objects.append(obj1)
objects.append(obj2)
objects.append(obj3)
objects.append(obj4)





while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

    for obj in objects:
        pygame.draw.circle(screen, (255, 255, 255), (obj.x, obj.y), obj.radius)
        pygame.draw.line(screen, (255, 255, 255), (obj.x, obj.y), ((obj.x + (obj.fx / density)), (obj.y + (obj.fy / density))))

        obj.resultant(objects)





        
    clock.tick(60)
    pygame.display.flip()
    screen.fill((0,0,0))