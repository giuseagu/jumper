# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the game
python3 main.py

# Install dependencies (venv already configured in .vscode/settings.json)
pip3 install -r requirements.txt
```

## Architecture

Vertical platformer in pygame. Il player rimbalza sulle piattaforme salendo verso l'alto; l'obiettivo è raggiungere il punteggio più alto prima di cadere fuori schermo.

---

### Flusso di avvio (`main.py`)
`main.py` → inizializza pygame → mostra `MenuScreen` → riceve il `config` della difficoltà scelta → crea `Game(surface, config)` → loop event/update/draw a `config['fps']` FPS.

---

### File principali

**`menu.py`** — `MenuScreen`
Schermata di selezione difficoltà all'avvio. Navigabile con ↑↓ + INVIO o mouse. Restituisce il dict config della difficoltà scelta da `DIFFICULTIES`.

**`game.py`** — `Game`
Accetta `config` dict e lo propaga a `Player` (speed) e `PlatformManager` (bounce_chance, breakable_chance). Gestisce tutto lo stato: `Player`, `PlatformManager`, `Camera`, `Renderer`, score, game-over e restart (`R`). Al game over chiama `save_score()` e carica i top 3 per la difficoltà corrente.

**`player.py`** — `Player`
Accetta `speed=` dal config. Al contatto con una piattaforma chiama `platform.on_land()` che restituisce la forza di salto. Traccia `highest_y` per il calcolo del punteggio. Si teletrasporta da un lato all'altro dello schermo.

**`platforms.py`** — piattaforme e `PlatformManager`
Contiene tutte le classi piattaforma. Rinominato da `platform.py` per evitare shadowing del modulo standard Python.

| Tipo | Colore | Larghezza | Comportamento |
|---|---|---|---|
| `Platform` | Verde | 80px | Base, `on_land()` → `JUMP_FORCE` (-13) |
| `BouncePlatform` | Oro | 50px | Trampolino, `on_land()` → `BOUNCE_JUMP_FORCE` (-24) |
| `BreakablePlatform` | Marrone | 80px | Si distrugge al primo uso (`broken=True`) |

`PlatformManager(bounce_chance, breakable_chance)`: genera piattaforme con le probabilità dal config. Rimuove quelle uscite dallo schermo o con `broken=True`.

**`constants.py`** — `DIFFICULTIES`
Fonte unica per bilanciamento e spawn. Per modificare i parametri di gioco intervenire solo qui.

| | Facile | Media | Difficile |
|---|---|---|---|
| `fps` | 45 | 60 | 80 |
| `player_speed` | 4 | 5 | 6 |
| `bounce_chance` | 18% | 10% | 5% |
| `breakable_chance` | 5% | 10% | 20% |
| Normali (implicito) | 77% | 80% | 75% |

**`camera.py`** — `Camera`
Singolo `offset` float. Scorre verso l'alto quando il player entra nel 40% superiore dello schermo. Non scorre mai verso il basso.

**`renderer.py`** — `Renderer`
Disegna sfondo gradiente, stelle con parallax (layer 0.3/0.6/1.0), score HUD e overlay game over. La schermata game over mostra lo score attuale, il TOP 3 per la difficoltà corrente e i box per scegliere la difficoltà e riavviare.

**`scores.py`** — gestione punteggi locali
Salva e legge i punteggi dal file `scores.json` (locale, non versionato su git).

- `save_score(score, difficulty)` — aggiunge una entry con score e difficoltà
- `top_scores(difficulty, n=3)` — restituisce i migliori `n` punteggi per quella difficoltà

`scores.json` è in `.gitignore`: i dati rimangono solo sul dispositivo locale.

---

## Git workflow

Dopo ogni modifica significativa esegui sempre commit e push.

I messaggi di commit devono spiegare **cosa** è cambiato, **perché** e **cosa ha risolto**:

```
<tipo>: <titolo breve e descrittivo>

- Cosa è stato modificato e in quale file
- Perché la modifica era necessaria
- Cosa ha risolto o migliorato
```

Tipi comuni: `fix`, `feat`, `refactor`, `chore`, `docs`.
