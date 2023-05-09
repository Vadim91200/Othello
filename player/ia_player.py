from generic_player import Player, timer_decorator
from alphabeta import alphabeta_search
import random


class IaPlayer(Player):
    # Constructeur pour la classe IA
    def __init__(self, player_number):
        super().__init__(player_number)
    # Méthode pour obtenir un mouvement d'une IA
    @timer_decorator
    def get_move(self, game, **kwargs):
        return alphabeta_search(game, self.player_number)
