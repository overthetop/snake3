# 06: Validate the Linux x64 download on Ubuntu

**What to build:** Establish real-desktop evidence that the standalone Linux x64 download launches and delivers the agreed gameplay experience on Ubuntu.

**Blocked by:** None (can start immediately).

**Status:** ready-for-human

**Execution requirement:** A human tester with an Ubuntu x64 graphical desktop and real audio output. Headless CI is not a substitute.

**Spec coverage:** Linux delivery and the cross-platform human playtest requirement.

- [ ] Record the archive/build identifier, Ubuntu version, hardware, desktop/display session, tester, and date; begin with the Ubuntu 22.04 build baseline or explicitly record a different tested version.
- [ ] Extract the archive and launch its executable without relying on a separately installed Python. Verify executable permissions and record any missing runtime-library or desktop requirements.
- [ ] Play with arrow keys and WASD; verify rapid corners, ignored reversals, eating/growth/score, increasing speed, collision losses, and restart. Assess responsiveness and fairness near the speed cap.
- [ ] Inspect smooth motion, readable neon visuals, reduced effects, and the title, play, pause, countdown, loss, and settings screens.
- [ ] Verify real audio output, a complete music loop, event sounds, independent volume controls, and zero-volume behavior.
- [ ] Verify focus loss during play/countdown, explicit safe resume, window resizing, fullscreen transitions, and menu hit alignment.
- [ ] Quit and relaunch to verify best score and preferences persist in the user's application data location.
- [ ] Record pass/fail/not-tested per check and reproduce failures; leave unavailable observations pending.
- [ ] Repeat affected checks after relevant fixes; avoid extending compatibility claims to untested distributions or display sessions.

## Comments

The Linux build already passed automated tests and packaged smoke checks on Ubuntu 22.04. Existing downloads allow independent testing. No additional distribution support is requested by this ticket.
