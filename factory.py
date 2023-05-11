import const
from game.tictactoe import Tictactoe
from game.othello import Othello
from player.human_player import HumanPlayer
from player.ia_player import IaPlayer


# Fonction pour charger les ressources en fonction du type de jeu
def asset_factory(game_type):
    if game_type == 1:
        return const.OTHELLO_ASSETS_PATH
    elif game_type == 2:
        return const.TICTACTOE_ASSETS_PATH


# Fonction pour créer un jeu en fonction du type passé
def game_factory(game_type):
    if game_type == 1:
        return Othello()
    elif game_type == 2:
        return Tictactoe()


# Fonction pour créer un joueur en fonction du type passé
def player_factory(player_type, player_number):
    if player_type == 1:
        return HumanPlayer(player_number)
    elif player_type == 2:
        return IaPlayer(player_number)
