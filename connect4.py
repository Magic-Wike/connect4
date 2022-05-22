#imports
import random


# class definitions

# probably wont use this, unnecessary..the Board is the game...
class Game:
    def __init__(self, num_players=1):
        self.num_players = num_players
        self.players = []
        self.tokens = []

# ***MOST IMPORTANT COMMENT IN THE WHOLE THING**:
# game board is a 2 dimensional list and thus is referenced as board[Y][X]..this is counter intuitive since Y value comes first. 
# everything else *should* be coded to take an x,y value (token objects for example), but easy mistake to make. keep eye out for bugs
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

    # creates a Token object and drops it into the game board at specified column number (1-7). 
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
            tokenY = i
            cell = row[tokenX]
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

    def print_all_tokens(self):
        for num , t in self.tokens.items():
            print(f'Token {num}... X: {t.x}, Y: {t.y}')

    # work in progress...
    def check_win(self):
        # thinking count will work with while to recursively check adjacents until 4, in which case win
        # iterate through every Token object in self.tokens (list). adjacents list is all possible adjacent cells relative X and Y values
        for num, t in self.tokens.items():
            adjacents = [(t.x-1, t.y+1), (t.x-1, t.y), (t.x-1, t.y-1), (t.x, t.y+1), (t.x, t.y-1,), (t.x+1, t.y+1), (t.x+1, t.y), (t.x+1, t.y-1)]
            # current_x and y are for legibility..having trouble wrapping my head around this...
            current_x = t.x
            current_y = t.y
            print(f'\r**Current token position is: {current_x}, {current_y}')
            for a in adjacents:
                adj_x = a[0]
                adj_y = a[1]
                print(f'Checking: {adj_x}, {adj_y}')
                # first, check if adjacent cell is within board. if not, ignore
                if adj_x < 0 or adj_y < 0:
                    # print('out of range!')
                    continue
                if adj_x > self.num_cols-1 or adj_y > self.num_rows-1:
                    # print('out of range!')
                    continue
                else:
                    # passes boundary checks. check if symbol matches current token, if so continue to check adjacents until 4 in a row
                    # print('Valid  cell!')
                    adj_cell = self.board[adj_y][adj_x]
                    if adj_cell == t.symbol:
                        print('Ping!')
                        next_token = self.token_lookup(adj_x, adj_y)
                        if next_token.x == t.x-1 and next_token.y == t.y+1:
                            print('\ndown_left!\n')
                            count = 2
                            while count < 4:
                                print('entered loop...')
                                current_token = next_token
                                next_token = self.token_lookup(current_token.x-1,current_token.y+1)
                                try:
                                    print(f'Checking down_left... x:{next_token.x} y:{next_token.y}')
                                except:
                                    print('Nonetype')
                                if next_token is None:
                                    break
                                if next_token.symbol == current_token.symbol:
                                    print('Hit! +1')
                                    count += 1
                                    continue
                            if count == 4:
                                print('\nholy shit did it work?')
                                return 'Win!'
                            else:
                                continue
                        elif next_token.x == current_x-1 and next_token.y == current_y: 
                            direction = 'left'
                        elif next_token.x == current_x-1 and next_token.y == current_y+1:
                            direction = 'up_left'
                        elif next_token.x == current_x and next_token.y == current_y+1:
                            direction = 'up'
                        elif next_token.x == current_x+1 and next_token.y == current_y+1:
                            direction = 'up_right'
                        elif next_token.x == current_x+1 and next_token.y == current_y:
                            direction = 'right'
                        elif next_token.x == current_x+1 and next_token.y == current_y-1:
                            direction = 'down_right'
            
    # looks up a Token on board based on X,Y value. Returns said Token object
    # takes optional display parameter that if True will print the game board w/ lookup location as '| ! |'
    def token_lookup(self, x, y, display=False):
        for token in self.tokens.values():
            if token.x == x and token.y == y:
                if display:
                    # stores current value (X or O) so we can revert it after displaying it's location
                    current_value = self.board[y][x]
                    self.board[y][x] = '| ! |'
                    self.print_board()
                    self.board[y][x] = current_value
                return token

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

# testing function. fills entire board with Token for specified Player object
def fill_board(board, player=Player(), fill_random=False):
    for c in range(board.num_cols):
        for r in range(board.num_rows):
            rnd = random.choice([Player(), CPU()])
            if fill_random:
                board.drop_token(c+1, rnd)
            else:
                board.drop_token(c+1, player)


board = Board()
p1 = Player('Wike')
cpu = CPU()

# print(board.check_win())
# board.board[5][6] = '| ! |'
# board.print_board()

fill_board(board, fill_random=True)
# fill_board(board, p1)

# t1 = board.token_lookup(6, 5, True)
# t2 = board.token_lookup(3, 3, True)
# t3 = board.token_lookup(1, 4, True)
# print(t1.x,t1.y)
# board.print_board()


# board.print_all_tokens()

board.check_win()
