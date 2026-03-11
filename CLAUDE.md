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

**Flusso di avvio** (`main.py`): inizializza pygame → mostra `MenuScreen` → riceve il `config` della difficoltà scelta → crea `Game(surface, config)` → loop event/update/draw a `config['fps']` FPS.

**`menu.py`** — `MenuScreen`: schermata di selezione difficoltà mostrata all'avvio. Navigabile con ↑↓ + INVIO o con il mouse (hover + click). Restituisce il dict config della difficoltà scelta da `DIFFICULTIES`.

**`Game`** (`game.py`): accetta `config` dict e lo propaga a `Player` (speed) e `PlatformManager` (bounce_chance, breakable_chance). Owns all state — `Player`, `PlatformManager`, `Camera`, `Renderer`. Computes score from `player.highest_y`, triggers game-over when player falls below screen bottom, handles restart (`R` key).

**`Player`** (`player.py`): accetta `speed=` nel costruttore (valore dal config, default `PLAYER_SPEED`). On platform collision calls `platform.on_land()` which returns the jump force. Tracks `highest_y` for scoring. Wraps horizontally across screen edges.

**`platforms.py`**: contiene tutte le classi piattaforma e il `PlatformManager`. File rinominato da `platform.py` a `platforms.py` per evitare shadowing del modulo standard Python (causava `AttributeError` in pygame).

- **`Platform`** (verde, 80px): piattaforma base. `on_land()` restituisce `JUMP_FORCE` (-13).
- **`BouncePlatform`** (oro, 50px): trampolino. `on_land()` restituisce `BOUNCE_JUMP_FORCE` (-24). Freccia triangolare in cima come indicatore visivo.
- **`BreakablePlatform`** (marrone, 80px): si distrugge al primo utilizzo. `on_land()` imposta `self.broken = True`. Il `PlatformManager` la rimuove al frame successivo. Linee orizzontali sul disegno ne suggeriscono la fragilità.
- **`PlatformManager(bounce_chance, breakable_chance)`**: accetta le probabilità dal config. Il metodo `_make_platform()` usa questi valori per decidere il tipo. Rimuove piattaforme uscite dallo schermo **o con `broken=True`**.

**`constants.py`** — `DIFFICULTIES`: dizionario con i parametri per ogni livello. È la fonte unica per bilanciamento e spawn:

| | Facile | Media | Difficile |
|---|---|---|---|
| `fps` | 45 | 60 | 80 |
| `player_speed` | 4 | 5 | 6 |
| `bounce_chance` | 18% | 10% | 5% |
| `breakable_chance` | 5% | 10% | 20% |
| Normali (implicito) | 77% | 80% | 75% |

Le piattaforme normali sono sempre la maggioranza. Per modificare il bilanciamento intervenire solo su `DIFFICULTIES` in `constants.py`.

**`Camera`** (`camera.py`): single `offset` float. Moves up (decreases) when player enters the upper 40% of the screen; never scrolls down.

**`Renderer`** (`renderer.py`): draws gradient background, parallax stars, score HUD, and game-over overlay. Stars use a `layer` factor (0.3, 0.6, 1.0) for depth.

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
