# 04: Validate the Apple Silicon Mac download

**What to build:** Establish real-device evidence that the standalone Apple Silicon build launches and delivers the agreed gameplay experience on a Mac.

**Blocked by:** None (can start immediately).

**Status:** ready-for-human

**Execution requirement:** A human tester with an Apple Silicon Mac. An agent can prepare and record the session; completion requires real-device observations.

**Spec coverage:** Apple Silicon delivery and the cross-platform human playtest requirement.

- [ ] Record the archive/build identifier, macOS version, hardware architecture, tester, and date.
- [ ] Extract and launch the ARM64 application without relying on a separately installed Python; record any launch barriers and required user actions without claiming notarization.
- [ ] Play with arrow keys and WASD; verify rapid corners, ignored reversals, eating/growth/score, increasing speed, collision losses, and restart. Assess responsiveness and fairness near the speed cap.
- [ ] Inspect smooth motion, readable neon visuals, reduced effects, and the title, play, pause, countdown, loss, and settings screens.
- [ ] Verify real audio output, a complete music loop, event sounds, independent volume controls, and zero-volume behavior.
- [ ] Verify focus loss during play/countdown, explicit safe resume, window resizing, fullscreen transitions, and menu hit alignment.
- [ ] Quit and relaunch to verify best score and preferences persist.
- [ ] Record pass/fail/not-tested per check and reproduce any failures; do not mark missing observations as passed.
- [ ] Repeat affected checks after relevant fixes and report support only for the actual tested environment.

## Comments

The ARM64 build already passed automated tests and packaged smoke checks. Existing downloads allow this session to start independently of other tickets. Signing and notarization remain outside this spec.
