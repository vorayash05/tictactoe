# Importing Libraries
import sys
import pygame
import numpy as np
import random
import copy

from constants import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe AI")

# Classes
class Board:
    def __init__(self):
        self.squares = np.zeros((rows, cols))
        self.empty_squares = self.squares  # Initializing the whole board as empty
        self.marked_squares = 0

    def final_state(self, show=False):
        '''
        @return 0 if there is no win yet
        @return 1 if player 1 wins
        @return 2 if player 2 wins
        '''
        # vertical wins
        for col in range(cols):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = circle_color if self.squares[0][col] == 2 else cross_color
                    iPos = (col * square_size + square_size // 2, 20)
                    fPos = (col * square_size + square_size // 2, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.squares[0][col]

        # horizontal wins
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = circle_color if self.squares[row][0] == 2 else cross_color
                    iPos = (20, row * square_size + square_size // 2)
                    fPos = (width - 20, row * square_size + square_size // 2)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = circle_color if self.squares[1][1] == 2 else cross_color
                iPos = (20, 20)
                fPos = (width - 20, height - 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = circle_color if self.squares[1][1] == 2 else cross_color
                iPos = (20, height - 20)
                fPos = (width - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.squares[1][1]

        # no win yet
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squares(self):
        empty_squares = []
        for row in range(rows):
            for col in range(cols):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares

    def is_full(self):
        return self.marked_squares == 9

    def is_empty(self):
        return self.marked_squares == 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # Random
    def rnd(self, board):
        empty_squares = board.get_empty_squares()
        idx = random.randrange(0, len(empty_squares))
        return empty_squares[idx]  # row, col

    # Minimax
    def minimax(self, board, maximizing):
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None  # Eval, move
        # player 2 wins
        if case == 2:
            return -1, None
        # draw
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

    # Main evaluation
    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd_choice(main_board)
        else:
            # minimax algo
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')
        return move  # row, col

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # Player 1- X, Player 2- 0
        self.game_mode = 'ai'  # Player v player or AI
        self.running = True
        self.show_lines()

    # Draw methods
    def show_lines(self):
        # Background color
        screen.fill(bg_color)
        # Vertical lines
        pygame.draw.line(screen, line_color, (square_size, 0), (square_size, height), line_width)
        pygame.draw.line(screen, line_color, (width - square_size, 0), (width - square_size, height), line_width)

        # Horizontal lines
        pygame.draw.line(screen, line_color, (0, square_size), (width, square_size), line_width)
        pygame.draw.line(screen, line_color, (0, height - square_size), (width, height - square_size), line_width)

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = 3 - self.player

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            start_desc = (col * square_size + offset, row * square_size + offset)
            end_desc = (col * square_size + square_size - offset, row * square_size + square_size - offset)
            pygame.draw.line(screen, cross_color, start_desc, end_desc, cross_width)

            start_desc = (col * square_size + offset, row * square_size + square_size - offset)
            end_desc = (col * square_size + square_size - offset, row * square_size + offset)
            pygame.draw.line(screen, cross_color, start_desc, end_desc, cross_width)

        elif self.player == 2:
            # draw circle
            center = (col * square_size + square_size // 2, row * square_size + square_size // 2)
            pygame.draw.circle(screen, circle_color, center, radius, circle_width)

    # Other methods
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.game_mode = 'ai' if self.game_mode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

    def reset(self):
        self.__init__()

def main():
    # Objects
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // square_size
                col = pos[0] // square_size

                # human mark square
                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        # AI initial call
        if game.game_mode == 'ai' and game.player == ai.player and game.running:
            # update the screen
            pygame.display.update()

            # eval
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()

main()
