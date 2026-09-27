# 03: Complete the Windows 11 playtest checklist

**What to build:** Complete and record the remaining real-device Windows 11 validation for the standalone download. Preserve the user's successful general playtest report without treating it as evidence for unreported checklist items.

**Blocked by:** None (can start immediately).

**Status:** ready-for-human

**Execution requirement:** A human tester with a Windows 11 x64 machine. An agent can prepare the checklist and consolidate evidence; completion requires actual reported observations.

**Spec coverage:** Windows delivery and human validation of input, presentation, audio, interruptions, display behavior, and persistence.

- [ ] Record the tested archive/build identifier, OS version, hardware, tester, and date.
- [ ] Extract and launch the complete standalone download on a machine or clean environment without Python installed.
- [ ] Exercise arrow keys and WASD, rapid corner pairs, ignored reversals, eating, scoring, speed increases, wall/body losses, and immediate restart; assess responsiveness and fairness near the speed cap.
- [ ] Listen through a complete music loop and event sounds; confirm music/effects adjust independently and each is silent at zero.
- [ ] Verify reduced effects, readable food/body/walls, and smooth motion.
- [ ] Verify pause/resume, switching away during play and countdown, resizable windows, fullscreen transitions, and correctly aligned menu clicks after resizing.
- [ ] Quit and relaunch to confirm best score and preferences survive.
- [ ] Record pass/fail/not-tested for each check; leave unavailable checks explicitly pending and capture reproducible defects.
- [ ] Repeat affected checks after relevant fixes and distinguish observed results from automated build evidence.

## Comments

The user already reported that the game works great on Windows 11. This ticket fills the evidence gaps; it does not invalidate that report or require rebuilding completed features. Existing archives are sufficient to begin.
