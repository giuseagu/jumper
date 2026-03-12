import pygame
import random
from constants import (
    WIDTH, HEIGHT,
    BG_TOP, BG_BOTTOM, STAR_COLOR,
    SCORE_COLOR, GAMEOVER_COLOR,
    DIFFICULTIES, DIFF_COLORS
)

DIFF_NAMES = list(DIFFICULTIES.keys())


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
        self.font_small = pygame.font.SysFont("monospace", 15)
        self.font_diff = pygame.font.SysFont("monospace", 20, bold=True)
        self.stars = [Star() for _ in range(120)]
        self.gameover_box_rects = []  # popolato da draw_gameover, usato da Game per i click

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
            draw_y = draw_y % HEIGHT
            pygame.draw.circle(self.surface, STAR_COLOR, (star.x, draw_y), star.size)

    def draw_score(self, score):
        text = self.font_score.render(f"Score: {score}", True, SCORE_COLOR)
        self.surface.blit(text, (12, 10))

    def draw_gameover(self, score, selected_idx, top3=None):
        # Overlay semi-trasparente
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.surface.blit(overlay, (0, 0))

        # Titolo e score
        title = self.font_big.render("GAME OVER", True, GAMEOVER_COLOR)
        score_text = self.font_mid.render(f"Score: {score}", True, SCORE_COLOR)
        self.surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
        self.surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 92))

        # Top 3 punteggi per difficoltà
        if top3:
            diff_name = top3[0].get('difficulty', '')
            diff_color = DIFF_COLORS.get(diff_name, (255, 210, 60))
            top_label = self.font_small.render(f"TOP 3 — {diff_name}", True, diff_color)
            self.surface.blit(top_label, (WIDTH // 2 - top_label.get_width() // 2, 125))
            medals = ["1.", "2.", "3."]
            medal_colors = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]
            for i, entry in enumerate(top3):
                line = self.font_small.render(
                    f"{medals[i]}  {entry['score']} pt",
                    True, medal_colors[i]
                )
                self.surface.blit(line, (WIDTH // 2 - line.get_width() // 2, 143 + i * 18))

        # Etichetta sezione difficoltà
        label = self.font_small.render("Scegli difficoltà e rigioca:", True, (160, 170, 200))
        self.surface.blit(label, (WIDTH // 2 - label.get_width() // 2, 205))

        # Box difficoltà
        self.gameover_box_rects = []
        box_h = 58
        box_w = WIDTH - 60
        start_y = 225
        gap = 8

        for i, name in enumerate(DIFF_NAMES):
            box_y = start_y + i * (box_h + gap)
            box_rect = pygame.Rect(30, box_y, box_w, box_h)
            self.gameover_box_rects.append(box_rect)
            is_selected = i == selected_idx
            color = DIFF_COLORS[name]

            bg_color = (40, 52, 82) if is_selected else (18, 22, 40)
            pygame.draw.rect(self.surface, bg_color, box_rect, border_radius=8)
            border_color = color if is_selected else (55, 65, 95)
            pygame.draw.rect(self.surface, border_color, box_rect, width=2, border_radius=8)

            label_color = color if is_selected else (110, 120, 145)
            diff_label = self.font_diff.render(name, True, label_color)
            self.surface.blit(diff_label, (box_rect.x + 14, box_rect.y + 10))

            if is_selected:
                hint_text = self.font_small.render("INVIO o R per riavviare", True, (190, 200, 220))
            else:
                hint_text = self.font_small.render("click per selezionare", True, (70, 80, 105))
            self.surface.blit(hint_text, (box_rect.x + 14, box_rect.y + 36))

        # Footer
        footer = self.font_small.render("↑↓ seleziona   INVIO / R riavvia   click per scegliere", True, (70, 80, 110))
        self.surface.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 28))
