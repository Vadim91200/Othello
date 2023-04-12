# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 12:31:05 2023

@author: Charles-André
"""
class Board:
    def __init__(self,size=8):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        mid = size // 2
        self.board[mid - 1][mid - 1] = -1
        self.board[mid - 1][mid] = 1
        self.board[mid][mid - 1] = 1
        self.board[mid][mid] = -1

    def __str__(self):
        symbols = {1: 'B', -1: 'W', 0: '.'}
        return '\n'.join([' '.join([symbols[item] for item in row]) for row in self.board]) + '\n'
    
    def valid_move(self, x, y, color):
       if self.board[x][y] != 0:
           return False

       opponent = -1 if color == 1 else 1
       directions = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx != 0 or dy != 0]

       for dx, dy in directions:
           nx, ny = x + dx, y + dy

           if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == opponent:
               while 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] != 0:
                   nx += dx
                   ny += dy

                   if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == color:
                       return True

       return False