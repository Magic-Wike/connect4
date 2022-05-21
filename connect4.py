#imports
import random
from tabnanny import check

# class definitions

# probably wont use this, unnecessary..the Board is the game...
class Game:
    def __init__(self, num_players=1):
        self.num_players = num_players
        self.players = []
        self.tokens = []


class Board:
    # creates a board instance with a variable # of rows and colums (default: 6, 7)
    # board currently does not format correctly for nums larger than 7. Need to update formatting for 2 digit numbers
    def __init__(self, num_rows=6, num_cols=7):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.board = self.generate_board(self.num_rows, self.num_cols)
        self.is_full = self.check_full()
        self.tokens = {}

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

    # loops through every cell in board, if any are empty, 'empty_found' updates to True
    # if empty is found, function returns false -- if no empties found, check_full = True
    def check_full(self):
        empty_found = False
        for r in self.board:
            for i in r:
                if i == '|   |':
                    empty_found = True
        if empty_found:
            return False
        else:
            return True


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
            column = self.board[i]
            tokenY = i
            cell = column[tokenX]
            # if cell is empty (valid move), instance of Token class is created, and board is updated
            # also adds +1 to player/CPU .moves
            if cell == '|   |':
                token = Token(player, tokenX, tokenY)
                self.board[i][tokenX] = str(token.symbol)
                print(f'{token.symbol[2]} dropped succesfully!\n')
                # adds Token to board.tokens for win checking
                self.tokens[token.num] = token
                player.moves += 1
                break

            # if at end of loop (i=0) the cell is occupied, column is full.
            # return None and end loop
            if i == 0 and cell in ['| X |', '| O |']:
                print('\nStack is full!\n')
                return
        self.print_board()
        # at the end of every token drop, check if board is full
        if self.check_full():
            print('\nBoard is full! No more possible moves...\n')
            print('\nGAME OVER!!!\n')

    # work in progress...
    def check_win(self):
        # thinking count will work with while to recursively check adjacents until 4, in which case win
        count = 1
        # iterate through every Token object in self.tokens (list). adjacents list is all possible adjacent cells relative X and Y values
        for num, t in self.tokens.items():
            adjacents = [(t.x-1, t.y+1), (t.x-1, t.y), (t.x-1, t.y-1), (t.x, t.y+1), (t.x, t.y-1,), (t.x+1, t.y+1), (t.x+1, t.y), (t.x+1, t.y-1)]
            # current_x and y are for legibility..having trouble wrapping my head around this...
            current_x = t.x
            current_y = t.y
            print(f'Token # {num} position is: {current_x}, {current_y}')
            for a in adjacents:
                adj_x = a[0]
                adj_y = a[1]
                print(f'Checking: {adj_x}, {adj_y}')
                # first, check if adjacent cell is within board. if not, ignore
                if adj_x < 0 or adj_y < 0:
                    print('out of range!')
                    continue
                if adj_x > self.num_rows-1 or adj_y > self.num_cols-1:
                    print('out of range!')
                    continue
                else:
                    # passes boundary checks. check if symbol matches current token, if so continue to check adjacents until 4 in a row
                    print('Valid  cell!')
                    adj_cell = self.board[adj_x][adj_y]
                    if adj_cell == t.symbol:
                        print('Ping!')
                        # count starts at 1 (current token), should now be count of 2 heading into While loop
                        # count += 1
                        # while count != 4:
                        #     pass
        


                
# token class created to track token locations, all instances are added to board.tokens
class Token:
    num = 0
    def __init__(self, player, x, y):
        Token.num += 1
        self.num = Token.num
        self.x = x
        self.y = y
        self.player = player
        self.symbol = self.get_symbol()

    # determine self.symbol based on player or CPU dropping it
    def get_symbol(self):
        if isinstance(self.player, Player):
            return '| X |'
        if isinstance(self.player, CPU):
            return '| O |'



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


for c in range(board.num_cols):
    for r in range(board.num_rows):
        board.drop_token(c+1, cpu)

for num, t in board.tokens.items():
    print(f'Token {num}... X: {t.x}, Token Y: {t.y}')

print(board.check_win())
# board.board[5][6] = '| ! |'
# board.print_board()