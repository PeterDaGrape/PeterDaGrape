# Example file showing a circle moving on screen
import pygame
import random
import concurrent.futures
import numpy as np
import tensorflow as tf
import random
from collections import deque

def defineModel(data, actionSize):

	model = tf.keras.models.Sequential([
		tf.keras.layers.Dense(64, activation='relu', input_shape=(len(data),)),
		tf.keras.layers.Dense(64, activation='relu'),
		tf.keras.layers.Dense(64, activation='relu'),
		tf.keras.layers.Dense(actionSize, activation='softmax')
	])


	return model

def predictModel(state, model):
	# Choose the action using the epsilon-greedy policy

	#print('Data provided, ', state)
	if np.random.uniform(0, 1) < epsilon:
		#action = np.random.randint(0, 2)
		action = random.randint(0,2)

		#epsilon = epsilon * epsilonDecay
	else:
		
		modelValues = model(np.expand_dims(state, axis=0))
		action = np.argmax(modelValues)
		#print(action)
	#print('Model gave,', action)
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
	
def run_multiple_games(n_games):
	replay_buffers = []
	game_outcomes = []
	rewards = []

	with concurrent.futures.ThreadPoolExecutor() as executor:
		futures = [executor.submit(runGame, game_id) for game_id in range(n_games)]

		for future in concurrent.futures.as_completed(futures):
			replay_buffer, game_outcome, reward = future.result()
			replay_buffers.append(replay_buffer)
			game_outcomes.append(game_outcome)
			rewards.append(reward)

	return replay_buffers, game_outcomes, rewards

def rewardFunc(posX, posY, winner, action, paddle, velX, pY, passedLine):
	reward = 0
	differenceY = pY - posY
	if differenceY < 0:
		differenceY *= -1

	differenceReward = (round(differenceY / (0.5*resolution[1])*4))

	if passedLine== 1:
		reward += differenceReward
		print('Diff Rew =', differenceReward)
	'''
	if action != 0:
		reward -= 1
	'''
	
	if collision(ball, paddle):
		if velX < 0:
			reward += 60
			print('Hit Ball!')
	
	'''
	if winner == 1:

		reward += 80
	'''
	if winner == 2:
		reward -= 20
	
	'''
	if collision(ball, paddle):
		if velX > 0:
			velX = -velX
			reward += 60
			#print('Hit ball')
	'''
	return reward
	
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

def gameState(posX, posY, velX, velY, pY, paddle):

	touching = collision(ball, paddle)
	if touching:
		touching = 1
	else:
		touching = 0

	if posY > pY:
		relative = 0
	else: 
		relative = 1
	
	relative = 0
	
	normPosX = posX / resolution[0]
	normPosY = posY / resolution[1]

	normPY = pY / resolution[1]



	return (normPosX, normPosY, velX, velY, normPY, touching)

