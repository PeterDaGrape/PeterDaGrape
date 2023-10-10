import random
import numpy as np
import math
from PIL import Image
import os
import cv2



num_agents = 10000
frame_rate = 60
speed = 1
speed_var = 0
resolution = (2560, 1600)
downscale = 3


agent_colour = (255, 255, 255)
fade = 0.97
sensor_angle = 35
sensor_distance = 50
max_turn = 16
rad_factor = 1

path = 'frames' 
path = "/Users/petervine/Desktop/macframes"




render = True
save = False
fullscreen = False
resolution = int(resolution[0] / downscale), int(resolution[1] / downscale)

pixels = np.zeros((resolution[0], resolution[1], 3))

sensor_distance = int(sensor_distance / downscale)

def save_file(pixels, image_index):
    frame = np.array(pixels, dtype=np.uint8)
    #frame = frame.swapaxes(0, 1) 
    frame = frame.swapaxes(0, 1)
    image = Image.fromarray(frame)
    image.save(os.path.join(path, f"frame_{image_index}.png"), "PNG")
    print('Saved image:', image_index)
    image_index += 1

def agent_create(num_agents):
    agents = []

    for i in range(num_agents):
        agent_speed = random.randint(int((speed - speed_var) * 100), int((speed + speed_var) * 100)) / 100
        #defines the initial position

        

        radius = int(min(resolution) * rad_factor / 2)  # Adjust the radius as needed

        
        
        #start_pos = [resolution[0] / 2, resolution[1] / 2]
        #start_pos = list(map(int, start_pos))

        start_pos = [0, 0]

        random_circle = [random.randint(-radius, radius), random.randint(-radius, radius)]


        while math.sqrt(random_circle[0]**2 + random_circle[1]**2) > radius:
            random_circle = [random.randint(-radius, radius), random.randint(-radius, radius)]

        start_pos = [resolution[0] // 2 + random_circle[0], resolution[1] // 2 + random_circle[1]]

        particle_bearing = math.degrees(math.atan2(start_pos[1] - resolution[1] // 2, start_pos[0] - resolution[0] // 2)) - 90
        particle_bearing += (random.random()-0.5) * 180
        



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

    return agent_pos, agent_bearing, agent_vel
 
def brain(position, angle, pixels):
    scent_strengths = []

    angles = angle, angle - sensor_angle, angle + sensor_angle

    for probe_angle in angles:
        probe_position = [int(position[0] + sensor_distance * math.sin(math.radians(probe_angle))),
                          int(position[1] - sensor_distance * math.cos(math.radians(probe_angle)))]

        #pixels[probe_position[0]][probe_position[1]] = (255, 255, 255)
        
        total_rgb = 0
        try:
            probe_pixel = pixels[probe_position[0]][probe_position[1]]
            for rgb in probe_pixel:
                total_rgb += rgb
        except:
            scent_strengths.append(-255)
            continue

        total_rgb /= 3
        scent_strengths.append(total_rgb)

    probe_forward = scent_strengths[0]
    probe_left = scent_strengths[1]
    probe_right = scent_strengths[2]

    if probe_forward < probe_left and probe_forward < probe_right:
        angle += (random.random() - 0.5) * 2 * max_turn
    elif probe_left > probe_right:

        angle -= random.random() * max_turn
    elif probe_left < probe_right:

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

def uniform_filter(pixels, size=(3, 3, 1)):
    # Extracting dimensions of the input image
    height, width, channels = pixels.shape
    
    # Creating a padded array with zeros to handle border cases
    padded_pixels = np.pad(pixels, ((1, 1), (1, 1), (0, 0)), mode='constant')
    
    # Creating an empty output array
    output = np.zeros_like(pixels)
    
    # Iterating over each pixel in the image

    for i in range(1, height + 1):
        for j in range(1, width + 1):
            # Extracting the neighborhood region
            region = padded_pixels[i-1:i+2, j-1:j+2, :]
            
            # Calculating the mean value for each channel
            mean_value = np.mean(region, axis=(0, 1))
            
            # Assigning the mean value to the corresponding pixel in the output image
            output[i-1, j-1, :] = mean_value
    
    return output

def screen_refresh(agents, pixels):
    
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
    pixels = cv2.blur(pixels, (3, 3))
    

    

    for agent in agents:
        agent_pos, agent_bearing, agent_vel = agent[:3]
        agent_pos = list(map(int, agent_pos))
        try:
            #pixels[agent_pos[0]-1:agent_pos[0]+2, agent_pos[1]-1:agent_pos[1]+2] = agent_colour
            pixels[agent_pos[0], agent_pos[1]] = agent_colour

        except:
            continue

    if render and not fallback:
        pygame.event.get()
        pygame.surfarray.blit_array(surface, pixels)
        
        pygame.display.flip()
        clock.tick(frame_rate)
        #print(clock.get_fps())

    return pixels

def main():
    global pixels
    global fallback

    image_index = 0 

    print('Creating Agents...')
    agents = agent_create(num_agents)
    print('Created Agents, starting...')

    while True:

        agents = agents_start(agents, pixels)

        pixels = screen_refresh(agents, pixels)

        if save:
            save_file(pixels, image_index)
            image_index += 1


if __name__ == '__main__':

    try:
        from scipy.ndimage.filters import uniform_filter
        import pygame
        fallback = False
    except:
        print('Recommended modules not found... ')
        fallback = True

    if not fallback and render:
        
        pygame.init()
        clock = pygame.time.Clock()

        if fullscreen:
            screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(resolution)


        surface = pygame.surfarray.make_surface(pixels)
    main()


