# Neon Snake — Product Requirements

Status: ready-for-agent

This document consolidates the agreed first-release requirements and the implementation already delivered. The user confirmed the testing boundaries before publication to the local markdown issue tracker. It does not request that completed functionality be rebuilt.

## Problem Statement

The player wants the simplicity of classic Snake with modern graphics and satisfying, responsive gameplay. The game must run offline on Windows, macOS, and Linux, be easy to launch without installing Python, and deliver short, replayable runs without accounts or unnecessary game mechanics.

## Solution

Provide an offline desktop game with one fixed board, keyboard steering, food, growth, score, lethal collisions, and a win when the board is filled. Pair these familiar rules with smooth animation, readable neon visuals, restrained effects, original music and sound, safe pause/resume behavior, immediate restarts, and a persistent local best score.

Deliver standalone downloads for Windows x64, macOS Apple Silicon, macOS Intel, and Linux x64. Automate builds and behavioral checks for each target, then validate the actual experience through human playtesting.

## User Stories

1. As a player, I want to launch a standalone download without installing Python, so that getting started is straightforward.
2. As a Windows player, I want a Windows x64 build, so that I can play on my PC.
3. As an Apple Silicon Mac player, I want a native ARM64 build, so that I can play on my Mac.
4. As an Intel Mac player, I want an Intel build, so that I can play on my Mac.
5. As a Linux player, I want an x64 build verified on Ubuntu, so that I have a supported starting point.
6. As a player, I want to play entirely offline without an account, so that a network connection never interrupts a run.
7. As a player, I want the title screen to show how to start and steer, so that I can begin without reading separate documentation.
8. As a player, I want to start with Enter or Space, so that I can begin with the keyboard.
9. As a player, I want a fixed 24 by 24 board, so that the playing space remains predictable.
10. As a player, I want a four-cell starting snake, so that every new run begins under the same rules.
11. As a player, I want both arrow keys and WASD, so that I can use a comfortable keyboard layout.
12. As a player, I want rapid successive turns to be buffered, so that intentional corner combinations are not lost between movement steps.
13. As a player, I want reverse-direction inputs and repeated key events ignored, so that accidental inputs do not immediately reverse the snake into itself.
14. As a player, I want one food at a time in an empty cell, so that there is always a clear, reachable target while space remains.
15. As a player, I want food to add one cell and 10 points, so that growth and scoring are easy to understand.
16. As a player, I want to see my current score during a run, so that I can judge my progress.
17. As a player, I want speed to increase gradually as I eat, so that a run becomes more challenging.
18. As a player, I want a maximum speed, so that late-game play remains controllable.
19. As a player, I want collisions with walls and my own body to end the run consistently, so that losses feel fair.
20. As a player, I want to enter the tail's cell when it vacates that cell, so that collision rules match the snake's actual movement.
21. As a player, I want filling the board to count as a win, so that completing the challenge has a defined outcome.
22. As a player, I want smooth movement with precise grid-based turns and collisions, so that visual polish preserves reliable rules.
23. As a player, I want the snake, food, and board boundary to remain clearly distinguishable, so that effects never hide information needed to play.
24. As a player, I want a rounded snake and restrained neon glow, so that the game looks modern while staying focused.
25. As a player, I want clear feedback when eating, losing, or winning, so that important events feel satisfying.
26. As a player, I want Escape to pause, so that I can take a break without abandoning a run.
27. As a player, I want switching away from the window to pause automatically, so that interruptions do not cause an unfair loss.
28. As a player, I want a three-second countdown before resuming, so that I can prepare to steer.
29. As a player, I want the snake to stay still during pause and countdown, so that resuming does not advance hidden game time.
30. As a player, I want a long frame stall to pause play, so that the game does not catch up by moving me into a wall.
31. As a player, I want Enter or Space to restart after a run ends, so that trying again takes one action.
32. As a player, I want a new run to reset my score while preserving my best score, so that each attempt is independent.
33. As a player, I want my best score to survive quitting and relaunching, so that I retain a personal goal.
34. As a player, I want a resizable window that preserves the entire square board, so that I can fit the game to my display.
35. As a player, I want an optional fullscreen view, so that I can choose a more immersive presentation.
36. As a player, I want fullscreen changes to pause active play, so that changing the display cannot cost me a run.
37. As a player, I want quiet original electronic music and short arcade sound effects, so that audio supports concentration and feedback.
38. As a player, I want independent music and sound-effect volume controls, so that I can tune or mute either independently.
39. As a player, I want reduced effects, so that I can remove glow, particles, and pulsing when they distract me.
40. As a player, I want settings to persist between launches, so that I do not repeat my preferences each time.
41. As a player, I want keyboard-accessible settings and clickable menu controls, so that I can adjust the game conveniently.
42. As a player, I want opening settings to pause my run, so that I can make changes safely.
43. As a player, I want silent play if an audio device is unavailable, so that audio problems do not prevent playing.
44. As a player, I want invalid saved preferences to recover safely and save failures to be visible, so that storage problems do not crash the game or silently mislead me.
45. As a maintainer, I want separate platform builds and packaged smoke checks, so that missing dependencies are caught before downloads reach players.
46. As a maintainer, I want automated results distinguished from human playtests, so that platform support claims reflect the evidence.

