import pygame
import random
from constants import (
    WIDTH, HEIGHT,
    PLATFORM_WIDTH, PLATFORM_HEIGHT,
    PLATFORM_MIN_GAP, PLATFORM_MAX_GAP,
    PLATFORM_COUNT, PLATFORM_COLOR, PLATFORM_BORDER
)


class Platform:
    def __init__(self, x, y, width=PLATFORM_WIDTH):
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_offset):
        draw_y = int(self.y - camera_offset)
        rect = pygame.Rect(self.x, draw_y, self.width, self.height)
        pygame.draw.rect(surface, PLATFORM_COLOR, rect, border_radius=6)
        pygame.draw.rect(surface, PLATFORM_BORDER, rect, width=2, border_radius=6)


class PlatformManager:
    def __init__(self):
        self.platforms = []
        self._generate_initial()

    def _generate_initial(self):
        # Starting platform: wide, in center, at bottom third of screen
        start_x = WIDTH // 2 - 60
        start_y = HEIGHT - 120
        self.platforms.append(Platform(start_x, start_y, width=120))

        # Generate upward platforms
        current_y = start_y
        for _ in range(PLATFORM_COUNT - 1):
            current_y -= random.randint(PLATFORM_MIN_GAP, PLATFORM_MAX_GAP)
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            self.platforms.append(Platform(x, current_y))

    def _topmost_y(self):
        return min(p.y for p in self.platforms)

    def update(self, camera_offset):
        # Generate new platforms above the topmost one
        while self._topmost_y() > camera_offset - HEIGHT:
            new_y = self._topmost_y() - random.randint(PLATFORM_MIN_GAP, PLATFORM_MAX_GAP)
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            self.platforms.append(Platform(x, new_y))

        # Remove platforms that have scrolled off bottom of screen
        bottom_cutoff = camera_offset + HEIGHT + 100
        self.platforms = [p for p in self.platforms if p.y < bottom_cutoff]

    def draw(self, surface, camera_offset):
        for p in self.platforms:
            p.draw(surface, camera_offset)
