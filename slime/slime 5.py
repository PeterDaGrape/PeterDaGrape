import random
import numpy as np
import math
from PIL import Image
import os

num_agents = 10000
frame_rate = 60
speed_var = 0
w = 2560
h = 1600
downscale = 4

w = int(w / downscale)
h = int(h / downscale)
agent_speed = 1

colours = [(0, 0, 255), 
           (0, 255, 0), 
           (0, 255, 255), 
           (255, 0, 0), 
           (255, 0, 255), 
           (255, 255, 0)]


colours = [(255, 255, 255)]





fade = 0.97
sensor_angle = 35
sensor_distance = 60
max_turn = math.radians(14)
rad_factor = 1

path = 'frames' 
#path = '/Users/petervine/Desktop/frames'

render = True
save = False
fullscreen = False


sensor_distance = int(sensor_distance / downscale)

def save_file(pixels, image_index):
    frame = np.array(pixels, dtype=np.uint8)
    #frame = frame.swapaxes(0, 1) 
    frame = frame.swapaxes(0, 1)
    image = Image.fromarray(frame)
    image.save(os.path.join(path, f"frame_{image_index}.png"), "PNG")
    print('Saved image:', image_index)
    image_index += 1

class Agent:
    def __init__(self):
        
        spawn_radius = int(h * rad_factor / 2)  

        random_circle_x = random.randint(-spawn_radius, spawn_radius)
        random_circle_y = random.randint(-spawn_radius, spawn_radius)

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
    
    def update(self, pixels):
        self.collision()
        self.brain(pixels)
        self.move()

    def move(self):

        self.vel_x = agent_speed * math.sin(self.agent_angle)
        self.vel_y = agent_speed * math.cos(self.agent_angle)

        self.x += self.vel_x
        self.y -= self.vel_y
    
    def collision(self):

        
        if self.x > w:
            self.x = w - 1
            self.agent_angle = math.radians(random.randint(180, 360))
        elif self.x < 0:
            self.x = 1
            self.agent_angle = math.radians(random.randint(0, 180))
        elif self.y > h:
            self.y = h - 1
            self.agent_angle = math.radians(random.randint(270, 450))
        elif self.y < 0:
            self.y = 1
            self.agent_angle = math.radians(random.randint(90, 270))

    def brain(self, pixels):
        scent_strengths = []
        angles = self.agent_angle, self.agent_angle - sensor_angle, self.agent_angle + sensor_angle
        for probe_angle in angles:
            probe_position = [int(self.x + sensor_distance * math.sin(math.radians(probe_angle))),
                            int(self.y - sensor_distance * math.cos(math.radians(probe_angle)))]
            if probe_position[0] > w - 1 or probe_position[0] < 0 or probe_position[1] > h - 1 or probe_position[1] < 0:
                score = -10000
            
            else:
                probe_pixel = pixels[probe_position[0]][probe_position[1]]
                distance = math.sqrt((probe_pixel[0] - self.colour[0])**2 + (probe_pixel[1] - self.colour[1])**2 + (probe_pixel[2] - self.colour[2])**2)
                score = -distance

            #pixels[probe_position[0], probe_position[1]] = (255,255,255)

            scent_strengths.append(score)
        probe_forward = scent_strengths[0]
        probe_left = scent_strengths[1]
        probe_right = scent_strengths[2]


        if probe_forward < probe_left and probe_forward < probe_right:
            self.agent_angle += (random.random() - 0.5) * 2 * max_turn
        elif probe_left > probe_right:

            self.agent_angle -= random.random() * max_turn
        elif probe_left < probe_right:

            self.agent_angle += random.random() * max_turn
        
def screen_refresh(agents, image_index, pixels):
    if not fallback and render:
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                pygame.quit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        screen.blit(surface, (0, 0))
    
    pixels *= fade
    #comment this out to disable blur
    #pixels = uniform_filter(pixels, size=(3, 3, 1))
    

    for agent in agents:
    
        try:
            pixels[int(agent.x), int(agent.y)] = agent.colour

        except:
            continue
    
    if render and not fallback:
        pygame.event.get()
        pygame.surfarray.blit_array(screen, pixels)
        
        pygame.display.flip()
        clock.tick(frame_rate)
        #print(clock.get_fps())
    if save:
        save_file(pixels, image_index)


    pixels = cv2.blur(pixels, (3, 3))

    return pixels

def agent_create(num_agents):
    agents = []

    for _ in range(num_agents):
        agents.append(Agent())
    return agents

def main(pixels):

    image_index = 0
    print('Creating Agents...')
    
    agents = agent_create(num_agents)
    print('Created Agents, starting...')
    while True:

        for agent in agents:
            agent.update(pixels)
        pixels = screen_refresh(agents, image_index, pixels)
        image_index += 1

if __name__ == '__main__':

    try:
        from scipy.ndimage.filters import uniform_filter
        import cv2
        import pygame
        fallback = False
    except:
        print('Recommended modules not found... ')
        fallback = True
    pixels = np.zeros((w, h, 3))


    if not fallback and render:
        
        pygame.init()
        clock = pygame.time.Clock()

        if fullscreen:
            screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((w, h))
        surface = pygame.surfarray.make_surface(pixels)
    main(pixels)