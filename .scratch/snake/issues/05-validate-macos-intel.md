# 05: Validate the Intel Mac download

**What to build:** Establish real-device evidence that the standalone Intel build launches and delivers the agreed gameplay experience on an Intel Mac.

**Blocked by:** None (can start immediately).

**Status:** ready-for-human

**Execution requirement:** A human tester with an Intel Mac. Apple Silicon testing or a successful build alone cannot substitute for this target's observations.

**Spec coverage:** Intel Mac delivery and the cross-platform human playtest requirement.

- [ ] Record the archive/build identifier, macOS version, Intel hardware, tester, and date.
- [ ] Extract and launch the Intel application without relying on a separately installed Python; record any launch barriers and required user actions without claiming notarization.
- [ ] Play with arrow keys and WASD; verify rapid corners, ignored reversals, eating/growth/score, increasing speed, collision losses, and restart. Assess responsiveness and fairness near the speed cap.
- [ ] Inspect smooth motion, readable neon visuals, reduced effects, and the title, play, pause, countdown, loss, and settings screens.
- [ ] Verify real audio output, a complete music loop, event sounds, independent volume controls, and zero-volume behavior.
- [ ] Verify focus loss during play/countdown, explicit safe resume, window resizing, fullscreen transitions, and menu hit alignment.
- [ ] Quit and relaunch to verify best score and preferences persist.
- [ ] Record pass/fail/not-tested per check and reproduce any failures; keep unavailable observations pending.
- [ ] Repeat affected checks after relevant fixes and report support only for the actual tested environment.

## Comments

The Intel build already passed automated tests and packaged smoke checks. Existing downloads allow independent testing. Signing and notarization remain outside this spec.
