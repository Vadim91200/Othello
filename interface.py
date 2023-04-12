# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 17:43:35 2023

@author: User
"""
from board import Board
import pygame
class Interface:
    def __init__(self, board_size=8, cell_size=64):
        pygame.init()
        self.board = Board(board_size)
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((board_size * cell_size, board_size * cell_size))
        pygame.display.set_caption('Othello')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)

    def draw_board(self):
        for x in range(self.board.size):
            for y in range(self.board.size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (0, 128, 0), rect, 0)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

                if self.board.board[x][y] != 0:
                    color = (255, 255, 255) if self.board.board[x][y] == -1 else (0, 0, 0)
                    pygame.draw.circle(self.screen, color, rect.center, self.cell_size // 2 - 4)

    def run(self):
        current_color = 1
        tour = 1
        while tour <=60:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    x //= self.cell_size
                    y //= self.cell_size

                    if self.board.valid_move(x, y, current_color):
                        print(self.board.valid_move(x, y, current_color))
                        current_color = -1 if current_color == 1 else 1
                        tour+=1
                    else:
                        print('Invalid move, try again.')
            self.screen.fill((0, 0, 0))
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
