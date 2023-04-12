# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 12:50:38 2023

@author: Charles-André
"""
from board import Board
def main():
    OthelloBoard = Board()
    current_color = 1
    tour = 1
    while tour <=60:
        print(OthelloBoard)
        move = input(f'{"Black" if current_color == 1 else "White"} to play (x, y): ')
        x, y = map(int, move.strip().split())

        if OthelloBoard.valid_move(x, y, current_color):
            print(OthelloBoard.valid_move(x, y, current_color))
            current_color = -1 if current_color == 1 else 1
            tour+=1
        else:
            print('Invalid move, try again.')

if __name__ == "__main__":
    main()