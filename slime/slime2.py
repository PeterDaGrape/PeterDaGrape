import pygame
import random
import numpy as np
import math
from PIL import Image
import os
from scipy.ndimage.filters import uniform_filter
from concurrent import futures
import multiprocessing
import time

num_agents = 5000
frame_rate = math.inf
speed = 1
speed_var = 0.5
resolution = (1280, 720)
agent_colour = (255, 255, 255)
agent_rad = 1
fade = 0.985
pygame.init()

sensor_angle = 10
sensor_distance = 8
clock = pygame.time.Clock()
pixels = np.zeros((resolution[0], resolution[1], 3))
screen = pygame.display.set_mode(resolution)
surface = pygame.surfarray.make_surface(pixels)
intensity_threshold = 235
max_turn = 6
rad_factor = 0.7

path = '/Users/petervine/Desktop/frames'
image_index = 0 


render = True
save = False
num_processes = 4



def save_file(pixels):
    global image_index
    frame = np.array(pixels, dtype=np.uint8)
    #frame = frame.swapaxes(0, 1) 
    frame = frame.swapaxes(0, 1)
    image = Image.fromarray(frame)
    image.save(os.path.join(path, f"frame_{image_index}.png"), "PNG")
    image_index += 1

def agent_create(num_agents):
    agents = []


    center_x = resolution[0] // 2
    center_y = resolution[1] // 2
    angle_increment = 360 / num_agents



    for i in range(num_agents):
        agent_speed = random.randint(int((speed - speed_var) * 100), int((speed + speed_var) * 100)) / 100
        #defines the initial position

        
        particle_bearing = (i * angle_increment)
        angle_rad = math.radians(particle_bearing)
        #particle_bearing = random.randint(0,360)

        radius = min(resolution) * rad_factor / 2  # Adjust the radius as needed

        distance = random.uniform(0, radius)
        start_pos = [resolution[0] - int(center_x + distance * math.sin(angle_rad)), int(center_y + distance * math.cos(angle_rad))]

        '''
        start_pos = [resolution[0] / 2, resolution[1] / 2]
        start_pos = list(map(int, start_pos))
        '''



        #creates a direction vector to follow, based off the angle set in particle_bearing
        velocity_vec = [agent_speed * math.sin(math.radians(particle_bearing)), agent_speed * math.cos(math.radians(particle_bearing))]

        #creates a list of paramaters of each agent
        #the last element refers to the scent detectors, first is up, second is left, third is right
        agent = [start_pos, particle_bearing, velocity_vec, agent_speed]

        #creates a list of lists, this can be easily returned
        
        agents.append(agent)
    return agents

def agent_collision(agent_pos, agent_bearing, agent_vel):
    update = True

    
    if agent_pos[0] > resolution[0]:
        agent_pos[0] = resolution[0] - 1
        angle = random.randint(180, 360)
    elif agent_pos[0] < 0:
        agent_pos[0] = 1
        angle = random.randint(0, 180)
    elif agent_pos[1] > resolution[1]:
        agent_pos[1] = resolution[1] - 1
        angle = random.randint(270, 450)
    elif agent_pos[1] < 0:
        agent_pos[1] = 1
        angle = random.randint(90, 270)
    else:
        update = False


    if update:
        if angle >= 360:
            angle -= 360
        agent_bearing = angle
    #agent_pos += agent_vel

    return agent_pos, agent_bearing, agent_vel
 
def brain(position, angle, pixels):
    scent_strengths = []

    angles = angle, angle - sensor_angle, angle + sensor_angle

    for probe_angle in angles:
        probe_position = [int(position[0] + sensor_distance * math.sin(math.radians(probe_angle))),
                int(position[1] - sensor_distance * math.cos(math.radians(probe_angle)))]

        #pixels[probe_position[0]][probe_position[1]] = (255, 255, 255)
        
        try:
            total_rgb = 0
            probe_pixel = pixels[probe_position[0]][probe_position[1]]
            for rgb in probe_pixel:
                total_rgb += rgb

        except:
            scent_strengths.append(-1)
            
            continue

        total_rgb /= 3
        scent_strengths.append(total_rgb)
    probe_forward = scent_strengths[0]
    probe_left = scent_strengths[1]
    probe_right = scent_strengths[2]

    if probe_forward < probe_left and probe_forward < probe_right:
        angle += (random.random() - 0.5) * 2 * max_turn
    elif probe_left > probe_right:
        if probe_left > intensity_threshold:
            angle += random.random() * max_turn
        else:
            angle -= random.random() * max_turn
    elif probe_left < probe_right:
        if probe_right > intensity_threshold:
            angle -= random.random() * max_turn
        else:
            angle += random.random() * max_turn
    return angle

def move_agent(pos, angle, velocity, agent_speed):
        velocity = [agent_speed * math.sin(math.radians(angle)), agent_speed * math.cos(math.radians(angle))]   
        pos[0] += velocity[0]
        pos[1] -= velocity[1]
        return pos, velocity

def agent_update(agent, pixels):

    position, angle, velocity, speed = agent
    #update agent code

    #check for collisions and change if needed
    
    position, angle, velocity = agent_collision(position, angle, velocity)


    angle = brain(position, angle, pixels)
    position, velocity = move_agent(position, angle, velocity, speed)
    

    #subroutine that changes the position from velocity
    agent = position, angle, velocity, speed
    return agent

def agents_start(agents, pixels):
    agent_index = 0
    for agent in agents:
        agent = agent_update(agent, pixels)
        agents[agent_index] = agent
        agent_index += 1
    return agents

def screen_refresh(agents, pixels):

    
    pixels *= fade
    #comment this out to disable blur
    pixels = uniform_filter(pixels, size=(3, 3, 1))
   
    screen.blit(surface, (0, 0))

    for agent in agents:
        agent_pos, agent_bearing, agent_vel = agent[:3]
        agent_pos = list(map(int, agent_pos))
        try:
            pixels[agent_pos[0]-1:agent_pos[0]+2, agent_pos[1]-1:agent_pos[1]+2] = agent_colour

        except:
            continue

    if render:
        pygame.event.get()
        pygame.surfarray.blit_array(surface, pixels)
        
        pygame.display.flip()
        clock.tick(frame_rate)
        print(clock.get_fps())

    return pixels

def main():

    print('Creating Agents...')
    agents = agent_create(num_agents)
    print('Created Agents, starting...')
    tasks = []
    while True:
        global pixels
        '''
        with multiprocessing.Pool() as executor:
            # Submit agent processing tasks to the executor
            agent_futures = [executor.apply_async(agent_update, (agent, pixels)) for agent in agents]

            for future in agent_futures:
                future.get()

            agents = [future.get() for future in agent_futures]
        '''
        agents = agents_start(agents, pixels)

        pixels = screen_refresh(agents, pixels)

        if save:
            save_file(pixels)


if __name__ == '__main__':
    main()


