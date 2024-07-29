import numpy as np
import pygame
import sys

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)


class GUI:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        # Set up the display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.screen.fill(BG_COLOR)

    def draw_lines(self):
        for row in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        for col in range(1, BOARD_COLS):
            pygame.draw.line(self.screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    def draw_figures(self, board):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == "x":
                    pygame.draw.line(self.screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                    pygame.draw.line(self.screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                elif board[row][col] == "o":
                    pygame.draw.circle(self.screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)

    def update_board(self, board_str):
        board = [list(row) for row in board_str.split("\n")]
        self.screen.fill(BG_COLOR)
        self.draw_lines()
        self.draw_figures(board)
        pygame.display.update()
