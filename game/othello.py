from generic_game import Game
import const
import numpy as np

SIZE = 8
WIN = 100000000.0
LOSS = -100000000.0
DRAW = 0.0

EARLY_GAME = 0
MID_GAME = 1
END_GAME = 2
NUMBER_OF_PIECE_MAGNITUDE = [0, 0, 4]
MOBILITY_MAGNITUDE = [400, 300, 0]
ANTI_CORNER_SCORE = [1000.0, 1000.0, 0.0]
CORNER_SCORE = [2000.0, 2000.0, 0]
EGDE_MAGNITUDE = [50, 50, 0]

cache = {}
DEPTH = 4


class Othello(Game):
    def __init__(self, board=None):
        super().__init__(SIZE, True, DEPTH, board)
        mid = SIZE // 2
        if board is None:
            self.board[mid - 1, mid - 1] = const.SECOND_PLAYER
            self.board[mid - 1, mid] = const.FIRST_PLAYER
            self.board[mid, mid - 1] = const.FIRST_PLAYER
            self.board[mid, mid] = const.SECOND_PLAYER

    def valid_move(self, move, player=None):
        if not super().valid_move(move):
            return False
        if self.board[move] != const.EMPTY_CELL:
            return False
        opponent = 1 + player % 2
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dx, dy in directions:
            nx, ny = move[0] + dx, move[1] + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx, ny] == opponent:
                while 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx, ny] != const.EMPTY_CELL:
                    nx += dx
                    ny += dy
                    if 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx, ny] == player:
                        return True

        return False

    def count_piece(self, player):
        return np.count_nonzero(self.board == player)

    def check_win(self, player):
        if self.is_end():
            return self.count_piece(player) > self.count_piece(1 + player % 2)

    def get_all_moves(self, player):
        key = self.board.data.tobytes(), player
        if key in cache:
            return cache[key]
        all_moves = [(row, col) for col in range(SIZE) for row in range(SIZE) if self.valid_move((row, col), player)]
        cache[key] = all_moves
        return all_moves

    def is_end(self):
        return np.all(self.board != const.EMPTY_CELL)

    def apply_move(self, move, player):
        self.board[move] = player
        opponent = 1 + player % 2
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            nx, ny = move[0] + dx, move[1] + dy
            to_flip = []
            if 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx, ny] == opponent:
                while 0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx, ny] == opponent:
                    to_flip.append((nx, ny))
                    nx += dx
                    ny += dy
                if not (0 <= nx < SIZE and 0 <= ny < SIZE and self.board[nx, ny] == player):
                    to_flip.clear()
            for flip_row, flip_col in to_flip:
                self.board[flip_row, flip_col] = player
        return self

    def copy(self):
        return Othello(self.board.copy())

    def evaluate(self, player, depth):
        if self.check_win(player):
            return WIN + self.piece_count_heuristic(player, END_GAME)
        elif self.check_win(1 + player % 2):
            return LOSS + self.piece_count_heuristic(player, END_GAME)

        played_piece_count = np.count_nonzero(self.board != const.EMPTY_CELL)
        if played_piece_count < 12:
            game_time = EARLY_GAME
        elif played_piece_count < 58:
            game_time = MID_GAME
        else:
            game_time = END_GAME

        score = 0
        if NUMBER_OF_PIECE_MAGNITUDE[game_time] != 0:
            score = score + self.piece_count_heuristic(player, game_time)
        if MOBILITY_MAGNITUDE[game_time] != 0:
            score = score + self.mobility_heuristic(player, game_time)
        if ANTI_CORNER_SCORE[game_time] != 0:
            score = score + self.anti_corner_heuristic(player, game_time)
        if CORNER_SCORE[game_time] != 0:
            score = score + self.corner_heuristic(player, game_time)
        if EGDE_MAGNITUDE[game_time] != 0:
            score = score + self.edge_heuristic(player, game_time)

        return score

    def mobility_heuristic(self, player, game_time):
        score = 0
        score = score + len(self.get_all_moves(player)) * MOBILITY_MAGNITUDE[game_time]
        score = score - len(self.get_all_moves(1 + player % 2)) * MOBILITY_MAGNITUDE[game_time]
        return score

    def piece_count_heuristic(self, player, game_time):
        score = self.count_piece(player) * NUMBER_OF_PIECE_MAGNITUDE[game_time]
        score = score - self.count_piece(1 + player % 2) * NUMBER_OF_PIECE_MAGNITUDE[game_time]
        return score

    def anti_corner_heuristic(self, player, game_time):
        score = 0
        for x, y in [(0, 0), (0, SIZE - 1), (SIZE - 1, 0), (SIZE - 1, SIZE - 1)]:
            if self.board[x, y] == const.EMPTY_CELL:
                for nx, ny in [(1, 0), (1, 1), (0, 1)]:
                    dx = (nx + x) % (SIZE - 1)
                    dy = (ny + y) % (SIZE - 1)

                    if self.board[dx, dy] == const.EMPTY_CELL:
                        continue
                    elif self.board[dx, dy] == player:
                        factor = -1
                    else:
                        factor = 1

                    if (nx, ny) == (1, 1):
                        score = factor * (score + ANTI_CORNER_SCORE[game_time])
                    else:
                        score = factor * (score + ANTI_CORNER_SCORE[game_time]) / 2
        return score

    def corner_heuristic(self, player, game_time):
        score = 0
        for x, y in [(0, 0), (0, SIZE - 1), (SIZE - 1, 0), (SIZE - 1, SIZE - 1)]:
            if self.board[x, y] == player:
                score = score + CORNER_SCORE[game_time]
            elif self.board[x, y] == 1 + player % 2:
                score = score - CORNER_SCORE[game_time]
        return score

    def edge_heuristic(self, player, game_time):
        def get_score(p):
            edge_counts = np.array([
                np.count_nonzero(self.board[0, 2:-2] == p),
                np.count_nonzero(self.board[SIZE - 1, 2:-2] == p),
                np.count_nonzero(self.board[2:-2, 0] == player),
                np.count_nonzero(self.board[2:-2, SIZE - 1] == p),
            ])
            return np.sum(edge_counts * EGDE_MAGNITUDE[game_time])

        score = get_score(player)
        score = score - get_score(1 + player % 2)
        return score
