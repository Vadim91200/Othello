from alphabeta import State
import numpy as np


class Game(State):
    # Constructeur pour la classe Game
    def __init__(self, size, depth, is_only_maximising=False, show_live_score=False, board=None):
        super().__init__(depth, is_only_maximising)
        self.size = size
        self.show_live_score = show_live_score
        if board is None:
            self.board = np.zeros((size, size), dtype=int)
        else:
            self.board = board

    # Méthode pour vérifier si un mouvement est valide
    def valid_move(self, move, player=None):
        return len(move) == 2 and 0 <= move[0] < self.size and 0 <= move[1] < self.size

    # Méthode pour vérifier si un joueur a gagné
    def check_win(self, player):
        pass
