import numpy as np

import const
from factory import game_factory, player_factory, asset_factory

import pygame
import pygame_menu

PLAYABLE_TILE_INDEX = -1
HUMAN = ('Humain', 1)
IA = ('IA', 2)
TICTACTOE = ('Tictactoe', 2)
OTHELLO = ('Othello', 1)
PLAYER_TYPES = [HUMAN, IA]
GAME_MODES = [OTHELLO, TICTACTOE]
PURPLE_TILE = (206, 169, 245)
BORDER_COLOR = (54, 54, 54)


class GUI:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h

        main_theme = pygame_menu.themes.THEME_SOLARIZED
        self.main_menu = pygame_menu.Menu(
            title='CA-S Game studio',
            theme=main_theme,
            width=self.screen_width,
            height=self.screen_height,
        )

        self.player1 = HUMAN
        self.player2 = HUMAN
        self.game_type = OTHELLO

        def set_player1(selected_item, *_):
            self.player1 = selected_item[0]

        def set_player2(selected_item, *_):
            self.player2 = selected_item[0]

        def set_game_type(selected_item, *_):
            self.game_type = selected_item[0]

        self.main_menu.add.selector(title='Joueur 1 : ', items=PLAYER_TYPES, onchange=set_player1)
        self.main_menu.add.selector(title='Joueur 2 : ', items=PLAYER_TYPES, onchange=set_player2)
        self.main_menu.add.selector(title='Mode de jeux : ', items=GAME_MODES, onchange=set_game_type)
        self.main_menu.add.button('Jouer', self.game_loop)
        self.main_menu.add.button('Quitter', pygame_menu.events.EXIT)

    def run(self):
        self.main_menu.mainloop(self.surface)

    def draw_board(self, board, start_xy, possible_moves, asset):
        for row in range(board.size):
            for col in range(board.size):
                x = row * const.TILE_SIZE + start_xy[0]
                y = col * const.TILE_SIZE + start_xy[1]
                rect = pygame.Rect(x, y, const.TILE_SIZE, const.TILE_SIZE)
                pygame.draw.rect(self.surface, PURPLE_TILE, rect, border_radius=5)
                pygame.draw.rect(self.surface, BORDER_COLOR, rect, 2, border_radius=5)
                cell = board.board[row, col]
                if cell != const.EMPTY_CELL:
                    self.surface.blit(asset[cell - 1], (x, y))
                elif (row, col) in possible_moves:
                    self.surface.blit(asset[PLAYABLE_TILE_INDEX], (x, y))

    def announce_score(self, player=None):
        font = pygame.font.Font(None, 80)
        text = f'Le joueur 1 gagne la partie' if player == 1 else 'Le joueur 2 gagne la partie' if player else 'Match nul !'
        text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))
        text_x = (self.surface.get_width() - text_surface.get_width()) // 2
        text_y = (self.surface.get_height() - text_surface.get_height()) // 2
        self.surface.blit(text_surface, (text_x, text_y))

    def update(self, events, **kwargs):
        self.draw_board(kwargs['game'], kwargs['start_xy'], kwargs['possible_moves'], kwargs['assets'])

        if kwargs['score'][0]:
            self.announce_score(kwargs['score'][1])
                    
        pygame.display.update()
        kwargs['menu'].update(events)
        kwargs['menu'].draw(self.surface)

    def game_loop(self):
        assets_path = asset_factory(self.game_type[1])
        played_game = game_factory(self.game_type[1])
        players = [player_factory(self.player1[1], const.FIRST_PLAYER),
                   player_factory(self.player2[1], const.SECOND_PLAYER)]
        assets = [pygame.image.load(path) for path in assets_path]
        current_player = const.FIRST_PLAYER

        theme = pygame_menu.themes.THEME_DARK
        theme.background_color = (54, 54, 54)
        theme.widget_margin = ((self.screen_width / 2) * 0.75, 0)
        game_menu = pygame_menu.Menu(
            title=self.game_type[0],
            theme=theme,
            width=self.screen_width,
            height=self.screen_height
        )

        player_1_score = None
        player_2_score = None
        total_time_label = None
        if played_game.show_live_score:
            game_menu.add.label('Score:', underline=True)
            frame1 = game_menu.add.frame_h(180, 110)
            frame1.pack(game_menu.add.image(assets_path[0]).set_margin(0, 0))
            player_1_score = frame1.pack(
                game_menu.add.label(np.count_nonzero(played_game.board == const.FIRST_PLAYER)).set_margin(0, 0),
                vertical_position=pygame_menu.locals.POSITION_CENTER)

            frame2 = game_menu.add.frame_h(180, 110)
            frame2.pack(game_menu.add.image(assets_path[1]).set_margin(0, 0), align=pygame_menu.locals.ALIGN_LEFT)
            player_2_score = frame2.pack(
                game_menu.add.label(np.count_nonzero(played_game.board == const.FIRST_PLAYER)).set_margin(0, 0),
                vertical_position=pygame_menu.locals.POSITION_CENTER)

            game_menu.add.vertical_margin(10)
            
            if self.player1[1] != 1 or self.player2[1] != 1:
                game_menu.add.label('Total time:', underline=True)
                total_time_label = game_menu.add.label(f'{played_game.total_elapsed_time:.2f} s')
                game_menu.add.vertical_margin(10)

        game_menu.add.button('Rejouer', self.game_loop)
        game_menu.add.button('Menu principal', self.run)

        total_size = played_game.size * const.TILE_SIZE
        start_x = (self.surface.get_width() - total_size) / 2
        start_y = (self.surface.get_height() - total_size) / 2

        is_end = False
        winner = None
        possible_moves = played_game.get_all_moves(const.FIRST_PLAYER)
        while True:
            self.clock.tick(const.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            update_info = {
                'score': (is_end, winner),
                'menu': game_menu,
                'game': played_game,
                'start_xy': (start_x, start_y),
                'possible_moves': possible_moves,
                'assets': assets
            }
            self.update(events, **update_info)
            total_time_label.set_title(f'{played_game.total_elapsed_time:.2f} s')

            if not is_end and len(possible_moves) > 0:
                move = players[current_player - 1].get_move(played_game,
                                                            update_callback=lambda e: self.update(e, **update_info))

                played_game.apply_move(move, current_player)

                if played_game.show_live_score:
                    player_1_score.set_title(str(np.count_nonzero(played_game.board == const.FIRST_PLAYER)))
                    player_2_score.set_title(str(np.count_nonzero(played_game.board == const.SECOND_PLAYER)))

                if played_game.is_end():
                    if played_game.check_win(const.FIRST_PLAYER):
                        winner = const.FIRST_PLAYER
                    elif played_game.check_win(const.SECOND_PLAYER):
                        winner = const.SECOND_PLAYER
                    is_end = True

            current_player = 1 + current_player % 2
            possible_moves = played_game.get_all_moves(current_player)


if __name__ == '__main__':
    game = GUI()
    game.run()
