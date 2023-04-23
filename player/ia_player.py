from generic_player import Player
from alphabeta import alphabeta_search


class IaPlayer(Player):
    def __init__(self, player_number):
        super().__init__(player_number)

    def get_move(self, board, **kwargs):
        return alphabeta_search(board.copy(), self.player_number)
