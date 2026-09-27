# Release verification

Automated tests and packaged smoke tests cover rules, rendering, input events and saves. Real device playtests are required before calling a target release tested.

| Target | Automated packaged test | Human playtest |
| --- | --- | --- |
| Windows x64 | Passed locally on Windows 11, Python 3.13.5 | Pending |
| macOS Apple Silicon | Pending GitHub Actions | Pending |
| macOS Intel | Pending GitHub Actions | Pending |
| Linux x64 / Ubuntu | Pending GitHub Actions | Pending |

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
