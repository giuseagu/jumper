# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the game
python3 main.py

# Install dependencies
pip3 install -r requirements.txt
```

## Architecture

A vertical platformer built with pygame. The player automatically bounces on platforms and climbs upward; the goal is to get the highest score before falling off screen.

**Game loop** (`main.py`): initializes pygame, creates a `Game` instance, and runs the standard event → update → draw loop at 60 FPS.

**`Game`** (`game.py`): owns all state — `Player`, `PlatformManager`, `Camera`, `Renderer`. Computes score from `player.highest_y`, triggers game-over when player falls below screen bottom, and handles restart (`R` key).

**`Player`** (`player.py`): position/velocity physics with gravity. On platform collision calls `platform.on_land()` which returns the jump force — no hardcoded `JUMP_FORCE`. Tracks `highest_y` for scoring. Wraps horizontally across screen edges.

**`platforms.py`**: contiene tutte le classi piattaforma e il `PlatformManager`. File rinominato da `platform.py` a `platforms.py` per evitare shadowing del modulo standard Python (causava `AttributeError` in pygame).

- **`Platform`** (verde, 80px): piattaforma base. `on_land()` restituisce `JUMP_FORCE` (-13).
- **`BouncePlatform`** (oro, 50px): trampolino. `on_land()` restituisce `BOUNCE_JUMP_FORCE` (-24, quasi il doppio). Disegnata con freccia triangolare in cima. Spawn ~10% delle piattaforme.
- **`BreakablePlatform`** (marrone, 80px): si distrugge al primo utilizzo. `on_land()` imposta `self.broken = True` e restituisce `JUMP_FORCE` normale. Il `PlatformManager` la rimuove al frame successivo. Disegnata con linee orizzontali che suggeriscono fragilità. Spawn ~10% delle piattaforme.
- **`_make_platform(x, y)`**: factory function che decide il tipo in base a `SPECIAL_PLATFORM_CHANCE` (0.20 totale: 10% bounce, 10% breakable, 80% normale).
- **`PlatformManager`**: genera piattaforme proceduralmente verso l'alto. Rimuove quelle uscite dallo schermo **o con `broken=True`**.

**`Camera`** (`camera.py`): single `offset` float. Moves up (decreases) when player enters the upper 40% of the screen; never scrolls down.

**`Renderer`** (`renderer.py`): draws gradient background, parallax stars, score HUD, and game-over overlay. Stars use a `layer` factor (0.3, 0.6, 1.0) for depth.

**`constants.py`**: single source of truth for physics (`GRAVITY`, `JUMP_FORCE`, `BOUNCE_JUMP_FORCE`, `PLAYER_SPEED`), dimensions, colors (incluse `BOUNCE_PLATFORM_COLOR`, `BREAKABLE_PLATFORM_COLOR`), e `SPECIAL_PLATFORM_CHANCE`.

## Git workflow

Dopo ogni modifica significativa al codice (nuova funzionalità, bugfix, refactoring rilevante) esegui sempre commit e push.

I messaggi di commit devono spiegare **cosa** è cambiato, **perché** è stato fatto e **cosa ha risolto**, seguendo questo formato:

```
<tipo>: <titolo breve e descrittivo>

- Cosa è stato modificato e in quale file
- Perché la modifica era necessaria (causa del problema o motivazione)
- Cosa ha risolto o migliorato
```

Tipi comuni: `fix`, `feat`, `refactor`, `chore`, `docs`.

Esempio:
```
fix: rinomina platform.py in platforms.py per evitare conflitto con stdlib

- Rinominato platform.py → platforms.py
- Il nome platform.py shadowing il modulo standard Python causava
  AttributeError in pkg_resources al momento dell'import di pygame
- Aggiornato l'import in game.py di conseguenza
```
