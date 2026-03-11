import pygame
from constants import WIDTH, HEIGHT
from player import Player
from platform import PlatformManager
from camera import Camera
from renderer import Renderer


class Game:
    def __init__(self, surface):
        self.surface = surface
        self.renderer = Renderer(surface)
        self._init_state()

    def _init_state(self):
        start_x = WIDTH // 2
        start_y = HEIGHT - 150
        self.player = Player(start_x, start_y)
        self.initial_y = start_y
        self.platform_manager = PlatformManager()
        self.camera = Camera()
        self.score = 0
        self.game_over = False

    def update(self, keys):
        if self.game_over:
            return

        self.player.update(keys, self.platform_manager.platforms)
        self.camera.update(self.player.y)
        self.platform_manager.update(self.camera.offset)

        # Score: how high the player has climbed
        climbed = self.initial_y - self.player.highest_y
        self.score = max(0, int(climbed / 10))

        # Game over: player fell below screen bottom
        if self.player.y - self.camera.offset > HEIGHT + 50:
            self.game_over = True

    def draw(self):
        self.renderer.draw_background(self.camera.offset)
        self.platform_manager.draw(self.surface, self.camera.offset)
        self.player.draw(self.surface, self.camera.offset)
        self.renderer.draw_score(self.score)

        if self.game_over:
            self.renderer.draw_gameover(self.score)

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._init_state()
