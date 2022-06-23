import numpy as np
from constants import *

class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLUMNS) )
        self.empty_squares = self.squares
        self.marked_squares = 0
    
    def final_state(self):
        '''
            @return 0 if there is no win yet!
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # CHECK FOR VERTICAL WIN
        for col in range(COLUMNS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        
        # CHECK FOR HORIZONTAL WIN
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        
        # CHECK FOR DIAGONAL WIN
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            return self.squares[1][1]
        
        # NO WIN YET
        return 0
    
    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        if self.squares[row][col] == 0:
            return True
        return False

    def is_full(self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares
    
