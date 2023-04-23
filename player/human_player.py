from generic_player import Player
import const
import pygame


class HumanPlayer(Player):

    def __init__(self, player_number):
        super().__init__(player_number)

    def get_move(self, board, **kwargs):
        update_callback = kwargs['update_callback']
        start_x, start_y = kwargs['start_coord']
        possible_moves = kwargs['possible_moves']
        clock = pygame.time.Clock()

        while True:
            clock.tick(const.FPS)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = e.pos
                    x = int((x - start_x) // const.TILE_SIZE)
                    y = int((y - start_y) // const.TILE_SIZE)
                    if (x, y) in possible_moves:
                        return x, y

            update_callback(events)
