#Importing Libraries

import sys
import pygame
from constants import *
import numpy as np

# Pygame setup

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(bg_color)

class Board:
	def __init__(self):
		self.squares = np.zeros((rows, cols))
		print(self.squares)

	def mark_square(self, row, col, player):
		self.squares[row][col] = player

	def empty_square(self, row, col):
		return self.squares[row][col] == 0



class Game():
	def __init__(self):
		self.board = Board()
		self.show_lines()
		self.player = 1

	def show_lines(self):
		#vertical lines
		pygame.draw.line(screen, line_color, (square_size, 0), (square_size, height), line_width)
		pygame.draw.line(screen, line_color, (width - square_size, 0), (width - square_size, height), line_width)

		#horizontal lines
		pygame.draw.line(screen, line_color, (0, square_size), (width, square_size), line_width)
		pygame.draw.line(screen, line_color, (0, height - square_size), (width, height - square_size), line_width)

	def next_turn(self):
		self.player = 3 - self.player




def main():
	game = Game()
	board = game.board

	while True:

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				row = pos[1]//square_size
				col = pos[0]//square_size
				
				if board.empty_square(row, col):
					board.mark_square(row, col, game.player)
					game.next_turn()
					print(board.squares)
				


		pygame.display.update()

main()