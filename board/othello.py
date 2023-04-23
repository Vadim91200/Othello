from generic_board import Board
import const
import numpy as np

SIZE = 8
WIN = 1000.0
LOSS = -1000.0
DRAW = 0.0


class Othello(Board):
    def __init__(self, board=None):
        super().__init__(SIZE, board)
        mid = SIZE // 2
        self.board[mid - 1, mid - 1] = const.SECOND_PLAYER
        self.board[mid - 1, mid] = const.FIRST_PLAYER
        self.board[mid, mid - 1] = const.FIRST_PLAYER
        self.board[mid, mid] = const.SECOND_PLAYER

    def valid_move(self, move, player=None):
        if not super().valid_move(move):
            return False

        opponent = 1 + player % 2
        directions = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx != 0 or dy != 0]

        for dx, dy in directions:
            nx, ny = move[0] + dx, move[1] + dy

            if 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx][ny] == opponent:
                while 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx][ny] != const.EMPTY_CELL:
                    nx += dx
                    ny += dy

                    if 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx][ny] == player:
                        return True

        return False

    def check_win(self, player):
        if self.is_end():
            return np.count_nonzero(self.board == player) > np.count_nonzero(self.board == 1 + player % 2)

    def get_all_moves(self, player):
        return [(row, col) for col in range(SIZE) for row in range(SIZE) if self.valid_move((row, col), player)]

    def evaluate(self, depth):
        pass

    def is_end(self):
        return np.all(self.board != const.EMPTY_CELL)

    def apply_move(self, move, player):
        self.board[move] = player

    def copy(self):
        return Othello(self.board.copy())