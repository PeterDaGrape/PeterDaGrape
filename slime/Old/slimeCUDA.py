import pygame
import random
import numpy as np
import math
#import cupy as cp
from PIL import Image
import os
from scipy.ndimage.filters import uniform_filter



def ballCreate(numBalls):




    if useCuda:
        balls = cp.zeros((numBalls, 3, 2), dtype=cp.float32)

        for i in range(numBalls):
            initialPos = cp.array([resolution[0] / 2, resolution[1] / 2], dtype=cp.float32)
            angle = random.randint(0, 360)

            initialVel = cp.array([velocity*math.sin(math.radians(angle)), velocity * math.cos(math.radians(angle))], dtype=cp.float32)

            balls[i, 0] = initialPos
            balls[i, 1] = initialVel
        return balls
    else:
        ballsF = []
    
    
    for i in range(numBalls):
        initialPos = [resolution[0] / 2, resolution[1] / 2]
        angle = random.randint(0, 360)

        initialVel = [velocity*math.sin(math.radians(angle)), velocity * math.cos(math.radians(angle))]

        ballF = pygame.Vector2(initialPos)

        ballsF.append([ballF, initialPos, initialVel])
    return ballsF

#kernel = np.ones((3, 3)) / 9
'''
'''
kernel_code = '''
extern "C" __global__
void ballsUpdate(float* balls, int num_balls, int velocity, int* resolution)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (i < num_balls)
    {
        float* ballC = &balls[i * 6];
        float* velC = &balls[i * 6 + 2];

        

        int xMult, yMult;
        unsigned int seed = (unsigned int)clock();
        seed = seed * i * 1103515245 + 12345;
        int random_value = (unsigned int)(seed / 65536) % 32768;

        if (ballC[0] > resolution[0])
        {
            xMult = -1;
            yMult = (random_value % 2 == 0) ? 1 : -1;
            ballC[0] = resolution[0] - 1;
        }
        else if (ballC[0] < 0)
        {
            xMult = 1;
            yMult = (random_value % 2 == 0) ? 1 : -1;
            ballC[0] = 1;
        }
        else if (ballC[1] > resolution[1])
        {
            xMult = (random_value % 2 == 0) ? 1 : -1;
            yMult = -1;
            ballC[1] = resolution[1] - 1;
        }
        else if (ballC[1] < 0)
        {
            xMult = (random_value % 2 == 0) ? 1 : -1;
            yMult = 1;
            ballC[1] = 1;
        }
        else
        {
            ballC[0] = ballC[0] + velC[0];
            ballC[1] = ballC[1] + velC[1];
            return;
        }

        int angle = random_value % 360;
        float rad = angle * 0.0174532925; // Convert to radians
        velC[0] = velocity * sinf(rad) * xMult;
        velC[1] = velocity * cosf(rad) * yMult;

        ballC[0] = ballC[0] + velC[0];
        ballC[1] = ballC[1] + velC[1];
        return;

    }
}
'''

#balls_update_kernel = cp.RawKernel(kernel_code, 'ballsUpdate')

def balls_update_gpu(balls, resolution, velocity, block_size=1024):
    num_balls = balls.shape[0]
    grid_size = (num_balls + block_size - 1) // block_size
    balls_update_kernel((grid_size,), (block_size,), (balls, num_balls, velocity, resolution))
    
    balls = cp.asnumpy(balls)



    return balls

def updateBalls(balls):
    index = -1
    for ball in balls:

        ballC, position, velC = ball
        index += 1





        if ballC[0] > resolution[0]:
            xMult = -1
            yMult = random.choice([1, -1])
            ballC[0] = resolution[0] - 1
        elif ballC[0] < 0:
            xMult = 1
            yMult = random.choice([1, -1])
            ballC[0] = 1
        elif ballC[1] > resolution[1]:
            xMult = random.choice([1, -1])
            yMult = -1
            ballC[1] = resolution[1] - 1
        elif ballC[1] < 0:
            xMult = random.choice([1, -1])
            yMult = 1
            ballC[1] = 1
        else:
            ballC += velC
            balls[index] = ball

            continue
        angle = random.randint(0, 360)
        velC = [velocity * math.sin(math.radians(angle)) * xMult, velocity * math.cos(math.radians(angle))*int(yMult)]
        ballC += velC

        ball = ballC, position, velC
        balls[index] = ball

    return balls


if not 'CUDA_VISIBLE_DEVICES' in os.environ:
    print('No GPU found! ')
    useCuda = False
else:
    print('GPU detected! ')
    useCuda = True
useCuda = False




numBalls = 200
ballRad = 1
velocity = 1
resolution = (1280, 720)
print('Creating Balls...')

balls = ballCreate(numBalls)

print('Created balls, starting...')

clock = pygame.time.Clock()


orbColour = 'white'

pygame.init()
if useCuda:
    pixels = cp.zeros((resolution[0], resolution[1]), 3)
else:
    pixels = np.zeros((resolution[0], resolution[1], 3))
screen = pygame.display.set_mode(resolution)
surface = pygame.surfarray.make_surface(pixels)

if useCuda:
    resolution = cp.array([resolution])


while True:
    pygame.event.get()

    if useCuda:
        balls = cp.array(balls)
        balls = balls_update_gpu(balls, resolution, velocity)
    else:
        balls = updateBalls(balls)

    
    for ball in balls:
        ballV, position, velC = ball
        #ballV =  tuple(map(int, cp.asnumpy(ballV)))
        try:
            pixels[ballV] = 255
        except:
            continue
    
    
    
    


    pygame.surfarray.blit_array(surface, pixels)


    pygame.display.flip()

    pixels *= 0.98

    pixels = uniform_filter(pixels, size=(3, 3, 1))



    
    screen.blit(surface, (0, 0))



    clock.tick(60)
    
    


    
