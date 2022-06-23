import copy
import random
import sys
import pygame
from constants import *
from board import Board

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT))
pygame.display.set_caption('AI TIC-TAC-TOE')
screen.fill(BG_COLOR)


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
    
    def show_lines(self):
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

                if board.empty_square(row, col):
                    board.mark_square(row, col, game.player)

                    game.draw_fig(row, col)

                    game.next_player()
            
        if game.gamemode == 'ai' and game.player == ai.player:
            pygame.display.update()

            row, col = ai.eval(board)

            board.mark_square(row, col, game.player)
            game.draw_fig(row, col)
            game.next_player()

        
        pygame.display.update()

main()
