import numpy as np
import random
import math
import pygame
from perlin_noise import PerlinNoise
from PIL import Image
import os

width = 2560
height = 1600

downscale = 4

num_particles = 1000
max_magnitude = 0.05
vector_spacing = 40
max_speed = 1
start_speed = 1

particle_rad = 1

show_vectors = True
line_mode = True
save = True
path = '/Users/Peter/iCloudDrive/wallpapers/frames'
path = '/Users/petervine/Desktop/frames'

octaves = 3
seed = random.random()

strength = 0.1

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
    def __init__(self):
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)

        self.vel_x = (2 * random.random() - 1) * start_speed
        up_or_down = random.choice([-1, 1])
        self.vel_y = math.sqrt((start_speed**2) - (self.vel_x**2)) * up_or_down


    def nearest_vector(self):
        nearest = math.inf
        for v in vectors:
            distance = v.distance(self.x, self.y)
            if distance < nearest:
                nearest = distance
                self.current_nearest = v


        
        return self.current_nearest

    def update(self, vec_x, vec_y):
        

        current_speed = math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)


        if current_speed > max_speed:
            scale_factor = max_speed / current_speed
            self.vel_x *= scale_factor
            self.vel_y *= scale_factor

        self.vel_x += vec_x
        self.vel_y += vec_y





   
        self.old_x = self.x
        self.old_y = self.y

        self.x += self.vel_x
        self.y += self.vel_y

def update_particles():
    for p in particles:
        v = p.nearest_vector()
        
        if p.x > w:
            p.x = 0
        if p.x < 0:
            p.x = w
        if p.y > h:
            p.y = 0
        if p.y < 0:
            p.y = h
        p.update(v.vector_x, v.vector_y)

def main():
    setup(int(width / downscale), int(height / downscale), vector_spacing, max_magnitude, num_particles)
    while True:

        update_particles()
        



        clock.tick(framerate)
        
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                pygame.quit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        
        render()

def setup(width, height, vector_spacing, max_magnitude, num_particles):

    global w
    global h
    global screen 
    global clock
    global framerate
    global noise

    global image_index


    image_index = 0
    
    framerate = 60
    h = height
    w = width

    global pixels 
    pixels = np.zeros((w, h, 3))

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size=(w, h))

    noise = PerlinNoise(octaves, seed)

    vectors = create_vectors(vector_spacing, max_magnitude)
    particles = create_particles(num_particles)

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

    for _ in range(num_particles):
        p = particle()
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



    for p in particles:
        try:
            pixels[int(p.x)][int(p.y)] += [255 * strength, 255 * strength, 255 * strength]

            for i in range(3):
                if pixels[int(p.x)][int(p.y)][i] >= 255:
                    pixels[int(p.x)][int(p.y)][i] = 255

        except:
            continue

    
 
    
    pygame.surfarray.blit_array(screen, pixels)

    for v in vectors:
        pygame.draw.line(screen, (255,255,255), (v.x, v.y), (v.x + v.vector_x * 100, v.y + v.vector_y * 100))
    if save and image_index % 5 == 0:
        save_file(pixels, image_index)


    pygame.display.flip()
    if not line_mode:
        screen.fill((0, 0, 0))

    image_index += 1

main()