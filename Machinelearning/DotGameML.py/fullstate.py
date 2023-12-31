import numpy as np
import random
import math
import time


learning_rate=0.001
# Define the epsilon-greedy policy
epsilon = 0.05
discount = 0.7
# Define the replay buffer



gameSize = 9

game = np.zeros((gameSize,gameSize), dtype=int)

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
        elif action == 1:
            #go down
            newPlayerPos = (playerPos[0] + 1, playerPos[1])
        elif action == 2:
            #go left
            newPlayerPos = (playerPos[0], playerPos[1] - 1)
        else:
            #go right
            newPlayerPos = (playerPos[0], playerPos[1] + 1)

        #this version wras around to the other side

        
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
    





    



