# Example file showing a circle moving on screen
import pygame
import random

import numpy as np
import tensorflow as tf
import random
import math
from collections import deque

def defineModel(data, actionSize):

	model = tf.keras.models.Sequential([
		tf.keras.layers.Dense(64, activation='relu', input_shape=(len(data),)),
		tf.keras.layers.Dense(64, activation='relu'),
		tf.keras.layers.Dense(64, activation='relu'),
		tf.keras.layers.Dense(actionSize, activation=None)
	])


	return model

def predictModel(state, model):
	# Choose the action using the epsilon-greedy policy
	if np.random.uniform(0, 1) < epsilon:
		#action = np.random.randint(0, 2)
		action = random.randint(0,2)

		#epsilon = epsilon * epsilonDecay
	else:
		
		modelValues = model(np.expand_dims(state, axis=0))
		action = np.argmax(modelValues)
		#print(action)
	#print(action)
	return action


def DQN(batchSize, replayBuffer):


	
	
	if len(replayBuffer) >= batchSize:
		
		batch = random.sample(replayBuffer, batchSize)
		# Compute the target Q-values for the batch
		targets = []
		states = []
		for state, action, reward, next_state, done in batch:
			
			if done:
				target = reward
			else:
				
				nextModelValues = model(np.expand_dims(state, axis=0))
				maxModelValue = np.max(nextModelValues)
				target = reward + discount * maxModelValue
			
			#print("State:", state)
			targetModelValues = (model(np.expand_dims(state, axis=0)))
			targetModelValues = targetModelValues.numpy()
			#print("targetModelValues shape:", targetModelValues.shape)  # Add this line
			#print("Action:", action)  # Add this line
			targetModelValues[0][action] = target

			targets.append(targetModelValues)
			states.append(state)

		# Update the Q-value function
		targets = np.vstack(targets)
		states = np.vstack(states)
		with tf.GradientTape() as tape:
			# Compute the loss and gradients
			loss = tf.reduce_mean(tf.square(model(states) - targets))
			gradients = tape.gradient(loss, model.trainable_variables)
		
		# Apply the gradients
		optimizer.apply_gradients(zip(gradients, model.trainable_variables))
		replayBuffer.clear()
		model.compile()
		model.save('model.h5')

def gameState(playerPos, targetPos):
	xDist = playerPos[1] - targetPos[1]
	yDist = playerPos[0] - targetPos[0]
	vectorDist = math.sqrt((playerPos[0] - targetPos[0])**2 + (playerPos[1] - targetPos[1])**2)

	state = [xDist, yDist, vectorDist]
	return state

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
# Define the epsilon-greedy policy

epsilon = 0.99
epsilonDecay = 0.999
discount = 0.99
# Define the replay buffer
global replayBuffer

replayBuffer = deque(maxlen=100000)

def gameState(posX, posY, velX, velY, pY):
	if posY > pY:
		relative = 1
	else: 
		relative = 0
	
	return (posX, posY, velX, velY, pY, relative)

model = defineModel((0, 0, 0, 0, 0, 0), 3)

if input('Do you want to load the previous model? ') == 'y':
	model.load_weights('model.h5')







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

dt = 0

global paddle1Y

paddleHeight = 90


ballRad = 10
ball = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


global ballPosY

global ballVec


game = 0



while True:
	game += 1
	reward = 0

	acceleration = 0.001
	
	simpleDifficulty = 4
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


	print('Starting Game, ', game)
	while gameOver != True:


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
			reward -= 2
		elif collision(ball, paddle2):
			ballVelX = -ballVelX
			reward += 30
		if ballPosY < 0 or ballPosY > resolution[1]:
			ballVelY = -ballVelY
		if ballPosX < 0:
			winner = 1
			gameOver = True
			reward += 60
			print('CoolAI wins')
		elif ballPosX > resolution[0]:
			gameOver = True
			winner = 2
			reward -= 80
			print('BoringAI wins')


		prevHeight = paddle2Y

		
		state = gameState(ballPosX, ballPosY, ballVelX, ballVelY, paddle2Y)

		ballPosX += ballVelX
		ballPosY += ballVelY
		paddle1Y = simpleAI(paddle1Y, ballPosY)
		action = predictModel(state, model)
		

		if action == 1:
			paddle2Y -= 5
		elif action == 2:
			paddle2Y += 5
		else:
			paddle2Y += 0
			reward -= 0.1
		

			
		
		newState = gameState(ballPosX, ballPosY, ballVelX, ballPosY, paddle2Y)

		
		



		ball.xy = ballPosX, ballPosY

		
			

		




		# flip() the display to put your work on screen
		pygame.display.flip()

		# limits FPS to 60
		# dt is delta time in seconds since last frame, used for framerate-
		# independent physics.
		dt = clock.tick(60) / 1000

		ballVelX = ballVelX + acceleration * ballVelX
		ballVelY = ballVelY + acceleration * ballVelY
		acceleration *= accelerationDecay
		replayBuffer.append((state, action, reward, newState, gameOver))


	if winner == 1:
		simpleDifficulty += 0.5
	else:
		if simpleDifficulty > 4:
			simpleDifficulty -= 0.1

	print('The AI scored ', reward)
	print('The simpleAI difficulty is now:', simpleDifficulty)
	DQN(64, replayBuffer)


	epsilon *= epsilonDecay




	

		

pygame.quit()