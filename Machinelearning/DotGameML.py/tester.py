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

    reshapedGame = np.reshape(game, (gameSize**2,))
    modelValues = model(np.expand_dims(reshapedGame, axis=0))
    action = np.argmax(modelValues)
    #print(action)
    return action






gameSize = 7

game = np.zeros((gameSize,gameSize), dtype=int)

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
                targetPos = (random.randint(0, gameSize - 1), random.randint(0, gameSize -1))
                if targetPos != playerPos:
                    break
        elif reward == -1 * maxReward / 2:
            errorCount += 1
        else:
            done = False


        playerPos = newPlayerPos


        


        if moves > 250:
            print('Gave up.')
            done = True

        moves += 1
        game = newGame
        print(game)
        
        

    print('Game completed in', moves, 'moves, and made ', errorCount, 'mistakes')





    