import numpy as np
import tensorflow as tf
import random
import math
from collections import deque
import time



def predictModel(state, model):

        
    modelValues = model(np.expand_dims(state, axis=0))
    action = np.argmax(modelValues)
    #print(action)
    return action

def rewardFunc(newPlayerPos, playerPos, targetPos):

    playerTargetDist = math.sqrt((playerPos[0] - targetPos[0])**2 + (playerPos[1] - targetPos[1])**2)

    newPlayerTargetDist = math.sqrt((newPlayerPos[0] - targetPos[0])**2 + (newPlayerPos[1] - targetPos[1])**2)
    if playerPos == targetPos:
        reward = maxReward
    elif newPlayerTargetDist < playerTargetDist:
        reward = maxReward / 4
    else:
        reward = -1 * maxReward / 2
        
    #print(reward)


    



    return reward



    
    
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
            
            
            targetModelValues = (model(np.expand_dims(state, axis=0)))
            targetModelValues = targetModelValues.numpy()

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
epsilon = 0.05
discount = 0.7
# Define the replay buffer
global replayBuffer

replayBuffer = deque(maxlen=100000)

gameSize = 9

game = np.zeros((gameSize,gameSize), dtype=int)

state = np.zeros(3, dtype=float)
model = tf.keras.models.load_model('model.h5')
global targetPos
global playerPos
maxReward = 20

playerPos = (gameSize // 2, gameSize // 2)
global errorCount
errorCount = 0

while True:
    targetPos = (random.randint(0, gameSize - 1), random.randint(0, gameSize -1))
    if targetPos != playerPos:
        break

playerPos = (gameSize // 2, gameSize // 2)
done = False
gameCount = 1
while True:
    
    game = np.zeros((gameSize,gameSize), dtype=int)
    
    errorCount = 0

    game[targetPos] = (1)
    
    game[playerPos] = (2)
    print(game)
    input('')
    moves = 0
    done = False
    while not done:
        done = False

        state = gameState(playerPos, targetPos)

        action = predictModel(state, model)

        if action == 0:
            #go up
            newPlayerPos = (playerPos[0] - 1, playerPos[1])
            #print('Up')
        elif action == 1:
            #go down
            newPlayerPos = (playerPos[0] + 1, playerPos[1])
            #print('Down')
        elif action == 2:
            #go left
            newPlayerPos = (playerPos[0], playerPos[1] - 1)
            #print('Left')
        else:
            #go right
            newPlayerPos = (playerPos[0], playerPos[1] + 1)
            #print('Right')

        #this version wras around to the other side

        if (newPlayerPos[0] < 0) or (newPlayerPos[0] > gameSize -1) or (newPlayerPos[1] < 0) or (newPlayerPos[1] > gameSize -1):
            newPlayerPos = playerPos
            reward = -10
            endState = 1
            done = True
            playerPos = (gameSize // 2, gameSize // 2)
        else:
            game[playerPos] = 0
            game[newPlayerPos] = 2
            reward = rewardFunc(newPlayerPos, playerPos, targetPos)
        if reward == maxReward:
            done = True
            endState = 0
            while True:
                targetPos = (random.randint(1, gameSize - 2), random.randint(1, gameSize -2))
                game[targetPos] = 1
                if targetPos != playerPos:
                    break

        elif reward == -1 * maxReward / 2:
            errorCount += 1
        else:
            done = False

        playerPos = newPlayerPos
        newState = gameState(playerPos, targetPos)

        if moves > 500:
            endState = 2
            done = True

        moves += 1

        if done == True:
            break
        print(game)
        input('')
     
    if endState == 0:
        print('Game Won!')
    elif endState == 1:
        print('Hit Wall.')
        
    elif endState == 2:
        print('Gave Up.')
        
    print('Game', gameCount, 'completed in', moves, 'moves, and made ', errorCount, 'mistakes')
    gameCount += 1
