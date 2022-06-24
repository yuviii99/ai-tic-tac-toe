import copy
import random
import sys
import pygame
from constants import *
import numpy as np

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT))
pygame.display.set_caption('AI TIC-TAC-TOE')
screen.fill(BG_COLOR)


class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLUMNS) )
        self.empty_squares = self.squares
        self.marked_squares = 0
    
    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet!
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # CHECK FOR VERTICAL WIN
        for col in range(COLUMNS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    start_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    final_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, start_pos, final_pos, LINE_WIDTH)
                return self.squares[0][col]
        
        # CHECK FOR HORIZONTAL WIN
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    start_pos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2, )
                    final_pos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, start_pos, final_pos, LINE_WIDTH)
                return self.squares[row][0]
        
        # CHECK FOR DIAGONAL WIN
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                start_pos = (20, 20)
                final_pos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, start_pos, final_pos, LINE_WIDTH)
            return self.squares[1][1]
        
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                start_pos = (20, HEIGHT - 20)
                final_pos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, start_pos, final_pos, LINE_WIDTH)
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


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
    
    def random_choice(self, board):
        empty_squares = board.get_empty_squares()
        random_idx = random.randrange(0, len(empty_squares))
        return empty_squares[random_idx]
        
    def minimax(self, board, maximizing):

        # CHECK FOR TERMINAL CASES
        case = board.final_state()
        if case == 1:
            return 1, None
        if case == 2:
            return -1, None
        elif board.is_full():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            
            return min_eval, best_move
    
    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.random_choice(main_board)
        else:
            # minmax algo
            eval, move = self.minimax(main_board, False)
        
        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')

        return move


class Game:

    def __init__(self):
        self.ai = AI()
        # Console Board
        self.board = Board()
        # Graphical Board
        self.show_lines()
        self.player = 1
        self.gamemode = 'ai' # pvp or ai
        self.running = True
    
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_player()
    
    def change_gamemode(self):
        if self.gamemode == 'pvp':
            self.gamemode = 'ai'
        else:
            self.gamemode = 'pvp'

    
    def show_lines(self):
        screen.fill( BG_COLOR )
        # VERTICAL LINES
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0), ( WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # HORIZONTAL LINES
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)
    
    def next_player(self):
        self.player = self.player % 2 + 1

    def draw_fig(self, row, col):
        if self.player == 1:
            start_desc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)


        elif self.player == 2:
            center = (col * SQUARE_SIZE + SQUARE_SIZE //2, row * SQUARE_SIZE + SQUARE_SIZE //2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def reset(self):
        self.__init__()
    
    def is_over(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()


def main():

    game = Game()
    board = game.board
    ai = game.ai

    # MAINLOOP
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.is_over():
                        game.running = False
            
            if event.type == pygame.KEYDOWN:
                # G - Game Mode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # 0 - Level 0 -> Random AI
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1 - Level 1 -> Minmax AI
                if event.key == pygame.K_1:
                    ai.level = 1
                
                # r - Reset Game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
            
        
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.is_over():
                game.running = False
            
        
        pygame.display.update()

main()
