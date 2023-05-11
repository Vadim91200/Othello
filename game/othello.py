from generic_game import Game
import const
import numpy as np
from numba import njit

# Point cardinal sud, est, ouest, nord, etc...
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
# Representation du tablier 8x8 du jeu avec un score arbitraire à chaque case
# Ce tablier permet de trier une première fois les coups possibles afin d'augmenter les chances de donner
# au minmax alphabeta un coup puissant en premier et ainsi optimiser l'elagage.
WEIGHT_MAP = np.array([
    [100, -25, 20, 10, 10, 20, -25, 100],
    [-25, -25, 5, 5, 5, 5, -25, -25],
    [20, 5, 15, 3, 3, 15, 5, 20],
    [10, 5, 3, 3, 3, 3, 5, 10],
    [10, 5, 3, 3, 3, 3, 5, 10],
    [20, 5, 15, 3, 3, 15, 5, 20],
    [-25, -25, 5, 5, 5, 5, -25, -25],
    [100, -25, 20, 10, 10, 20, -25, 100]
])

SIZE = 8
# Heuristique de victoire, defaite et nul
WIN = 100000000.0
LOSS = -100000000.0
DRAW = 0.0
# Etat de la partie (debut, milieu et fin) et aussi index pour les scores d'heuristic
EARLY_GAME = 0
MID_GAME = 1
END_GAME = 2
# heuristique pour le nombre de pion (active en fin de partie)
NUMBER_OF_PIECE_MAGNITUDE = [0, 0, 5]
# heuristique pour le nombre de coup possible pour un joueur
# on veut maximiser pour le joueur actif et minimiser pour l'opposant
MOBILITY_MAGNITUDE = [200, 200, 0]
# Heuristique pour les cases adjacentes aux coins (on cherche à eviter ces cases mais elles restent jouables)
ANTI_CORNER_SCORE = [1000.0, 1000.0, 0.0]
# Heuristique strategique pour les coins, ce sont des cases très importante car elles apportent une stabilité et son
# imprenable
CORNER_SCORE = [10000.0, 10000.0, 0]
# Heuristique pour les bords (sans les coins et anti-coins), ce sont des cases stables est importante.
EGDE_MAGNITUDE = [50, 50, 0]
# Le cache permet de stocker pour un etat de l'othello et le joueur en cours le calcul des coups possibles l'objectif
# est d'eviter de recalculer tout les coups possibles d'un etat s'il est deja present dans le cache (gain de vitesse)
cache = {}
# profondeur pour le minmax (à faire varier entre 4 et 6)
DEPTH = 4


class Othello(Game):
    # Constructeur pour la classe Othello
    def __init__(self, board=None):
        super().__init__(SIZE, DEPTH, True, True, board)
        mid = SIZE // 2
        if board is None:
            self.board[mid - 1, mid - 1] = const.SECOND_PLAYER
            self.board[mid - 1, mid] = const.FIRST_PLAYER
            self.board[mid, mid - 1] = const.FIRST_PLAYER
            self.board[mid, mid] = const.SECOND_PLAYER

    def valid_move(self, move, player=None):
        if not super().valid_move(move):
            return False

        return fast_valid_move(self.board, move, player)

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
        all_moves.sort(key=lambda xy: WEIGHT_MAP[xy], reverse=True)
        cache[key] = all_moves
        return all_moves

    def is_end(self):
        return np.count_nonzero(self.board != const.EMPTY_CELL) == self.size * self.size

    def apply_move(self, move, player):
        fast_apply_move(self.board, move, player)
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
        # Calcul les positions des anti-coins, si c'est case sont occupés par le joueur actuel le score baisse
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

                    score = factor * (score + ANTI_CORNER_SCORE[game_time])

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
        # Calcul pour bord du tableau sans les coins et anti-coins
        def get_score(p):
            edge_counts = np.array([
                np.count_nonzero(self.board[0, 2:-2] == p),
                np.count_nonzero(self.board[SIZE - 1, 2:-2] == p),
                np.count_nonzero(self.board[2:-2, 0] == p),
                np.count_nonzero(self.board[2:-2, SIZE - 1] == p),
            ])
            return np.sum(edge_counts * EGDE_MAGNITUDE[game_time])

        score = get_score(player)
        score = score - get_score(1 + player % 2)
        return score


# numba est une librairie qui traduit une fonction python vers du c++ avec les meilleurs flags d'optimisation
# cette librairie aime particulierement les boucles et la librairie numpy mais deteste les classes customs et objet
# difficile à traduire vers du c++
# Toujours dans l'objectif de gagner en vitesse.
@njit
def fast_valid_move(board, move, player):
    if board[move] != const.EMPTY_CELL:
        return False
    opponent = 1 + player % 2
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for dx, dy in directions:
        nx, ny = move[0] + dx, move[1] + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx, ny] == opponent:
            while 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx, ny] != const.EMPTY_CELL:
                nx += dx
                ny += dy
                if 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx, ny] == player:
                    return True

    return False


# Applique un coup à un array numpy et cacul la logique des règles de l'othello pour retourner les pieces ennemies.
@njit
def fast_apply_move(board, move, player):
    board[move] = player
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    opponent = 1 + player % 2
    for dx, dy in directions:
        nx, ny = move[0] + dx, move[1] + dy
        to_flip = np.zeros((SIZE * SIZE, 2), dtype=np.int32)
        flip_flag = 0
        if 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx, ny] == opponent:
            while 0 <= nx < SIZE and 0 <= ny < SIZE and board[nx, ny] == opponent:
                to_flip[flip_flag, 0] = nx
                to_flip[flip_flag, 1] = ny
                flip_flag += 1
                nx += dx
                ny += dy
            if not (0 <= nx < SIZE and 0 <= ny < SIZE and board[nx, ny] == player):
                flip_flag = 0
        for i in range(flip_flag - 1, -1, -1):
            board[to_flip[i, 0], to_flip[i, 1]] = player
