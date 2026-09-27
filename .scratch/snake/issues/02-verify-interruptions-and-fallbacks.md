# 02: Complete automated coverage of interruption and fallback behavior

**What to build:** Provide behavioral evidence that runs stay safe during interruptions, optional effects and audio fail gracefully, and winning leads to a clean restart. Extend existing application-level tests rather than introduce new test-only architecture.

**Blocked by:** None (can start immediately).

**Status:** resolved

**Spec coverage:** User stories 21, 25, 27–32, 36, 39, and 43; application-boundary testing decisions.

- [x] A frame stall longer than a quarter second pauses active play without catch-up movement or an unfair collision, exercising the actual frame-loop behavior.
- [x] Fullscreen transitions during active play pause the run; the test exercises the transition rather than the hidden-window early return. Real display behavior remains subject to human playtesting.
- [x] Focus loss during the resume countdown returns the run to pause without advancing the snake; focus restoration alone does not resume it.
- [x] Simulated audio-device initialization failure permits startup, a scored food, and continued play without an audio exception.
- [x] Reduced effects removes particles, glow, and pulsing while preserving movement, score, and speed; verify observable effects without brittle whole-screen pixel snapshots.
- [x] A full-board win reaches the application win presentation with final score and best score, then keyboard restart begins a fresh run while retaining the best score.
- [x] Countdown and win presentations have inspectable rendering evidence, supplementing existing title, play, pause, loss, and settings coverage.
- [x] Test saves remain isolated from player data, existing tests pass, and any failures discovered are fixed or explicitly recorded as follow-up defects.

## Comments

Invalid-save recovery belongs to ticket 01. These checks cover distinct behavior and can proceed independently. Automated audio/display substitutes cannot establish real-device experience.

Resolved: added application-boundary checks for the real frame loop, actual fullscreen transition calls with SDL's dummy display, countdown interruption, missing audio hardware, reduced visual effects, and full-board win/restart. Extended smoke evidence with countdown, reduced-effects and win images; countdown and win images were visually inspected. Full suite: 31 passed. Typechecking: passed and added to CI. Human platform tickets remain open.