## Implementation Decisions

- Use Python with pygame-ce for the desktop application and PyInstaller for standalone packaging. The game has no runtime service, account, or network dependency.
- Keep the game-rules model independent of graphics and audio. It owns the board, snake, food, score, direction queue, collisions, speed, and win condition.
- The board contains 576 cells. The snake starts four cells long. Each food adds one cell and 10 points; the maximum score for a completed run is 5,720.
- Place exactly one food in a randomly selected empty cell. When no empty cells remain after eating, end the run as a win instead of attempting to place another food.
- Start at 6 cells per second, add 0.5 after each five foods, and cap at 12. These values are the agreed initial tuning and can be revisited after playtesting.
- Buffer at most two valid direction changes. Validate each input against the last queued direction, or the current direction when the queue is empty. Ignore duplicates, reversals, repeated key events, and excess inputs beyond the queue limit.
- A move into the current tail cell is legal when the tail moves away during that same step. A wall or non-vacating body collision ends the run.
- Separate the fixed-step simulation clock from rendering. Interpolate positions between grid states for smooth animation; grid state remains authoritative for turns and collisions.
- The application coordinates title, active play, pause, resume countdown, and end-of-run states. Clear queued turns on pause. Allow intentional new turns during countdown and do not apply countdown time to simulation.
- Pause on focus loss, settings access, active-play fullscreen changes, and frame stalls longer than a quarter second. Resume only with focus and an explicit resume action, followed by a three-second countdown.
- Preserve the complete board when resizing or switching fullscreen; scale the presentation proportionally with letterboxing where needed. Fit the initial window to the available desktop.
- Draw the rounded snake, food, board, menus, glow, and particles in code. Reduced effects disables glow, particles, and pulsing; it does not change game rules or speed.
- Generate original electronic music and event sounds in memory. Loop the music quietly by default, offer separate volume controls, and permit silent play if audio initialization fails.
- Persist the best score and preferences in per-user application storage using validated values and atomic replacement. Invalid saves fall back to defaults; save failures display a message without ending play.
- Use GitHub Actions in the existing repository for separate Windows x64, Linux x64, macOS ARM64, and macOS Intel builds. Retain local markdown as the issue tracker.
- Build on each target operating system, smoke-test the packaged executable, and produce downloadable archives with their required runtime dependencies.

## Testing Decisions

- Prefer the existing application boundary: send keyboard and focus events, advance controlled time, and assert observable run transitions, score, pause behavior, rendering success, and persistence. Extend this boundary rather than introduce new test-only architecture.
- Retain focused tests at the existing game-rules boundary for cases that are impractical to reach through long play sessions: all wall directions, body collision, the vacating tail, growth, rapid queued turns, speed thresholds and cap, food placement, and a full-board win.
- Retain focused storage-boundary tests for restart persistence, malformed preferences, invalid values, and unwritable locations. Use isolated temporary saves rather than player data.
- Exercise the packaged application on every target with its existing smoke-test entry point. Verify launch, a scored food, pause/resume, collision, restart, saved best score, and rendered screens. Successful source tests alone do not validate a standalone archive.
- Test external behavior and meaningful outcomes. Avoid tests that merely reproduce implementation steps or assert incidental internal layout. Existing event-driven application tests, deterministic rules tests, save-recovery tests, and packaged smoke checks provide the prior art.
- Render the title, play, pause, countdown, end-of-run, and settings states, including a resized view. Use visual inspection for legibility and layout; successful rendering alone does not establish visual quality.
- Human playtesting must assess responsiveness, animation, music and sound, volume controls, reduced effects, focus changes, window resizing, fullscreen behavior, restart flow, and persistence on each platform. Dummy audio/video checks cannot validate real device experience.
- Do not claim a target is fully playtested solely because its automated build succeeds. Record the specific evidence and any untested checklist items.

## Out of Scope

- Power-ups, additional obstacles, alternate boards, extra game modes, and multiplayer.
- Gamepad, touch, mobile, and browser support for this release.
- Accounts, cloud saves, online leaderboards, monetization, and server infrastructure.
- Additional Linux architectures or a compatibility claim for every distribution or older operating system.
- An installer wizard or automatic updater; the agreed delivery is a standalone extracted application.
- Public release signing and notarization credentials, which have not been arranged. Current Windows builds are unsigned and current Mac builds are not notarized.
- Rebuilding already delivered features solely because this retrospective specification is being written.

## Further Notes

The first implementation is already delivered on the feature branch. All four platform builds passed the existing 19 automated tests and packaged smoke checks in the recorded GitHub Actions run. The user reported that it works great on Windows 11; this is successful general playtest feedback, not confirmation of every checklist item.

Human playtesting on both Mac architectures and Linux remains outstanding. Exact minimum OS compatibility beyond the build/test environments has not been established. The initial Linux build environment is Ubuntu 22.04, and the Mac build environments are macOS 15.

The main remaining release work is real-device validation on the outstanding targets and any fixes that validation reveals. Requirements here distinguish those remaining checks from features already implemented.