def runGame(gameID):
	
	clock = pygame.time.Clock()
	#print('GameID: ', gameID)
	reward = 0
	acceleration = 0.00
	global winner
	global randomDir
	global randomStart
	if winner == 1:
		
		randomStart = random.randint(20, 80)
		randomDir = random.randint(0,1)

		
	winner = 0
	gameOver = False

	initialVel = 4



	ballPosX, ballPosY = resolution[0] / 2, resolution[1] / 2
	if randomDir == 0:
		dirMult = 1
	else:
		dirMult = -1
	ballVelX = (randomStart / 100) * initialVel
	ballVelY = (((initialVel ** 2) - (((randomStart / 100) * initialVel)  ** 2))**0.5) * dirMult
	if enemy:
		paddle1Y = resolution[1] / 2
		paddle1 = pygame.Rect(0.075*resolution[0], paddle1Y - paddle1Height/2, 10, paddle1Height)
	paddle2Y = resolution[1] / 2
	
	paddle2 = pygame.Rect(0.925*resolution[0], paddle2Y - paddle2Height/2, 10, paddle2Height)
	reward = 0
	totalReward = 0
	passedLine = 0

	

	while gameOver != True:
		winner = 0

		# pygame.QUIT event means the user clicked X to close your window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True

		# fill the screen with a color to wipe away anything from last frame
		
		state = gameState(ballPosX, ballPosY, ballVelX, ballVelY, paddle2Y, paddle2)

		screen.fill("white")
		if render and gameID == 0:
			pygame.draw.circle(screen, "red", ball, ballRad)
			if enemy:
				pygame.draw.rect(screen, 'black', paddle1)
			pygame.draw.rect(screen, 'black', paddle2)


		if enemy:
			if collision(ball, paddle1):
				if ballVelX < 0:
					ballVelX = -ballVelX
		if collision(ball, paddle2):
			
			if ballVelX > 0:
				ballVelX = -ballVelX
			winner = 1
			gameOver = True
			
		if ballPosY < 0 or ballPosY > resolution[1]:
			ballVelY = -ballVelY

		if ballPosX < 0:
			winner = 1
			gameOver = True
			print('CoolAI wins')
		elif ballPosX > resolution[0]:
			gameOver = True
			winner = 2
			print('BoringAI wins')

		ballPosX += ballVelX
		ballPosY += ballVelY

		if ballPosX > 0.935*resolution[0]:
			if passedLine == 0:
				passedLine = 1
				
			else:
				passedLine = 2


		if enemy:
			paddle1Y = simpleAI(paddle1Y, ballPosY)


		if manualPlay:
			if event.type == pygame.KEYDOWN:
               
				# checking if key "A" was pressed
				if event.key == pygame.K_w:
					action = 2
				
				# checking if key "J" was pressed
				elif event.key == pygame.K_s:
					action = 1
			else:
				action = 0 
		else:

		
			action = predictModel(state, model)

		if action == 1:
			paddle2Y -= 3
		elif action == 2:
			paddle2Y += 3
		else:
			paddle2Y += 0
		reward = rewardFunc(ballPosX, ballPosY, winner, action, paddle2, ballVelX, paddle2Y, passedLine)

		if paddle2Y > resolution[1]:
			paddle2Y = resolution[1]
		elif paddle2Y < 0:
			paddle2Y = 0

		

		ball.xy = ballPosX, ballPosY
		if enemy:
			paddle1 = pygame.Rect(0.075*resolution[0], paddle1Y - paddle1Height/2, 10, paddle1Height)
		paddle2 = pygame.Rect(0.925*resolution[0], paddle2Y - paddle2Height/2, 10, paddle2Height)

		# flip() the display to put your work on screen
		if render and gameID == 0:
			pygame.display.flip()

		# limits FPS to 60
		# dt is delta time in seconds since last frame, used for framerate-
		# independent physics.
		dt = clock.tick(600) / 1000

		newState = gameState(ballPosX, ballPosY, ballVelX, ballVelY, paddle2Y, paddle2)

		ballVelX = ballVelX + acceleration * ballVelX
		ballVelY = ballVelY + acceleration * ballVelY
		acceleration *= accelerationDecay

		totalReward += reward
		replayBuffer.append((state, action, reward, newState, gameOver))
	return replayBuffer, winner, totalReward

global paddle1Y
global replayBuffer
global simpleDifficulty
global screen
global ballPosY
global ballVec
global render
global enemy 
global passedLine
global winner

pygame.init()

optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
# Define the epsilon-greedy policy


# Define the replay buffer

replayBuffer = deque(maxlen=100000)



model = defineModel((0, 0, 0, 0, 0, 0), 3)

if input('Do you want to load the previous model? ') == 'y':
	model.load_weights('model.h5')

resolution = (1280, 720)

accelerationDecay = 0.9995
ballRad = 13

# pygame setup


dt = 0

epsilon = 0.75
epsilonDecay = 0.999
discount = 0.95



paddle1Height = 90
paddle2Height = 120

screen = pygame.display.set_mode((1280, 720))

ball = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
winner = 1

render = True

game = 0

enemy = True

simpleDifficulty = 2

simGame = 0

manualPlay = False

while True:
	game += 1
	

	
	if simGame == 0:
		replayBuffer, winner, reward = runGame(0)
		DQN(400, replayBuffer)

		if enemy:
			if winner == 1:
				simpleDifficulty += 0.2
			else:
				if simpleDifficulty > 2:
					simpleDifficulty -= 0.1
			print('The simpleAI difficulty is now:', round(simpleDifficulty, 1))
			print('The AI scored ', round(reward))


	else:
		
		replayBuffers, outComes, rewards = run_multiple_games(simGame)
	
		for replayBuffer in (replayBuffers):
			
			DQN(200, replayBuffer)

		



	
	if epsilon > 0.5:
		epsilon *= epsilonDecay


	print('The randomness is now, ', round(epsilon*100), 'percent.')

