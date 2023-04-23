from alphabeta import State
import numpy as np


class Board(State):

    def __init__(self, size, board=None):
        self.size = size
        if board is None:
            self.board = np.zeros((size, size), dtype=int)
        else:
            self.board = board

    def valid_move(self, move, player=None):
        return len(move) == 2 and 0 <= move[0] < self.size and 0 <= move[1] < self.size

    def check_win(self, player):
        pass
