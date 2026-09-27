# Release verification

Automated tests and packaged smoke tests cover rules, rendering, input events and saves. Real device playtests are required before calling a target release tested.

| Target | Automated packaged test | Human playtest |
| --- | --- | --- |
| Windows x64 | Passed locally on Windows 11 and in GitHub Actions | Successful user playtest on Windows 11 |
| macOS Apple Silicon | Passed in GitHub Actions on macOS 15 | Pending |
| macOS Intel | Passed in GitHub Actions on macOS 15 | Pending |
| Linux x64 / Ubuntu | Passed in GitHub Actions on Ubuntu 22.04 | Pending |

Automated evidence: [Desktop builds run 36327193743](https://github.com/overthetop/snake3/actions/runs/36327193743), game commit `d9e8d4f`, September 27, 2026. All four targets passed the 19 tests and the packaged smoke test; downloadable archives and rendered screenshots are attached to the run. The local Windows smoke test also initialized the real video/audio drivers in a hidden window.

Human feedback, September 27, 2026: the user reported "works great on win 11" after receiving the build above. This confirms a successful general Windows 11 playtest; hardware details and individual checklist results were not reported. Human testing on macOS and Linux remains pending.

For each archive, record the commit, OS version, hardware, tester and date:

- Extract and launch without a system Python installation.
- Play several runs using both arrow keys and WASD. Try rapid corner pairs and reverse-direction input.
- Confirm food grows the snake, increments score by 10, and raises speed every five foods. Judge fairness at the speed cap.
- Check smooth motion, readable food/body/walls, and no distracting effects.
- Check eating/collision sounds and a complete music loop, including its seam. Confirm independent volume controls and silent playback at zero.
- Alt-tab while playing and during countdown; confirm automatic pause and safe resume.
- Resize to wide, square, and small windows. Toggle fullscreen and return. Confirm the whole board remains visible and menu hit targets align.
- Try reduced effects and verify particles/pulsing/glow disappear.
- Lose against walls and body, then restart with Enter. Confirm the score resets and best score remains.
- Quit and relaunch; verify best score and settings survive.
- Confirm a full-board win using an automated rules test; do not require a human to fill all 576 cells.

Signing/notarization is a separate distribution step; this project does not include private signing credentials.

## Follow-up automated validation

Tickets 01–02 add oversized-preference recovery and targeted application checks for interruptions, fullscreen transitions, missing audio devices, reduced effects, and full-board win/restart. The local suite now passes 31 tests, and typechecking passes for all six application modules. The smoke test now also emits countdown, reduced-effects, and win screenshots. These results do not replace the real-device observations requested in tickets 03–06, which are ready for human testers.
