#imports
import random
import c4utils
from time import sleep

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
        # generate a list of column numbers and print at top of list
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

    # celebrate good times, come on
    def celebrate(self):
        original_board = [i for i in self.board]
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                c4utils.clearFunc()
                self.board[y][x] = '| ! |'
                self.print_board()
                sleep(.3)
        self.board = [i for i in original_board]


    # loops through every cell in board, if any are empty, 'empty_found' updates to True
    # if empty is found, function returns false -- if no empties found, check_full = True
    # optionally, takes a column numbers (1-7) as argument. if present, checks onlt that column
    def check_full(self, column_number=None):
        empty_found = False
        if column_number is not None:
            for i in range(self.num_rows):
                if self.board[i][column_number-1] == "|   |":
                    empty_found = True
        for r in self.board:
            for i in r:
                if i == '|   |':
                    empty_found = True
        if empty_found:
            return False
        else:
            return True

    # creates a Token object and drops it into the game board at specified column number (1-7). 
    # returns None if out of range or other error, else returns True.
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
        print(f'\n\n\n{player.name} attempts to drop a {token} in column {col}...\r'), sleep(1)
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
                print('\nStack is full!\n'), sleep(1)
                return 
        self.print_board()
        # at the end of every token drop, check if board is full
        if self.check_full():
            print('\nBoard is full! No more possible moves...\n'), sleep(1)
            print('\nGAME OVER!!!\n')
            return 'Full'
        return token
        
    def print_all_tokens(self):
        for num , t in self.tokens.items():
            print(f'Token {num}... X: {t.x}, Y: {t.y}')

    # check_Win will loop through every adjacent cell to the newly dropped Token, if a hit is found, connect() is triggered
    # will iterate in both direction *and opposite* direction of adjacent matching cell, looking for more matching cells
    def check_win(self, t):
        # connect() is step 2 of function, called when we find any adjacent cell with matching value
        # will then iterate in both directions, looking for more matching tokens
        def connect(direction, current_token):
            # dictionary of directions with their opposites for easy lookup
            inverses = {'down_left': 'up_right', 'left': 'right', 'up_left': 'down_right', 'up': 'down', 'up_right': 'down_left', 'right': 'left', 'down_right': 'up_left', 'down': 'up'}
            # reset count to 1 every time function is called
            count = 1
            # get difference in X, Y coords from directions dict
            x_change1, y_change1 = directions[direction]
            # get opposite direction from inverses dictionary, and get difference in X, Y coords from directions
            inverse = inverses[direction]
            x_change2, y_change2 = directions[inverse]
            # define symbol to look for, and the next 2 tokens to search
            symbol = current_token.symbol
            next_token1 = self.token_lookup(current_token.x+x_change1,current_token.y+y_change1)
            next_token2 = self.token_lookup(current_token.x+x_change2,current_token.y+y_change2)
            # loop will only execute while next tokens exist (ignores out of bounds, etc)
            while next_token1 or next_token2:
                if next_token1 is not None:  
                    print(f'Checking {direction} (x:{next_token1.x} y:{next_token1.y})')
                    # check first token for matchimg symbol, if found +1 to count, next token1 is advanced to the next token in the same direction
                    # if symbol does not match or out of bounds, return None
                    if next_token1.symbol == symbol:
                        count += 1
                        print('Hit! +1, Count: ',count)
                        if count >= 4:
                            return 'Win!'
                        else: 
                            next_token1 = self.token_lookup(next_token1.x+x_change1,next_token1.y+y_change1)
                    else:
                        next_token1 = None
                # same process is repeated for next_token2 in opposite direction
                # if at any point count == 4, returns 'Win!', else returns None
                if next_token2 is not None:  
                    print(f'Checking {inverse} (x:{next_token2.x} y:{next_token2.y}')
                    if next_token2.symbol == symbol:
                        count += 1
                        print('Hit! +1, Count: ',count)
                        if count >= 4:
                            return 'Win!'
                        next_token2 = self.token_lookup(next_token2.x+x_change2, next_token2.y+y_change2)
                    else:
                        next_token2 = None
                if count == 4:
                    return 'Win!'
                else:
                    continue

        # Step 1 of the function. check_win() takes a Token object as an argument, and checks every adjacent cell for matching symbol
        # if found, executes connect() inner function to continue the search
        while True:
            # creates list of every adjacent cell's X, Y values using the position of the passed Token 
            adjacents = [(t.x-1, t.y+1), (t.x-1, t.y), (t.x-1, t.y-1), (t.x, t.y+1), (t.x, t.y-1,), (t.x+1, t.y+1), (t.x+1, t.y), (t.x+1, t.y-1)]
            current_x = t.x
            current_y = t.y
            print(f'\r**Current token position is: {current_x}, {current_y}')
            # loop through every adjacent cell 
            for a in adjacents:
                adj_x = a[0]
                adj_y = a[1]
                print(f'Checking: {adj_x}, {adj_y}')
                # first, check if adjacent cell is within board. if not, ignore
                if adj_x < 0 or adj_y < 0:
                    print('out of range!')
                    continue
                if adj_x > self.num_cols-1 or adj_y > self.num_rows-1:
                    print('out of range!')
                    continue
                else:
                    # passes boundary checks. check if symbol matches current token, if so continue to check adjacents until 4 in a row
                    directions = {'down_left': (-1,+1), 'left': (-1,0), 'up_left': (-1,-1), 'up': (0,-1), 'up_right': (+1,-1), 'right': (+1,0), 'down_right': (+1,+1), 'down': (0,+1)}
                    print('Valid  cell!')
                    # store adjacent cells value and check for matching symbol
                    adj_cell = self.board[adj_y][adj_x]
                    if adj_cell == t.symbol:
                        print('Ping!')
                        # use Token lookup function to return Token object of the current adjacent cell w/ matching val
                        next_token = self.token_lookup(adj_x, adj_y)
                        # determine direction of adjacent matching token by X,Y value with directions dict
                        if next_token.x == t.x-1 and next_token.y == t.y+1:
                            direction = 'down_left'
                        if next_token.x == t.x-1 and next_token.y == t.y: 
                            direction = 'left'
                        if next_token.x == t.x-1 and next_token.y == t.y-1:
                            direction = 'up_left'
                        if next_token.x == t.x and next_token.y == t.y-1:
                            direction = 'up'
                        if next_token.x == t.x+1 and next_token.y == t.y-1:
                            direction = 'up_right'
                        if next_token.x == t.x+1 and next_token.y == t.y:
                            direction = 'right'
                        if next_token.x == t.x+1 and next_token.y == t.y+1:
                            direction = 'down_right'
                        if next_token.x == t.x and next_token.y == t.y+1:
                            direction = 'down'
                        # call connect function w/ direction argument..will iterate in that direction until
                        # COUNT reaches 4, in which case, the game is over and Player wins
                        if direction:
                            result = connect(direction, t)
                            print('connect() result: ',result)
                        # will return True if there is a winner, False/continue loop if not
                            if result == 'Win!':
                                return True
            return False

        
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
        if self.name == 'Player':
            while True:
                c4utils.clearFunc()
                raw_name = input('\nWhat is your name, oh stranger?\n\n$')
                self.name = raw_name
                print(f'\nWelcome {self.name}!\n')
                break
        else:
            return self.name

