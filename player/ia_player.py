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
        copyedgame = game.copy()
        copyedgame.total_elapsed_time = game.total_elapsed_time
        move = alphabeta_search(copyedgame, self.player_number)
        print(f'player : {self.player_number} : move  {move}')
        game.total_elapsed_time = copyedgame.total_elapsed_time
        return move
