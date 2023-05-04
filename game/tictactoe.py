from generic_game import Game
import const
import numpy as np
import hashlib

SIZE = 3
WIN = 1000.0
LOSS = -1000.0
DRAW = 0.0
cache = {}
DEPTH = 6


class Tictactoe(Game):

    def __init__(self, board=None):
        super().__init__(SIZE, DEPTH, False, board)

    def valid_move(self, move, player=None):
        return super().valid_move(move) and self.board[move] == const.EMPTY_CELL

    def check_win(self, player):
        check = self.board == player

        if np.any(check.all(axis=1)):
            return True

        if np.any(check.all(axis=0)):
            return True

        if (self.board.diagonal() == player).all():
            return True
        if (np.fliplr(self.board).diagonal() == player).all():
            return True

        return False

    def get_all_moves(self, player):
        bytes_board = self.board.data.tobytes()
        if bytes_board in cache:
            return cache[bytes_board]
        all_moves = [(row, col) for col in range(SIZE) for row in range(SIZE) if self.valid_move((row, col), player)]
        cache[bytes_board] = all_moves
        return all_moves

    def evaluate(self, player, depth):
        if self.check_win(const.FIRST_PLAYER):
            return WIN + depth
        if self.check_win(const.SECOND_PLAYER):
            return LOSS - depth
        return DRAW

    def is_end(self):
        return np.all(self.board != const.EMPTY_CELL) or \
            self.check_win(const.FIRST_PLAYER) or \
            self.check_win(const.SECOND_PLAYER)

    def apply_move(self, move, player):
        self.board[move] = player
        return self

    def copy(self):
        return Tictactoe(self.board.copy())
