import pygame
import numpy
import time
import random

def mine_map(num_mines):
    global hidden_grid
    hidden_grid = numpy.full(resolution, False)

    
    for i in range(num_mines):
        while True:
            position = [random.randint(0, resolution[0]-1), random.randint(0, resolution[1]-1)]
            if hidden_grid[position[0]][position[1]]:
                continue
            else:
                hidden_grid[position[0]][position[1]] = True

                break

def calc_grid():
    global visible_grid
    visible_grid = numpy.zeros(shape=resolution, dtype=int)

    for x in range(resolution[0]):
        for y in range(resolution[1]):
            if hidden_grid[x][y]:
                visible_grid[x][y] = 10
            
            else:
                total_around = 0

                
                for local_x in range(-1, 2):
                    for local_y in range(-1, 2):
                        test_coordinate_x = x + local_x
                        test_coordinate_y = y + local_y
                        print(test_coordinate_x, test_coordinate_y)
                        

                        if not (test_coordinate_x > resolution[0] - 1 or test_coordinate_x < 0 or test_coordinate_y > resolution[1] - 1 or test_coordinate_y < 0):

                            if hidden_grid[test_coordinate_x][test_coordinate_y]:
                                total_around += 1
                        



                print(total_around, 'found')
                visible_grid[x][y] = total_around
                    
def visible_map():
    global covered_map
    covered_map = numpy.full(fill_value= 10, shape=resolution, dtype=int)
    
def game_loop():
    while True:
        print(covered_map)
        print('Please type in coordinates: ')
        x_cor = int(input('What is the X coordinate? '))
        y_cor = int(input('What is the Y coordinate? '))
        selected = x_cor, y_cor
        action = input('What action do you want to take? (u/uncover, f/flag)')
        if action == 'u':
            if hidden_grid[selected]:
                print('Game Over')
                break

            else:
                covered_map[selected] = visible_grid[selected]
        elif action == 'r':
            print(visible_grid)
        
def main():
    global resolution
    resolution = (10, 10)
    mine_map(num_mines=10)

    calc_grid()

    visible_map()

    game_loop()


if __name__ == '__main__':
    main()