class CPU:
    def __init__(self, name='CPU'):
        self.name = name
        self.moves = 0

# testing function. fills entire board with Token for specified Player object
# optionally, will fill board with random tokens
def fill_board(board, player=Player(), fill_random=False):
    for c in range(board.num_cols):
        for r in range(board.num_rows):
            rnd = random.choice([Player(), CPU()])
            rnd_col = random.randint(0, board.num_cols-1)
            if fill_random:
                board.drop_token(rnd_col, rnd)
            else:
                board.drop_token(c+1, player)

def play_game():
    # inner function definitions...

    # primary gameplay loop. gets column number (1-7) from user, attempts to drop a token in that position
    def player_move():
        while True:
            board.print_board()
            ask_col = input(f'\nWhich column will you play? (Enter a number between 1 - {board.num_cols}\n\n$')
            if ask_col == 'celebrate':
                board.celebrate()
                continue
            else:
                try:
                    col_selection = int(ask_col)
                except ValueError:
                    print('\nInvalid input! Enter numbers only.\n')
                    continue
            c4utils.clearFunc()
            player_token = board.drop_token(col_selection, p1)
            sleep(1)
            if player_token == 'Full':
                return 'Full'
            if player_token is False or player_token is None:
                continue
            # check_win() will return None or 'Win!'. If win, player_move() returns True, else Falsy
            game_over = board.check_win(player_token)
            if game_over:
                return True
            return
    # same process for the CPU, minus the user input. CPU currently very stupid and only uses random column selection
    def cpu_move():
        print("\nIt's the robot's turn...\n"), sleep(1)
        c4utils.clearFunc()
        while True:
            while True:
                random_col = random.randint(1, board.num_cols)
                if board.check_full(random_col):
                    continue
                else:
                    break
            # cpu logic needed, random for now 
            cpu_token = board.drop_token(random_col, cpu)
            if cpu_token == 'Full':
                return 'Full'
            if cpu_token is False or cpu_token is None:
                continue
            sleep(1)
            game_over = board.check_win(cpu_token)
            if game_over:
                return True
            return

    # welcome message and game start
    c4utils.clearFunc()
    print(c4utils.welcome)
    sleep(5)
    # ready to play? loop
    while True:
        ask_ready = input("\nReady to play?\n\n$")
        ask_ready.strip()
        if ask_ready == 'celebrate':
            Board().celebrate()
        if ask_ready in c4utils.y_responses:
            print('\nSetting up the game!...\n')
            p1 = Player()
            p1.get_name()
            break
        if ask_ready in c4utils.n_responses:
            c4utils.killswitch()
        else:
            print('\nInvalid input!\n')    
            continue
    # initializing the game objects
    print('\nSetting up the board...\n'), sleep(1)
    board = Board()
    print('\nWaking up the robot...\n'), sleep(1)
    cpu = CPU()
    # randomly decide whether player or cpu goes first
    print('\nFlipping the coin...\n'), sleep(1)
    go_first = random.choice([p1, cpu])
    # top level loops housing the primary function calls. onlt difference between the two is whether player or cpu goes first
    # must be a more pythonic way to write this, will come back
    if go_first == p1:
        print(f'\n{p1.name} will go first!\n'), sleep(1)
        print('\nReady to play!\n')
        while True:
            player_win = player_move()
            if player_win == 'Full':
                break
            if player_win:
                print('\n\n***WINNER CHICKEN DINNER!!!***\n\n')
                break
            cpu_win = cpu_move()
            if cpu_win == 'Full':
                break
            if cpu_win:
                print('\n\n***CPU WINS!!!***\n\n')
                break
    if go_first == cpu:
        print('\nThe robot will go first!\n'), sleep(1)
        print('\nReady to play!\n')
        while True:
            cpu_win = cpu_move()
            if cpu_win == 'Full':
                break
            if cpu_win:
                print('\n\n***CPU WINS!!!***\n\n')
                break
            player_win = player_move()
            if player_win == 'Full':
                break
            if player_win:
                print('\n\n***WINNER CHICKEN DINNER!!!***\n\n')
                break
    # game is over! print the board one last time and...        
    board.print_board()
    input('\nPress any key to celebrate!\n')
    # celebrate!!
    board.celebrate()
    # play again? loop
    while True:            
        play_again = input('\nWould you like to play again?\n\n$')
        if play_again in c4utils.y_responses:
            play_game()
        elif play_again in c4utils.n_responses:
            c4utils.killswitch()
        else:
            print('\nInvalid input!\n')
            continue

# ***testing blocks...leaving for now, will clean up later. 

# print(board.check_win())
# board.board[5][6] = '| ! |'
# board.print_board()

# fill_board(board, fill_random=True)
# fill_board(board, p1)

# t1 = board.token_lookup(6, 5, True)
# t2 = board.token_lookup(3, 3, True)
# t3 = board.token_lookup(1, 4, True)
# print(t1.x,t1.y)
# board.print_board()


# board.print_all_tokens()

# board.check_win()

# board.drop_token(7, p1)
# board.drop_token(7, p1)
# board.drop_token(7, p1)
# board.drop_token(7, p1)
# board.check_win()

# Board().celebrate()


# ***EXECUTE THE GAME!!!****

play_game()

