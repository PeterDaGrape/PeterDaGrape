import numpy as np
import random
import math
import pygame
from perlin_noise import PerlinNoise
from PIL import Image
import os
import time


downscale = 3


width = 1920
height = 1080



num_particles = 1000 
max_magnitude = 0.1
vector_spacing = 60
max_speed = 1
start_speed = 1


fullscreen = False
show_vectors = True
clear_mode = False
render_enable = True

save = True


path = '/Users/Peter/iCloudDrive/wallpapers/frames'
path = '/Users/petervine/Desktop/frames'

vector_display_mult = 100

octaves = 0.75

print('Please enter seed, otherwise press enter:' )
seed = input()
if seed == '':
    seed = round(random.random(), 5)

else:
    seed = float(seed)

print('Seed used is:- ', seed)

pixel_strength = 0.1

damp_multiplier = 1

w = int(width / downscale)
h = int(height / downscale)







class vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        


    def set_magnitudes(self, max_magnitude):

        random_value = noise([self.x / w, self.y / h])

        angle = random_value * math.pi * 2

        self.vector_x = math.sin(angle) * max_magnitude
        self.vector_y = math.cos(angle) * max_magnitude

    def distance(self,p_x, p_y):
        
        return math.sqrt((self.x - p_x)**2 + (self.y - p_y)**2)

class particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        colour_choice = random.randint(0, 1)


        if colour_choice == 0:
            self.colour = [random.randint(200, 255), random.randint(100, 255), random.randint(200, 255)]
        else:
            self.colour = [73 + random.randint(-20, 20), 65 + random.randint(-20, 20), 109  + random.randint(-20, 20)]
        


        v = nearest_vector(self)
        self.vel_x = v.vector_x
        self.vel_y = v.vector_y

    def update(self):  

        current_speed = math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)



        if current_speed > max_speed:
            scale_factor = max_speed / current_speed
            self.vel_x *= scale_factor
            self.vel_y *= scale_factor

        v = nearest_vector(self)


        self.vel_x += v.vector_x
        self.vel_y += v.vector_y

     


        self.x += self.vel_x
        self.y += self.vel_y
        
def nearest_vector(particle):


    nearest = math.inf
    for v in vectors:
        distance = v.distance(particle.x, particle.y)
        if distance < nearest:
            nearest = distance
            particle.current_nearest = v


    
    return particle.current_nearest

def update_particles():
    for p in particles:

        
        v = nearest_vector(p)
        
        
        if p.x > w:
            p.x = 0
        if p.x < 0:
            p.x = w
        if p.y > h:
            p.y = 0
        if p.y < 0:
            p.y = h
        p.update()

def main():
    setup()
    while True:


        start_time = time.time()
        update_particles()
        print("Update time is \n --- %s seconds ---" % (time.time() - start_time))



        if render_enable:
            clock.tick(framerate)
            for event in pygame.event.get():
        
                if event.type == pygame.QUIT:
                    pygame.quit()
        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
        

        render()

def setup():


    global screen 
    global clock
    global framerate
    global noise
    global image_index
    global pixels 

    
    framerate = 60


    pixels = np.zeros((w, h, 3))

    if render_enable:
        pygame.init()
        clock = pygame.time.Clock()
        if fullscreen:
            screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((w, h))

    noise = PerlinNoise(octaves, seed)

    vectors = create_vectors(vector_spacing, max_magnitude)



    particles = create_particles(num_particles)





    image_index = 0


def create_vectors(vector_spacing, max_magnitude):
    global vectors
    vectors = []

    for x in range(w):
        if (x % vector_spacing == 0):
            for y in range(h):
                if (y % vector_spacing == 0):
                    v = vector(x + vector_spacing / 2, y + vector_spacing / 2)
                    v.set_magnitudes(max_magnitude)

                    vectors.append(v)



def create_particles(num_particles):
    global particles
    particles = []

    for particle_num in range(num_particles):


        p = particle(random.randint(0, w), random.randint(0,h))

        particles.append(p)

def save_file(pixels, image_index):
    frame = np.array(pixels, dtype=np.uint8)
    #frame = frame.swapaxes(0, 1) 
    frame = frame.swapaxes(0, 1)
    image = Image.fromarray(frame)
    image.save(os.path.join(path, f"frame_{image_index}.png"), "PNG")
    print('Saved image:', image_index)
    image_index += 1

def render():

    global image_index
    global pixels

    for p in particles:

        colour = p.colour
        '''
        try:
            pixel = pixels[int(p.x)][int(p.y)]
        except:
            continue
        
        damp_colour = [colour[0] * pixel_strength, colour[1] * pixel_strength, colour[2] * pixel_strength]
        
        new_pixel = [0, 0, 0]
        for value, i in zip(pixel, range(3)):
            space = 254 - value
            max_add = space / damp_multiplier
            actual_add = min(damp_colour[i], max_add)
            new_pixel[i] = value + actual_add

        pixels[int(p.x)][int(p.y)] = new_pixel


        '''
        try:
            pixels[int(p.x)][int(p.y)] += [colour[0] * pixel_strength, colour[1] * pixel_strength, colour[2] * pixel_strength]
            
            for i in range(3):
                if pixels[int(p.x)][int(p.y)][i] >= 255:
                    pixels[int(p.x)][int(p.y)][i] = 255
            
        except:
            continue
        
    if render_enable:
        pygame.surfarray.blit_array(screen, pixels)
        if show_vectors:
            for v in vectors:

                pygame.draw.line(screen, (255,255,255), (v.x, v.y), (v.x + v.vector_x * vector_display_mult, v.y + v.vector_y * vector_display_mult))
        pygame.display.flip()


    if clear_mode:
        pixels = np.zeros((w, h, 3))
    
    if save and image_index % 5 == 0:
        save_file(pixels, image_index)


    


    print('Rendered Frame ', image_index)
    image_index += 1

main()