import sys
import pygame
from constants import *

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT))
pygame.display.set_caption('AI TIC-TAC-TOE')
screen.fill(BG_COLOR)


class Game:
    def __init__(self):
        self.show_lines()

    def show_lines(self):
        # VERTICAL LINES
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0), ( WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        # HORIZONTAL LINES
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)

def main():

    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

main()
