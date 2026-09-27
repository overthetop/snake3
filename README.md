# Neon Snake

A small offline Snake game with a neon board, smooth motion, responsive keyboard controls, and original synthesized music. Python + pygame-ce. No accounts, network calls, or asset downloads at runtime.

## Play

Extract the complete download, then run `NeonSnake.exe` on Windows, `NeonSnake.app` on macOS, or `./NeonSnake` inside the extracted directory on Linux. Keep the accompanying `_internal` directory with the executable. Python is included in standalone builds.

Downloads are generated as GitHub Actions artifacts in this repository's **Actions > Desktop builds** runs after the workflow is pushed. macOS builds are currently ad-hoc signed, not Apple-notarized; Windows builds are unsigned. Public trusted distribution requires release signing separately.

| Control | Action |
| --- | --- |
| Enter / Space | Start, restart after losing, or resume |
| Arrow keys / WASD | Steer |
| Escape | Pause / resume, close settings |
| Tab | Open settings |
| F11 | Toggle fullscreen |
| Settings: up/down, left/right | Select a setting, adjust volume |
| Settings: Enter | Toggle reduced effects or activate Done |

Mouse controls are also available for menus. Losing window focus pauses the run. Resuming counts down for three seconds; turns can be queued during the countdown. Fullscreen changes pause active play. Very long frame stalls also pause instead of skipping the snake into a wall.

## Rules

- One 24 by 24 board; the snake begins four cells long.
- Eat food for 10 points and one extra cell. Food appears only in empty cells.
- Hit a wall or your body and the run ends. The vacating tail cell is safe.
- Fill the board to win.
- Start at 6 cells/second. Every five foods adds 0.5, up to 12.
- Two turns can be buffered. Reverse-direction inputs and key repeats are ignored.

The settings menu has independent music/effect volumes and reduced effects. Best score and settings save automatically to `NeonSnake/settings.json` beneath `%LOCALAPPDATA%` (Windows), `~/Library/Application Support` (macOS), or `$XDG_DATA_HOME` / `~/.local/share` (Linux). Corrupt saves recover to defaults; a save failure is shown without stopping play. Audio-device failure permits silent play.

## Run from source

Use Python 3.11 or later (CI uses 3.13):

```sh
python -m venv .venv
# Windows:
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python run_game.py
# macOS / Linux:
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python run_game.py
```

## Test and package

Using the virtual environment's Python:

```sh
python -m pytest -q
python -m mypy
python run_game.py --smoke-test artifacts/smoke
python scripts/build.py
```

The smoke test runs in a hidden window with an isolated temporary save, exercises a short run and menu transitions, then saves screenshots and a completion marker. `scripts/build.py` packages the app, runs the packaged smoke test with SDL's dummy drivers, and creates an archive under `dist/archives/`. It must run on each target OS; it is not a cross-compiler.

GitHub Actions builds Windows x64, Linux x64 on Ubuntu 22.04, and separate macOS ARM64/Intel applications on macOS 15 runners. These are build/test environments, not a promise of compatibility with every older OS. Linux artifacts require a graphical desktop and compatible system libraries (glibc 2.35 or later); test other distributions before claiming support.

See [the release playtest checklist](docs/playtesting.md) for the checks that require real displays, keyboards and audio devices. Passing CI is not equivalent to a human playtest.

## Code map

- `snake3/model.py`: grid rules and turn buffer, independent of pygame.
- `snake3/app.py`: event handling, simulation clock, interpolation, drawing and menus.
- `snake3/audio.py`: procedural audio generated in memory.
- `snake3/storage.py`: validated, atomic per-user saves.
- `tests/`: rules, input/state transitions, rendering and save recovery.

The glossary is in `CONTEXT.md`; interview decisions are in `.scratch/snake/design.md`.
