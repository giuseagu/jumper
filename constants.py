WIDTH = 400
HEIGHT = 600

FPS = 60

# Colors
BG_TOP = (10, 10, 30)
BG_BOTTOM = (20, 30, 60)
STAR_COLOR = (255, 255, 255)
PLATFORM_COLOR = (50, 200, 150)
PLATFORM_BORDER = (30, 160, 120)
BOUNCE_PLATFORM_COLOR = (255, 200, 0)
BOUNCE_PLATFORM_BORDER = (200, 140, 0)
BREAKABLE_PLATFORM_COLOR = (139, 90, 43)
BREAKABLE_PLATFORM_BORDER = (90, 55, 20)
PLAYER_BODY = (100, 180, 255)
PLAYER_HEAD = (220, 220, 255)
SCORE_COLOR = (255, 255, 255)
GAMEOVER_COLOR = (255, 80, 80)

# Physics
GRAVITY = 0.4
JUMP_FORCE = -13
BOUNCE_JUMP_FORCE = -24
PLAYER_SPEED = 5

# Player dimensions
PLAYER_WIDTH = 28
PLAYER_HEIGHT = 36
HEAD_RADIUS = 12

# Platform dimensions
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 12
BOUNCE_PLATFORM_WIDTH = 50
PLATFORM_MIN_GAP = 60
PLATFORM_MAX_GAP = 110

# How many platforms to keep on screen
PLATFORM_COUNT = 10

# Colori associati a ogni difficoltà (usati in menu e game over)
DIFF_COLORS = {
    'Facile':    (80, 220, 120),
    'Media':     (255, 200, 0),
    'Difficile': (255, 80, 80),
}

# Difficoltà: fps, velocità player, probabilità piattaforme speciali
# Le normali sono sempre la maggioranza (>75% in tutti i livelli)
DIFFICULTIES = {
    'Facile':    {'fps': 45, 'player_speed': 4, 'bounce_chance': 0.18, 'breakable_chance': 0.05},
    'Media':     {'fps': 60, 'player_speed': 5, 'bounce_chance': 0.10, 'breakable_chance': 0.10},
    'Difficile': {'fps': 80, 'player_speed': 6, 'bounce_chance': 0.05, 'breakable_chance': 0.20},
}
