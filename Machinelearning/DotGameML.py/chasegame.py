import numpy as np
import tensorflow as tf
import random
import math
from collections import deque
import time



def defineModel(state, actionSize):

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(np.shape(state))),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(actionSize, activation=None)
    ])


    return model

def predictModel(state, model):
    # Choose the action using the epsilon-greedy policy
    if np.random.uniform(0, 1) < epsilon:
        action = np.random.randint(0, 3)
        #epsilon = epsilon * epsilonDecay
    else:
        
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

def DQN(batchSize, replayBuffer, model):


    
    
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

def agentMove(playerPos, action):
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
    return newPlayerPos

def outBounds(playerPos):
    return (newPlayerPos[0] < 0) or (newPlayerPos[0] > gameSize -1) or (newPlayerPos[1] < 0) or (newPlayerPos[1] > gameSize -1)

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
# Define the epsilon-greedy policy

epsilon = 0.05
#epsilonDecay = 0.95
discount = 0.7
# Define the replay buffer
global replayBuffer

replayBufferPlayer = deque(maxlen=100000)
replayBufferTarget = deque(maxlen=100000)




gameSize = 5

game = np.zeros((gameSize,gameSize), dtype=int)


state = np.zeros(3, dtype=float)
chaseState = np.zeros(3, dtype=float)

model = defineModel(state, 4)
model2 = defineModel(chaseState, 4)
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

playerPos = (gameSize // 2, gameSize // 2)
done = False
gameCounter = 0
while True:
    game = np.zeros((gameSize,gameSize), dtype=int)
    
    errorCount = 0



    
    game[targetPos] = (1)


    
    game[playerPos] = (2)
    moves = 0
    done = False
    while not done:
        done = False



        state = gameState(playerPos, targetPos)
        chaseState = gameState(targetPos, playerPos)
        actionPlayer = predictModel(state, model)
        actionTarget = predictModel(chaseState, model2)


        newPlayerPos = agentMove(playerPos, actionPlayer)

        newTargetPos = agentMove(targetPos, actionTarget)

        if outBounds(newPlayerPos):
            newPlayerPos = playerPos
            reward = -10
            print('Hit wall!')
            done = True
            playerPos = (gameSize // 2, gameSize // 2)
            
        else:
            game[playerPos] = 0
            game[newPlayerPos] = 2
            rewardPlayer = rewardFunc(newPlayerPos, playerPos, targetPos)
        
        if outBounds(newTargetPos):
            newTargetPos = targetPos
            targetReward = -20
            print('Target Hit wall!')
            done = True
            targetPos = (gameSize // 2, gameSize // 2)
            
        else:
            game[targetPos] = 0
            game[newTargetPos] = 1

            playerTargetDist = math.sqrt((newPlayerPos[0] - targetPos[0])**2 + (newPlayerPos[1] - targetPos[1])**2)

            newPlayerTargetDist = math.sqrt((newPlayerPos[0] - newTargetPos[0])**2 + (newPlayerPos[1] - newTargetPos[1])**2)
            if playerPos == targetPos:
                targetReward = -1 * maxReward
            elif newPlayerTargetDist > playerTargetDist:
                targetReward = maxReward / 2
            else:
                targetReward = -1 * maxReward / 4



        if rewardPlayer == maxReward:
            done = True
            print('GAME WON')
            while True:
                targetPos = (random.randint(0, gameSize - 1), random.randint(1, gameSize -1))

                if targetPos != playerPos:
                    break
        elif rewardPlayer == -1 * maxReward / 2:
            errorCount += 1
        else:
            done = False

        
        if moves > 500:
            targetReward = 40
            print('Gave up.')
            done = True

        
        newPlayerState = gameState(playerPos, targetPos)
        newTargetState = gameState(targetPos, newTargetPos)
        replayBufferPlayer.append((state, actionPlayer, rewardPlayer, newPlayerState, done))
        replayBufferTarget.append((chaseState, actionPlayer, targetReward, newPlayerState, done))

        playerPos = newPlayerPos
        targetPos = newTargetPos



            

        moves += 1
        if done == True:
            break
    #print(game)
        
    DQN(1, replayBufferPlayer, model)
    DQN(1, replayBufferTarget, model2)
    print('Game', gameCounter, 'completed in', moves, 'moves, and made ', errorCount, 'mistakes')
    gameCounter += 1

    





    



