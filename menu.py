import pygame
import sys
from constants import WIDTH, HEIGHT, BG_TOP, BG_BOTTOM, DIFFICULTIES

# Colori per ogni difficoltà
DIFF_COLORS = {
    'Facile':    (80, 220, 120),
    'Media':     (255, 200, 0),
    'Difficile': (255, 80, 80),
}

DIFF_DESCRIPTIONS = {
    'Facile':    ['Velocità ridotta', 'Più trampolini dorati', 'Poche piattaforme fragili'],
    'Media':     ['Velocità normale', 'Trampolini e fragili bilanciati', ''],
    'Difficile': ['Velocità elevata', 'Pochi trampolini dorati', 'Molte piattaforme fragili'],
}


class MenuScreen:
    def __init__(self, surface):
        self.surface = surface
        self.font_title = pygame.font.SysFont("monospace", 52, bold=True)
        self.font_option = pygame.font.SysFont("monospace", 26, bold=True)
        self.font_desc = pygame.font.SysFont("monospace", 15)
        self.options = list(DIFFICULTIES.keys())
        self.selected = 1  # default: Media
        self._box_rects = []

    def run(self):
        """Mostra il menu e restituisce il config della difficoltà scelta."""
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key in (pygame.K_UP,):
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key in (pygame.K_DOWN,):
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return DIFFICULTIES[self.options[self.selected]]
                if event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(self._box_rects):
                        if rect.collidepoint(event.pos):
                            self.selected = i
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self._box_rects):
                        if rect.collidepoint(event.pos):
                            self.selected = i
                            return DIFFICULTIES[self.options[self.selected]]

            self._draw()
            pygame.display.flip()
            clock.tick(60)

    def _draw(self):
        # Sfondo sfumato
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
            g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
            b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
            pygame.draw.line(self.surface, (r, g, b), (0, y), (WIDTH, y))

        # Titolo
        title = self.font_title.render("JUMPER", True, (100, 200, 255))
        self.surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        subtitle = self.font_desc.render("Scegli la difficoltà", True, (160, 170, 200))
        self.surface.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 128))

        # Opzioni
        self._box_rects = []
        box_h = 100
        start_y = 165
        gap = 14

        for i, name in enumerate(self.options):
            box_y = start_y + i * (box_h + gap)
            box_rect = pygame.Rect(30, box_y, WIDTH - 60, box_h)
            self._box_rects.append(box_rect)
            is_selected = i == self.selected
            color = DIFF_COLORS[name]

            # Sfondo box
            bg_color = (40, 52, 82) if is_selected else (18, 22, 40)
            pygame.draw.rect(self.surface, bg_color, box_rect, border_radius=10)
            border_color = color if is_selected else (55, 65, 95)
            pygame.draw.rect(self.surface, border_color, box_rect, width=2, border_radius=10)

            # Nome difficoltà
            label_color = color if is_selected else (120, 130, 155)
            label = self.font_option.render(name, True, label_color)
            self.surface.blit(label, (box_rect.x + 18, box_rect.y + 12))

            # Descrizioni
            for j, line in enumerate(DIFF_DESCRIPTIONS[name]):
                if not line:
                    continue
                desc_color = (190, 200, 220) if is_selected else (90, 100, 120)
                desc = self.font_desc.render(line, True, desc_color)
                self.surface.blit(desc, (box_rect.x + 18, box_rect.y + 48 + j * 18))

        # Footer hint
        hint = self.font_desc.render("↑↓ seleziona   INVIO conferma   click per scegliere", True, (80, 90, 120))
        self.surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))
