import numpy as np
import random

gridsize = (100, 100)

grid = np.zeros(shape=gridsize,dtype=int)



def randomize_grid():
    for y in range(len(grid[0])):
        for x in range(len(grid[1])):
            grid[x+1][y+1] = random.randint(0, 1)


def calculate_grid():
    for y in range(len(grid[0])):
        for x in range(len(grid[1])):
            print(x, y)
            print(grid[x][y])


            num_neighbours = find_neighbours(x, y)
            print(num_neighbours)
            input()
            

def find_neighbours(x, y):
    num = 0
    print(grid[x-1][y-1])
    if grid[x-1][y-1] == 1:
        num += 1
    if grid[x][y-1] == 1:
        num += 1
    if grid[x+1][y-1] == 1:
        num += 1
    if grid[x-1][y] == 1:
        num += 1
    if grid[x+1][y] == 1:
        num += 1
    if grid[x-1][y+1] == 1:
        num += 1
    if grid[x][y+1] == 1:
        num += 1
    if grid[x+1][y+1] == 1:
        num += 1
    
    return num





randomize_grid()
calculate_grid()