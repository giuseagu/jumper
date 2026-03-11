import pygame
import random
from constants import (
    WIDTH, HEIGHT,
    PLATFORM_WIDTH, PLATFORM_HEIGHT,
    BOUNCE_PLATFORM_WIDTH,
    PLATFORM_MIN_GAP, PLATFORM_MAX_GAP,
    PLATFORM_COUNT, PLATFORM_COLOR, PLATFORM_BORDER,
    BOUNCE_PLATFORM_COLOR, BOUNCE_PLATFORM_BORDER,
    BREAKABLE_PLATFORM_COLOR, BREAKABLE_PLATFORM_BORDER,
    JUMP_FORCE, BOUNCE_JUMP_FORCE,
    DIFFICULTIES
)


class Platform:
    def __init__(self, x, y, width=PLATFORM_WIDTH):
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT
        self.broken = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def on_land(self):
        """Called when player lands on this platform. Returns jump force."""
        return JUMP_FORCE

    def draw(self, surface, camera_offset):
        draw_y = int(self.y - camera_offset)
        rect = pygame.Rect(self.x, draw_y, self.width, self.height)
        pygame.draw.rect(surface, PLATFORM_COLOR, rect, border_radius=6)
        pygame.draw.rect(surface, PLATFORM_BORDER, rect, width=2, border_radius=6)


class BouncePlatform(Platform):
    """Trampolino: piu piccolo, colore oro, spinge il giocatore molto piu in alto."""

    def __init__(self, x, y):
        super().__init__(x, y, width=BOUNCE_PLATFORM_WIDTH)

    def on_land(self):
        return BOUNCE_JUMP_FORCE

    def draw(self, surface, camera_offset):
        draw_y = int(self.y - camera_offset)
        rect = pygame.Rect(self.x, draw_y, self.width, self.height)
        pygame.draw.rect(surface, BOUNCE_PLATFORM_COLOR, rect, border_radius=6)
        pygame.draw.rect(surface, BOUNCE_PLATFORM_BORDER, rect, width=2, border_radius=6)
        # Indicatore visivo: freccia verso l'alto al centro
        cx = self.x + self.width // 2
        arrow_color = BOUNCE_PLATFORM_BORDER
        points = [
            (cx, draw_y - 6),
            (cx - 5, draw_y - 1),
            (cx + 5, draw_y - 1),
        ]
        pygame.draw.polygon(surface, arrow_color, points)


class BreakablePlatform(Platform):
    """Piattaforma marrone: si distrugge al primo utilizzo."""

    def __init__(self, x, y):
        super().__init__(x, y, width=PLATFORM_WIDTH)

    def on_land(self):
        self.broken = True
        return JUMP_FORCE

    def draw(self, surface, camera_offset):
        if self.broken:
            return
        draw_y = int(self.y - camera_offset)
        rect = pygame.Rect(self.x, draw_y, self.width, self.height)
        pygame.draw.rect(surface, BREAKABLE_PLATFORM_COLOR, rect, border_radius=6)
        pygame.draw.rect(surface, BREAKABLE_PLATFORM_BORDER, rect, width=2, border_radius=6)
        # Linee orizzontali che suggeriscono fragilita
        for offset in (3, 7):
            pygame.draw.line(
                surface, BREAKABLE_PLATFORM_BORDER,
                (self.x + 4, draw_y + offset),
                (self.x + self.width - 4, draw_y + offset),
                1
            )


class PlatformManager:
    def __init__(self, bounce_chance, breakable_chance):
        self.bounce_chance = bounce_chance
        self.breakable_chance = breakable_chance
        self.platforms = []
        self._generate_initial()

    def _make_platform(self, x, y):
        """Crea una piattaforma casuale in base alle probabilità della difficoltà."""
        roll = random.random()
        if roll < self.bounce_chance:
            return BouncePlatform(x, y)
        elif roll < self.bounce_chance + self.breakable_chance:
            return BreakablePlatform(x, y)
        return Platform(x, y)

    def _generate_initial(self):
        # Piattaforma di partenza: larga, al centro, nel terzo inferiore
        start_x = WIDTH // 2 - 60
        start_y = HEIGHT - 120
        self.platforms.append(Platform(start_x, start_y, width=120))

        current_y = start_y
        for _ in range(PLATFORM_COUNT - 1):
            current_y -= random.randint(PLATFORM_MIN_GAP, PLATFORM_MAX_GAP)
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            self.platforms.append(self._make_platform(x, current_y))

    def _topmost_y(self):
        return min(p.y for p in self.platforms)

    def update(self, camera_offset):
        # Genera nuove piattaforme sopra quella piu alta
        while self._topmost_y() > camera_offset - HEIGHT:
            new_y = self._topmost_y() - random.randint(PLATFORM_MIN_GAP, PLATFORM_MAX_GAP)
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            self.platforms.append(self._make_platform(x, new_y))

        # Rimuove piattaforme uscite dallo schermo o distrutte
        bottom_cutoff = camera_offset + HEIGHT + 100
        self.platforms = [
            p for p in self.platforms
            if p.y < bottom_cutoff and not p.broken
        ]

    def draw(self, surface, camera_offset):
        for p in self.platforms:
            p.draw(surface, camera_offset)
