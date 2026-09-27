# Snake design decisions

Agreed during the grill-with-docs interview. The user confirmed shared understanding and authorized implementation.

## Product

- Offline downloadable desktop game with classic Snake rules and polished neon arcade presentation.
- One 24 x 24 board, a starting snake length of four cells, and one food at a time in an empty cell.
- Each food adds one cell and 10 points. Wall or self collision ends the run; filling the board wins.
- Start at 6 cells per second, increasing by 0.5 every five foods, capped at 12. Tune after playtesting.
- Smooth animation between cells, rounded snake, and restrained glow; turns and collisions obey the grid.
- Arrow keys and WASD, buffered quick turns, and ignored reverse-direction inputs.
- Escape pauses; losing focus automatically pauses. Resume with a short countdown. Enter restarts after a loss.
- Resizable window and optional fullscreen, preserving the full square board and fixed cell count.
- Original restrained electronic music, quiet by default, and short arcade sound effects.
- Separate volume controls and a reduced-effects option.
- Persist one local best score between launches; no accounts or online leaderboard.
- No power-ups, extra obstacles, or additional game modes.

## Implementation and delivery

- Python with pygame-ce; package standalone downloads using PyInstaller.
- Use the existing origin, git@github.com:overthetop/snake3.git, and GitHub Actions for platform builds.
- Keep issue tracking in local markdown as configured in docs/agents/issue-tracker.md.
- Targets: Windows x64, macOS Apple Silicon and Intel, and Linux x64, initially tested on Ubuntu.
- Build and automate checks on each operating system; require a human playtest on each before claiming the release is tested.
- Verify responsiveness, visuals, sound, pause/resume, restart, and score persistence during playtests.

## Release follow-through

- Exact supported OS versions, runner availability, and packaging dependencies must be verified during implementation.
- Human playtest results must be recorded; automated build success alone is insufficient.
- Signing credentials and public release publication have not been arranged or performed.

## Implementation status

The game, tests, standalone packaging script and GitHub Actions workflow have been implemented. See docs/playtesting.md for platform verification status; human playtests remain outstanding.
