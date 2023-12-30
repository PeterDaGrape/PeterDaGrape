import numpy as np
import random
import math
import pygame
from perlin_noise import PerlinNoise
from PIL import Image
import os
import time

downscale = 1

width = 1170
height = 2532

num_particles = 25000
max_magnitude = 1
vector_spacing = 1
max_speed = 1
start_speed = 1

fullscreen = False
show_vectors = False
show_particles = True
clear_mode = False
render_enable = True

request_seed = False

brightness_multiplier = 1

wrap_mode = False

save = True

verbose_print = False

save_period = 50

pixel_strength = 0.1


path = '/Users/petervine/Desktop/frames'

vector_display_mult = 150
display_alpha = 40

octaves = 1.5
if request_seed:
    print('Please enter seed, otherwise press enter:' )
    seed = float(input())
else:
    seed = round(random.random(), 5)



print('Seed used is:- ', seed)



w = int(width / downscale)
h = int(height / downscale)

class vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
        random_value = noise([self.x / w, self.y / h])

        angle = random_value * math.pi * 2
        self.vector_x = math.sin(angle) * max_magnitude
        self.vector_y = math.cos(angle) * max_magnitude

class particle:
    def __init__(self, x, y, index):

        self.index = index
        self.x = x
        self.y = y
        
        colour_choice = random.randint(0, 1)

        if colour_choice == 0:
            self.colour = [random.randint(220, 255), random.randint(100, 255), random.randint(170, 255)]
        else:
            self.colour = [73 + random.randint(-10, 40), 65 + random.randint(-40, 40), 109  + random.randint(-40, 40)]
        
        self.vel_x = 0
        self.vel_y = 0
        self.alive = True

    def update(self):  

        cell_x = int(self.x / vector_spacing)
        cell_y = int(self.y / vector_spacing)
        nearest_dist = float('inf')
        nearest_vec = None

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor_x = cell_x + dx
                neighbor_y = cell_y + dy

                if (0 <= neighbor_x < w // vector_spacing) and (0 <= neighbor_y < h // vector_spacing):
                    for vec in grid[neighbor_x][neighbor_y]:

                        dist = math.sqrt((vec.x - self.x)**2 + (vec.y - self.y)**2)
                        if dist < nearest_dist:
                            nearest_dist = dist
                            nearest_vec = vec


        current_speed = math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)

        if current_speed > max_speed:
            scale_factor = max_speed / current_speed
            self.vel_x *= scale_factor
            self.vel_y *= scale_factor


        self.vel_x += nearest_vec.vector_x
        self.vel_y += nearest_vec.vector_y

        self.x += self.vel_x
        self.y += self.vel_y

def update_particles():
    for p in particles:


        if p.x > w:
            if not wrap_mode:
                p.alive = False
            p.x = 0
        if p.x < 0:
            if not wrap_mode:
                p.alive = False
            p.x = w
        if p.y > h:
            if not wrap_mode:
                p.alive = False
            p.y = 0
        if p.y < 0:
            if not wrap_mode:
                p.alive = False
            p.y = h
        if not p.alive:

            replace_dead(p.index)
            continue
        p.update()

def replace_dead(index):
    global particles
    particles[index] = particle(random.randint(0, w), random.randint(0,h), index)

def main():
    global seed
    global screen 
    global clock
    global framerate
    global noise
    global image_index
    global pixels 

    framerate = 60

    if render_enable:
        pygame.init()
        clock = pygame.time.Clock()
        if fullscreen:
            screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((w, h))
    pixels = np.zeros((w, h, 3))

    noise = PerlinNoise(octaves, seed)

    vectors = create_vectors(vector_spacing)
    particles = create_particles(num_particles)

    image_index = 0
    num_frames = 0

    while True:

        if verbose_print:
            start_time = time.time()
        update_particles()
        if verbose_print:
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


        num_frames += 1

def create_vectors(vector_spacing):
    global vectors
    global grid


    vectors = []

    grid = [[[] for _ in range(h // vector_spacing)] for _ in range(w // vector_spacing)]
    for x in range(int(w / vector_spacing)):
        for y in range(int(h / vector_spacing)):
            v = vector(x * vector_spacing + vector_spacing / 2, y * vector_spacing + vector_spacing / 2)
            
            # Assign vector to the appropriate grid cell
            cell_x = int(v.x / vector_spacing)
            cell_y = int(v.y / vector_spacing)
            grid[cell_x][cell_y].append(v)
            
            vectors.append(v)

def create_particles(num_particles):
    global particles
    particles = []

    for particle_num in range(num_particles):
        p = particle(random.randint(0, w), random.randint(0,h), particle_num)

        particles.append(p)

def save_file(pixels, image_index):
    frame = np.array(pixels, dtype=np.uint8)
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

        try:

            existing_pixel = pixels[int(p.x)][int(p.y)]

            pixels[int(p.x)][int(p.y)] += ((255, 255, 255) - existing_pixel) / (255,255,255) * (colour[0] * pixel_strength, colour[1] * pixel_strength, colour[2] * pixel_strength)
            #pixels[int(p.x)][int(p.y)] /= 255 * colour
            #pixels[int(p.x)][int(p.y)] += [colour[0] * pixel_strength, colour[1] * pixel_strength, colour[2] * pixel_strength]
            
            for i in range(3):
                if pixels[int(p.x)][int(p.y)][i] >= 255:
                    pixels[int(p.x)][int(p.y)][i] = 255
            
        except:
            continue
        
    if render_enable:

        pygame.surfarray.blit_array(screen, pixels)
        surface = pygame.Surface((w, h))

        if show_particles:
            for p in particles:
                pygame.draw.line(surface, p.colour, (p.x, p.y), (p.x, p.y))
                #pygame.draw.circle(screen, p.colour, (p.x, p.y), 1)
        if show_vectors:
            for v in vectors:

                pygame.draw.line(surface, (255,255,255), (v.x, v.y), (v.x + v.vector_x * vector_display_mult, v.y + v.vector_y * vector_display_mult))
        surface.set_alpha(display_alpha)
        screen.blit(surface, (0,0))
        pygame.display.flip()

    if clear_mode:
        pixels = np.zeros((w, h, 3))
    
    if save and image_index % save_period == 0:
        save_file(pixels, image_index)
    
    pixels *= brightness_multiplier

    if verbose_print:
        print('Rendered Frame ', image_index)
    image_index += 1

main()