from generic_player import Player
from alphabeta import alphabeta_search
import random


class IaPlayer(Player):
    def __init__(self, player_number):
        super().__init__(player_number)

    def get_move(self, game, **kwargs):
        # moves= board.get_all_moves(self.player_number)
        # random.shuffle(moves)
        # return moves[0]

        return alphabeta_search(game.copy(), self.player_number)
