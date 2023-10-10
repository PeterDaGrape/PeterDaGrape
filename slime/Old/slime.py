import pygame
import random
import math



def ballCreate(numBalls):
    ballsF = []
    
    
    for i in range(numBalls):
        initialPos = [resolution[0] / 2, resolution[1] / 2]
        angle = random.randint(0, 360)

        initialVel = [velocity*math.sin(math.radians(angle)), velocity * math.cos(math.radians(angle))]

        ballF = pygame.Vector2(initialPos)

        ballsF.append([ballF, initialPos, initialVel])
    return ballsF

def ballUpdate(ball):
    ballC, position, velC = ball


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
        return ball
    angle = random.randint(0, 360)
    velC = [velocity * math.sin(math.radians(angle)) * xMult, velocity * math.cos(math.radians(angle))*int(yMult)]
    ballC += velC

    ball = ballC, position, velC
    
    return ball

def correctBounds(ballC, velC):
    
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
        return velC, ballC

    angle = random.randint(0, 360)
    velC = [velocity * math.sin(math.radians(angle)) * xMult, velocity * math.cos(math.radians(angle))*int(yMult)]
    

    return velC, ballC

resolution = (1280, 720)

screen = pygame.display.set_mode(resolution)

clock = pygame.time.Clock()

screen.fill('Black')

orbColour = 'white'


ballRad = 1

velocity = 1

numBalls = 1000
balls = ballCreate(numBalls)



while True:
    pygame.event.get()
    
    # create a copy of the screen surface
    fadeout = screen.copy()

    # get the pixel values of the screen as a 3D numpy array
    pixels = pygame.surfarray.pixels3d(fadeout)

    # reduce the brightness of the pixel values by 50%
    pixels = pixels * 0.99

    fadedSurface = pygame.surfarray.make_surface(pixels)

    fadedSurface.set_alpha(254)
    screen.fill('black')

    screen.blit(fadedSurface, (0, 0))
    
    # update the ball positions
    
    
    for balli in range (len(balls)):
        

        '''
        ballV, position, vel = ball

        vel, ballV = correctBounds(ballV, vel)
        ballV += vel

        balls[balli] = ballV, position, vel

        '''
        
        balls[balli] = ballUpdate(balls[balli])
        ballV, position, vel = balls[balli]


        pygame.draw.circle(screen, orbColour, ballV, ballRad) 






    # wait for all jobs to complete and get the results

    # update the display
    clock.tick(60)
    pygame.display.flip()

    
