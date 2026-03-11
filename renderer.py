import pygame
import random
from constants import (
    WIDTH, HEIGHT,
    BG_TOP, BG_BOTTOM, STAR_COLOR,
    SCORE_COLOR, GAMEOVER_COLOR
)


class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT * 4)
        self.size = random.choice([1, 1, 1, 2])
        self.layer = random.choice([0.3, 0.6, 1.0])  # parallax factor


class Renderer:
    def __init__(self, surface):
        self.surface = surface
        self.font_score = pygame.font.SysFont("monospace", 22, bold=True)
        self.font_big = pygame.font.SysFont("monospace", 42, bold=True)
        self.font_mid = pygame.font.SysFont("monospace", 24)
        self.stars = [Star() for _ in range(120)]

    def draw_background(self, camera_offset):
        # Gradient background
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
            g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
            b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
            pygame.draw.line(self.surface, (r, g, b), (0, y), (WIDTH, y))

        # Stars with parallax
        for star in self.stars:
            draw_y = int(star.y - camera_offset * star.layer) % (HEIGHT * 4)
            # Wrap star vertically within visible bands
            draw_y = draw_y % HEIGHT
            alpha = int(180 * star.layer)
            color = (
                min(255, STAR_COLOR[0]),
                min(255, STAR_COLOR[1]),
                min(255, STAR_COLOR[2])
            )
            pygame.draw.circle(self.surface, color, (star.x, draw_y), star.size)

    def draw_score(self, score):
        text = self.font_score.render(f"Score: {score}", True, SCORE_COLOR)
        self.surface.blit(text, (12, 10))

    def draw_gameover(self, score):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.surface.blit(overlay, (0, 0))

        title = self.font_big.render("GAME OVER", True, GAMEOVER_COLOR)
        score_text = self.font_mid.render(f"Score: {score}", True, SCORE_COLOR)
        restart_text = self.font_mid.render("Press R to restart", True, (180, 180, 180))

        self.surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
        self.surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        self.surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
