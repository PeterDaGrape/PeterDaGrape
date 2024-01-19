import numpy as np
import random 

class Minesweeper:
    def __init__(self, shape, mine_count):
        self.shape = shape
        self.x_size = self.shape[0]
        self.y_size = self.shape[1]
        self.mine_count = mine_count

        

        self.place_mines()





    def place_mines(self):
        
        self.hidden_grid = np.zeros(self.shape)
        for mine in range(self.mine_count):



            while True:

                mine_position = (random.randint(0, self.x_size - 1), (random.randint(0, self.y_size - 1)))

                if self.hidden_grid[mine_position] == 0:
                    
                    self.hidden_grid[mine_position] = 1

                    break




game = Minesweeper((10, 10), 25)
print(game.hidden_grid)

