from generic_game import Game
import const
import numpy as np

SIZE = 3
WIN = 1000.0
LOSS = -1000.0
DRAW = 0.0


class Tictactoe(Game):

    def __init__(self, board=None):
        super().__init__(SIZE, False, board)

    def valid_move(self, move, player=None):
        return super().valid_move(move) and self.board[move] == const.EMPTY_CELL

    def check_win(self, player):
        for row in range(SIZE):
            if np.all(self.board[row, :] == player):
                return True

        for col in range(SIZE):
            if np.all(self.board[:, col] == player):
                return True

        if np.all(self.board.diagonal() == player):
            return True
        if np.all(np.fliplr(self.board).diagonal() == player):
            return True

        return False

    def get_all_moves(self, player):
        return [(row, col) for col in range(SIZE) for row in range(SIZE) if self.valid_move((row, col), player)]

    def evaluate(self, depth):
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
