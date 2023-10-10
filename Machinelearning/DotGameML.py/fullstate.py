import numpy as np
import tensorflow as tf
import random
import math
from collections import deque
import time

def defineModel(data, actionSize):

    shapedData = np.reshape(data, (gameSize**2,))
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(np.shape(shapedData))),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(actionSize, activation=None)
    ])


    return model

def predictModel(game, model):
    # Choose the action using the epsilon-greedy policy
    if np.random.uniform(0, 1) < epsilon:
        action = np.random.randint(0, 3)
    else:
        reshapedGame = np.reshape(game, (gameSize**2,))
        modelValues = model(np.expand_dims(reshapedGame, axis=0))
        action = np.argmax(modelValues)
    #print(action)
    return action

def rewardFunc(newPlayerPos, playerPos, targetPos):

    playerTargetDist = math.sqrt((playerPos[0] - targetPos[0])**2 + (playerPos[1] - targetPos[1])**2)

    newPlayerTargetDist = math.sqrt((newPlayerPos[0] - targetPos[0])**2 + (newPlayerPos[1] - targetPos[1])**2)
    if playerPos == targetPos:
        reward = maxReward
        print('this is CORRREECTTT')
    elif newPlayerTargetDist < playerTargetDist:
        reward = maxReward / 4
    else:
        reward = -1 * maxReward / 2
        
    #print(reward)


    



    return reward

def DQN(batchSize, replayBuffer):


    
    
    if len(replayBuffer) >= batchSize:
        model.save('model.h5')
        print('Updating Model...')
        
        batch = random.sample(replayBuffer, batchSize)
        # Compute the target Q-values for the batch
        targets = []
        states = []
        for state, action, reward, next_state, done in batch:
            
            if done:
                target = reward
            else:
                reshapedNextState = np.reshape(next_state, (gameSize**2,))
                nextModelValues = model(np.expand_dims(reshapedNextState, axis=0))
                maxModelValue = np.max(nextModelValues)
                target = reward + discount * maxModelValue
            
            
            shapedState = np.reshape(state, ((gameSize**2),))
            targetModelValues = (model(np.expand_dims(shapedState, axis=0)))
            targetModelValues = targetModelValues.numpy()

            targetModelValues[0][action] = target
            targets.append(targetModelValues)
            states.append(shapedState)

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
        model.save('model2.h5')

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
# Define the epsilon-greedy policy
epsilon = 0.05
discount = 0.7
# Define the replay buffer
global replayBuffer

replayBuffer = deque(maxlen=100000)



gameSize = 9

game = np.zeros((gameSize,gameSize), dtype=int)

model = defineModel(game, 4)
global targetPos
global playerPos
maxReward = 20

playerPos = (gameSize // 2, gameSize // 2)
global errorCount
errorCount = 0

while True:
    targetPos = (random.randint(1, gameSize - 2), random.randint(1, gameSize -2))
    if targetPos != playerPos:
        break


done = False
while True:
    
    game = np.zeros((gameSize,gameSize), dtype=int)
    errorCount = 0



    
    game[targetPos] = (1)


    playerPos = (gameSize // 2, gameSize // 2)
    game[playerPos] = (2)
    moves = 0
    done = False
    while not done:
        done = False

        newGame = game

        action = predictModel(game, model)

        playerTargetDist = math.sqrt((playerPos[0] - targetPos[0])**2 + (playerPos[1] - targetPos[1])**2)

        

        if action == 0:
            #go up
            newPlayerPos = (playerPos[0] - 1, playerPos[1])
            print('Up')
        elif action == 1:
            #go down
            newPlayerPos = (playerPos[0] + 1, playerPos[1])
            print('Down')
        elif action == 2:
            #go left
            newPlayerPos = (playerPos[0], playerPos[1] - 1)
            print('Left')
        else:
            #go right
            newPlayerPos = (playerPos[0], playerPos[1] + 1)
            print('Right')

        #this version wras around to the other side
        '''
        newGame[playerPos] = 0
        if newPlayerPos[0] < 0:
            newGame[playerPos] = 0
            newPlayerPos = (gameSize -1, newPlayerPos[0])
        if newPlayerPos[0] > gameSize -1:
            newGame[playerPos] = 0
            newPlayerPos = (0, newPlayerPos[0])
        if newPlayerPos[1] < 0:
            newGame[playerPos] = 0
            newPlayerPos = (newPlayerPos[0], gameSize -1)
        if newPlayerPos[1] > gameSize -1:
            newGame[playerPos] = 0
            newPlayerPos = (newPlayerPos[0], 0)
        
        newGame[newPlayerPos] = 2
        reward = rewardFunc(newPlayerPos, playerPos, targetPos)
        '''
        
        if (newPlayerPos[0] < 0) or (newPlayerPos[0] > gameSize -1) or (newPlayerPos[1] < 0) or (newPlayerPos[1] > gameSize -1):
            newPlayerPos = playerPos
            reward = -10
            print('Hit wall!')
            done = True
            
            
        else:
            newGame[playerPos] = 0
            newGame[newPlayerPos] = 2
            reward = rewardFunc(newPlayerPos, playerPos, targetPos)
        




        if reward == maxReward:
            done = True
            print('GAME WON')
            while True:
                targetPos = (random.randint(1, gameSize - 2), random.randint(1, gameSize -2))

                if targetPos != playerPos:
                    break
        elif reward == -1 * maxReward / 2:
            errorCount += 1
        else:
            done = False


        playerPos = newPlayerPos

        replayBuffer.append((game, action, reward, newGame, done))

        


        if moves > 350:
            print('Gave up.')
            done = True

        moves += 1
        game = newGame
        print(game)
        
        
        

    DQN(1, replayBuffer)
    print('Game completed in', moves, 'moves, and made ', errorCount, 'mistakes')
    time.sleep(1)
    





    



