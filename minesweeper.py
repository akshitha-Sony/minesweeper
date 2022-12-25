import random
import re


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()  # plant bombs
        self.assign_values_to_board()
        # keep a track of uncovered locations
        # save tuples of (row,col) in a set
        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size
            if board[row][col] == '*':  # if bomb is already planted
                continue
            board[row][col] = '*'
            bombs_planted += 1
        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':  # we don't want to calculate anything if it's already a bomb
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)

    def get_num_neighbouring_bombs(self, row, col):
        # iterate through each of the neighbouring positions
        num_neighbouring_bombs = 0
        for r in range(max(0, row - 1), min(row + 2, self.dim_size)):
            for c in range(max(0, col - 1), min(col + 2, self.dim_size)):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs

    def dig(self, row, col):
        # return true if dug successfully,
        # False if bomb
        # few scenarios
        # 1. hit a bomb -> game over
        # 2. loc with neighbouring bombs -> finish dig
        # 3. loc with no neighbouring bombs -> dig recursively
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        # self.board[row][col] == 0
        for r in range(max(0, row - 1), min(row + 2, self.dim_size)):
            for c in range(max(0, col - 1), min(col + 2, self.dim_size)):
                if (r, c) in self.dug:
                    continue  # don't dig where you've already dug
                self.dig(r, c)
        return True

    def __str__(self):
        # this is a magic function where if you call print on this object
        # it'll print out what the function returns
        # return a string that shows the board to the player
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


# play the game
def play(dim_size=10, num_bombs=10):
    # step 1: create the board and plant the bombs
    # step 2: show the user the board and ask where they want to dig
    # step 3a: if the location is a bomb, show the game over message
    # step 3b: if the location is not a bomb, dig recursively until each square is atleast next to a bomb
    # step 4: repeat steps 2 and 3a/b until there are no places to dig..VICTORY!!
    board = Board(dim_size, num_bombs)
    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        # 0,0 or 0,  0 or 0,    0
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row, col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue
        # if it's valid we dig
        safe = board.dig(row, col)
        if not safe:  # we dig a bomb uh-oh
            break  # game over rip

    if safe:
        print("Congratulations!! You won...")
    else:
        print("Sorry!! Game over. Better luck next time.")
        # let's reveal the whole board
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__': # good practice :)
    play()
