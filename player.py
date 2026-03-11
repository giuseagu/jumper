import pygame
from constants import (
    WIDTH, GRAVITY, JUMP_FORCE, PLAYER_SPEED,
    PLAYER_WIDTH, PLAYER_HEIGHT, HEAD_RADIUS,
    PLAYER_BODY, PLAYER_HEAD
)


class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.highest_y = y

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height),
            self.width,
            self.height
        )

    def update(self, keys, platforms):
        # Horizontal input
        if keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED
        else:
            self.vx = 0

        # Gravity
        self.vy += GRAVITY

        # Move
        self.x += self.vx
        self.y += self.vy

        # Wrap horizontally
        if self.x < -self.width // 2:
            self.x = WIDTH + self.width // 2
        elif self.x > WIDTH + self.width // 2:
            self.x = -self.width // 2

        # Platform collisions (only when falling)
        if self.vy >= 0:
            player_rect = self.get_rect()
            # Expand check rect slightly for the feet
            feet_rect = pygame.Rect(
                player_rect.x, player_rect.bottom - 8,
                player_rect.width, 8
            )
            for platform in platforms:
                p_rect = platform.get_rect()
                if feet_rect.colliderect(p_rect):
                    # Land on platform
                    self.y = p_rect.top
                    self.vy = JUMP_FORCE
                    break

        # Track highest point (lower y = higher on screen)
        if self.y < self.highest_y:
            self.highest_y = self.y

    def draw(self, surface, camera_offset):
        draw_y = int(self.y - camera_offset)
        cx = int(self.x)

        # Body
        body_rect = pygame.Rect(
            cx - self.width // 2,
            draw_y - self.height + HEAD_RADIUS,
            self.width,
            self.height - HEAD_RADIUS
        )
        pygame.draw.rect(surface, PLAYER_BODY, body_rect, border_radius=5)

        # Head
        head_y = draw_y - self.height + HEAD_RADIUS
        pygame.draw.circle(surface, PLAYER_HEAD, (cx, head_y), HEAD_RADIUS)

        # Eyes
        eye_color = (30, 30, 80)
        pygame.draw.circle(surface, eye_color, (cx - 4, head_y - 2), 3)
        pygame.draw.circle(surface, eye_color, (cx + 4, head_y - 2), 3)
