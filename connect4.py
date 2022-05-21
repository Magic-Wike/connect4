#imports
import random

# class definitions
class Game:
    def __init__(self, num_players=1):
        self.num_players = num_players
        self.players = []

class Board:
    # creates a board instance with a variable # of rows and colums (default: 6, 7)
    # board currently does not format correctly for nums larger than 7. Need to update formatting for 2 digit numbers
    def __init__(self, num_rows=6, num_cols=7):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.board = self.generate_board(self.num_rows, self.num_cols)

    # creates initial state of game board
    def generate_board(self, num_rows, num_cols):
        return [['|   |' for a in range(num_cols)] for b in range(num_rows)]
    
    # prints board throughout the game
    def print_board(self):
        col_nums = ['  {}  '.format(i) for i in range(1, self.num_cols+1)]
        print("".join(col_nums))
        for i in range(self.num_cols):
            print('-----', end="")
        print('\r')
        for r in self.board:
            print("".join(r))
        for i in range(self.num_cols):
            print('-----', end="")
        print('\r')
    
    def drop_token(self, col, player):
        # assigns X or O depending on if Player or CPU. this is purely for string formatting
        if isinstance(player, Player):
            token = 'X'
        if isinstance(player, CPU):
            token = 'O'
        # assuming col will take user input (column number 1 - total columns). subtract one for indexing
        tokenX = int(col)-1
        # check if column is valid input. return None if false
        if col > self.num_cols:
            print(f'\nOut of range! There are {self.num_cols} columns in the board.\n')
            return
        # iterating through column from bottom up
        print(f'\n{player.name} attempts to drop a {token} in column {col}...\r')
        for i in range(self.num_rows-1, -1, -1):
            row = self.board[i]
            cell = row[tokenX]
            # if cell is empty, move is valid and token is dropped, else continue loop
            # also adds +1 to player/CPU .moves
            if cell == '|   |':
                if isinstance(player, Player):
                    self.board[i][tokenX] = '| X |'
                    print(f'{token} dropped succesfully!\n')
                    player.moves += 1
                    break
                if isinstance(player, CPU):
                    self.board[i][tokenX] = '| O |'
                    print(f'{token} dropped succesfully!\n')
                    player.moves += 1
                    break
            # if at end of loop (i=0) the cell is occupied, column is full.
            # return None and end loop
            if i == 0 and cell in ['| X |', '| O |']:
                print('\nStack is full!\n')
                return
        # always prints board at the end unless invalid input 
        self.print_board()
        

class Player:
    def __init__(self, name='Player'):
        self.name = name
        self.moves = 0
        
    # if player instance does not already have name, asks for one 
    # otherwise, returns player name    
    def get_name(self):
        if self.name == None:
            while True:
                raw_name = input('\nWhat is your name, oh stranger?\n')
                self.name = raw_name
                break
        else:
            return self.name

class CPU:
    def __init__(self, name='CPU'):
        self.name = name
        self.moves = 0



board = Board()
board.print_board()
p1 = Player('Wike')
cpu = CPU()

# board.drop_token(8)
board.drop_token(7, p1)
board.drop_token(7, cpu)
board.drop_token(7, p1)
board.drop_token(7, cpu)
board.drop_token(7, p1)
board.drop_token(7, cpu)
board.drop_token(7, p1)
board.drop_token(7, cpu)
print(p1.moves)
print(cpu.moves)


