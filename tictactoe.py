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
		self.empty_squares = self.squares  #Initialising the whole board as empty
		self.marked_squares = 0


	def final_state(self):
		'''
		return 0 if there is no win yet
		return 1 if player 1 wins
		return 2 if player 2 wins	
		'''
		
		#vertical wins
		for col in range(cols):
			if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] !=0:
					return self.squares[0][col]

		#horizontal wins
		for row in range(rows):
			if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] !=0:
					return self.squares[row][0]

		#diagonal wins
		if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] !=0:
			return self.squares[0][0]

		if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] !=0:
			return self.squares[0][2]

		return 0 #no win yet





	
	def mark_square(self, row, col, player):
		self.squares[row][col] = player
		self.marked_squares +=1

	def empty_square(self, row, col):
		return self.squares[row][col] == 0

	def is_full(self):
		return self.marked_squares == 9

	def is_empty(self):
		return self.marked_squares == 0

	def get_empty(self):
		empty_squares = []
		for row in range(rows):
			for col in range(cols):
				if self.empty_square(row, col):
					empty_squares.append((row, col))
		return empty_squares




class Game():
	def __init__(self):
		self.board = Board()
		self.player = 1 # Player 1- X, Player 2- 0
		self.game_mode = 'pvp' #Player v player or AI
		self.running = True
		self.show_lines()

	def show_lines(self):
		#vertical lines
		pygame.draw.line(screen, line_color, (square_size, 0), (square_size, height), line_width)
		pygame.draw.line(screen, line_color, (width - square_size, 0), (width - square_size, height), line_width)

		#horizontal lines
		pygame.draw.line(screen, line_color, (0, square_size), (width, square_size), line_width)
		pygame.draw.line(screen, line_color, (0, height - square_size), (width, height - square_size), line_width)

	def next_turn(self):
		self.player = 3 - self.player

	def draw_fig(self, row, col):
		if self.player == 1:
		#draw cross
			start_desc = (col * square_size + offset, row*square_size + offset)
			end_desc = (col * square_size + square_size - offset, row * square_size + square_size - offset)
			pygame.draw.line(screen, cross_color, start_desc, end_desc, cross_width)

			start_desc = (col * square_size + offset, row*square_size + square_size - offset)
			end_desc = (col * square_size + square_size - offset, row * square_size + offset)
			pygame.draw.line(screen, cross_color, start_desc, end_desc, cross_width)	


		elif self.player == 2:
		#draw circle
			center = (col * square_size + square_size//2, row*square_size + square_size//2)
			pygame.draw.circle(screen, circle_color, center, radius, circle_width)







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
					game.draw_fig(row, col)
					game.next_turn()
					print(board.squares)
				


		pygame.display.update()

main()