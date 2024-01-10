

class Game:
    def __init__(self):
        self.state = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.game_over = False
        self.move_count = 0



    def update_game(self, x, y, player):
        if self.state[y][x] not in [1, 2]:
            self.state[y][x] = player

            self.move_count += 1

            return True
        return False

    def player_move(self, player):
        success = False
        print(f'Enter coordinates for player {player}')
        while not success:
            x, y = int(input('Enter an X coordinate: ')), int(input('Enter a Y coordinate: '))

            if (x < 0 or x > 2 or y < 0 or y > 2):
                continue
            if self.update_game(x, y, player):
                success = True
            else:
                print('Choose somewhere else...')

    def check_winner(self):

        if self.move_count == 9:
            self.game_over = True
            return -1

        #check rows
        for x in range(3):
            check = []
            for y in range(3):
                check.append(self.state[x][y])
            if check == [1, 1, 1]:
                self.game_over = True
                return 1
            if check == [2, 2, 2]:
                self.game_over = True
                return 2
        for y in range(3):
            check = []
            for x in range(3):
                check.append(self.state[x][y])
            if check == [1, 1, 1]:
                self.game_over = True
                return 1
            if check == [2, 2, 2]:
                self.game_over = True
                return 2        
        #check columns 
            
        #check diagonals

        check = [[],[]]

        for i in range(3):
            check[0].append(self.state[i][i])
            check[1].append(self.state[2 - i][i])

        if [1, 1, 1] in check:
            self.game_over = True
            return 1
        if [2, 2, 2] in check:
            self.game_over = True
            return 2

        return 0
            
    def display_game(self):
        for layer in self.state:
            print(layer)

        print('')

if __name__ == '__main__':

    game = Game()
                    





    move_count = 0
    while not game.game_over:

        
        #game.player_move((move_count % 2) + 1)
        game.update_game(0, 0, 0)
        game.display_game()

        winner = game.check_winner()

        if game.game_over:
            print(f'Game is over, player {winner} has won')


        move_count += 1



