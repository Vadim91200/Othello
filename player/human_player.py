from generic_player import Player, timer_decorator
import const
import pygame


class HumanPlayer(Player):
    # Constructeur pour la classe Human
    def __init__(self, player_number):
        super().__init__(player_number)

    # M�thode pour obtenir un mouvement d'un joueur humain
    @timer_decorator
    def get_move(self, board, **kwargs):
        update_callback = kwargs['update_callback']
        clock = pygame.time.Clock()

        total_size = board.size * const.TILE_SIZE
        start_x = (const.SCREEN_WIDTH - total_size) / 2
        start_y = (const.SCREEN_HEIGHT - total_size) / 2
        possible_moves = board.get_all_moves(self.player_number)
        # logique pour recuperer le coup du joueur humain sur l'ihm pygame
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
            # Fonction pour garder l'ihm � jours des evenements en dehors de la loop principale
            update_callback(events)
