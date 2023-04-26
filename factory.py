from board.tictactoe import Tictactoe
from board.othello import Othello
from player.human_player import HumanPlayer
from player.ia_player import IaPlayer
import pygame


def asset_factory(game_type):
    if game_type == 1:
        return pygame.image.load('asset/othello_player_1.png'), pygame.image.load('asset/othello_player_2.png'), \
            pygame.image.load('asset/playable_tile.png')

    elif game_type == 2:
        return pygame.image.load('asset/tictactoe_player_1.png'), pygame.image.load('asset/tictactoe_player_2.png'), \
            pygame.image.load('asset/playable_tile.png')


def board_factory(game_type):
    if game_type == 1:
        return Othello()
    elif game_type == 2:
        return Tictactoe()


def player_factory(player_type, player_number):
    if player_type == 1:
        return HumanPlayer(player_number)
    elif player_type == 2:
        return IaPlayer(player_number)
