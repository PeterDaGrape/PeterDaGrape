# Example file showing a circle moving on screen
import pygame
import random

import numpy as np

import random
import math



# Define the epsilon-greedy policy

epsilon = 0.6
epsilonDecay = 0.999
discount = 0.95
learning_rate = 0.1





def simpleAI(paddleY, targetY):
    if targetY > paddleY:
        paddleY += simpleDifficulty

    else:
        paddleY -= simpleDifficulty

    return paddleY 

def collision(ball, paddle_rect):
    ball_rect = pygame.Rect(ball.x - ballRad, ball.y - ballRad, ballRad*2, ballRad*2)
    if ball_rect.colliderect(paddle_rect):
        # Collision detected
        return True
    else:
        # No collision detected
        return False

resolution = (1280, 720)
accelerationDecay = 0.9995
global simpleDifficulty


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()


global paddle1Y

paddleHeight = 90


ballRad = 10
ball = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


global ballPosY

global ballVec


q_table_shape = [20, 20, 20, 20]

game = 0
def discretize(ball_x, ball_y, paddle_y, vel_x, vel_y):
    discrete_x = int(ball_x / resolution[0]) * q_table_shape[0]
    discrete_y = int((ball_y - paddle_y) / resolution[1] * q_table_shape[1])



    dis_vel_x = int((vel_x + 10) / 20 * q_table_shape[2])
    dis_vel_y = int((vel_y + 10) / 20 * q_table_shape[3])

    

    return tuple((discrete_x, discrete_y, dis_vel_x, dis_vel_y))






num_actions = 3



q_table = np.random.uniform(low = -2, high = 0, size = (q_table_shape + [num_actions]))



while True:
    game += 1

    acceleration = 0.001
    
    simpleDifficulty = 2.5
    paddle1Y = resolution[1] / 2
    paddle2Y = resolution[1] / 2

    gameOver = False

    initialVel = 4

    randomStart = random.randint(40, 80)
    randomDir = random.randint(0,1)
    ballPosX, ballPosY = resolution[0] / 2, resolution[1] / 2
    if randomDir == 0:
        dirMult = 1
    else:
        dirMult = -1
    ballVelX = (randomStart / 100) * initialVel
    ballVelY = (((initialVel ** 2) - (((randomStart / 100) * initialVel)  ** 2))**0.5) * dirMult

    state = discretize(ballPosX, ballPosY, paddle2Y, ballVelX, ballVelY)
    total_reward = 0
    print('Starting Game, ', game)
    while gameOver != True:
        reward = 0


        # poll for events

        

        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True

        # fill the screen with a color to wipe away anything from last frame

        paddle1 = pygame.Rect(0.075*resolution[0], paddle1Y - paddleHeight/2, 10, paddleHeight)
        paddle2 = pygame.Rect(0.925*resolution[0], paddle2Y - paddleHeight/2, 10, paddleHeight)

        screen.fill("white")

        pygame.draw.circle(screen, "red", ball, ballRad)
        pygame.draw.rect(screen, 'black', paddle1)
        pygame.draw.rect(screen, 'black', paddle2)


        
        if collision(ball, paddle1):
            ballVelX = -ballVelX
            reward -= 1
        elif collision(ball, paddle2):
            ballVelX = -ballVelX
            reward += 10


        if ballPosY < ballRad or ballPosY > resolution[1] - ballRad:
            ballVelY = -ballVelY
        if ballPosX < ballRad:
            winner = 1
            gameOver = True
            reward += 6
            print('CoolAI wins')
        elif ballPosX > resolution[0] - ballRad:
            gameOver = True
            winner = 2
            reward -= 8
            print('BoringAI wins')


        prevHeight = paddle2Y

        



        ballPosX += ballVelX
        ballPosY += ballVelY



        paddle1Y = simpleAI(paddle1Y, ballPosY)
        

        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, num_actions-1)
        else:
            try:
                action = np.argmax(q_table[state])
            except:
                action = 0        

        

        if action == 1:
            paddle2Y -= 5
        elif action == 2:
            if paddle2Y < resolution[1]:
                if paddle2Y > 0:
                    paddle2Y += 5
        else:
            paddle2Y += 0
            reward -= 0.1
        

            
        
        new_state = discretize(ballPosX, ballPosY, paddle2Y, ballVelX, ballVelY)
        
        if not gameOver:
            try:
                max_future_q = np.max(q_table[new_state])

                current_q = q_table[state + (action, )]

                new_q = (1 - learning_rate) * current_q + learning_rate * (reward + discount * max_future_q)

                q_table[state + (action, )] = new_q
            except:
                pass
        

        state = new_state

        ball.xy = ballPosX, ballPosY

        
            

        




        #pygame.display.flip()

        #clock.tick(60)

        ballVelX = ballVelX + acceleration * ballVelX
        ballVelY = ballVelY + acceleration * ballVelY
        acceleration *= accelerationDecay
        total_reward += reward


    if winner == 1:
        simpleDifficulty += 0.2
    else:
        if simpleDifficulty > 2:
            simpleDifficulty -= 0.1

    print('The AI scored ', total_reward, 'epsilon is', epsilon)
    print('The simpleAI difficulty is now:', simpleDifficulty)


    epsilon *= epsilonDecay




    

        

pygame.quit()