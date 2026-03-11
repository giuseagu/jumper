import pygame
from constants import WIDTH, HEIGHT, DIFFICULTIES
from player import Player
from platforms import PlatformManager
from camera import Camera
from renderer import Renderer

DIFF_NAMES = list(DIFFICULTIES.keys())


class Game:
    def __init__(self, surface, config=None):
        self.surface = surface
        self.config = config or DIFFICULTIES['Media']
        self.renderer = Renderer(surface)
        self.gameover_selected = DIFF_NAMES.index(self._current_diff_name())
        self._init_state()

    def _current_diff_name(self):
        for name, cfg in DIFFICULTIES.items():
            if cfg is self.config:
                return name
        return 'Media'

    def _init_state(self):
        start_x = WIDTH // 2
        start_y = HEIGHT - 150
        self.player = Player(start_x, start_y, speed=self.config['player_speed'])
        self.initial_y = start_y
        self.platform_manager = PlatformManager(
            bounce_chance=self.config['bounce_chance'],
            breakable_chance=self.config['breakable_chance'],
        )
        self.camera = Camera()
        self.score = 0
        self.game_over = False

    def update(self, keys):
        if self.game_over:
            return

        self.player.update(keys, self.platform_manager.platforms)
        self.camera.update(self.player.y)
        self.platform_manager.update(self.camera.offset)

        climbed = self.initial_y - self.player.highest_y
        self.score = max(0, int(climbed / 10))

        if self.player.y - self.camera.offset > HEIGHT + 50:
            self.game_over = True

    def draw(self):
        self.renderer.draw_background(self.camera.offset)
        self.platform_manager.draw(self.surface, self.camera.offset)
        self.player.draw(self.surface, self.camera.offset)
        self.renderer.draw_score(self.score)

        if self.game_over:
            self.renderer.draw_gameover(self.score, self.gameover_selected)

    def _restart_with_selected(self):
        self.config = DIFFICULTIES[DIFF_NAMES[self.gameover_selected]]
        self._init_state()

    def handle_event(self, event):
        if not self.game_over:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.gameover_selected = (self.gameover_selected - 1) % len(DIFF_NAMES)
            elif event.key == pygame.K_DOWN:
                self.gameover_selected = (self.gameover_selected + 1) % len(DIFF_NAMES)
            elif event.key in (pygame.K_RETURN, pygame.K_r):
                self._restart_with_selected()

        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.renderer.gameover_box_rects):
                if rect.collidepoint(event.pos):
                    self.gameover_selected = i

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.renderer.gameover_box_rects):
                if rect.collidepoint(event.pos):
                    self.gameover_selected = i
                    self._restart_with_selected()
