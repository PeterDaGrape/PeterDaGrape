import numpy as np
import tensorflow as tf
import random
import math
from collections import deque

def defineModel(data, actionSize):

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(np.shape(data))),
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
#epsilonDecay = 0.95
discount = 0.7
# Define the replay buffer
global replayBuffer

replayBuffer = deque(maxlen=100000)


model = defineModel(state, 4)