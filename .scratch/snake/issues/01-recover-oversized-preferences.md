# 01: Recover safely from oversized saved volume values

**What to build:** Allow the player to launch and play when saved music or sound-effect volume contains an extremely large numeric value. Apply safe preference recovery rather than crashing. A saved music value of ten to the power of four hundred currently reproduces an uncaught OverflowError at startup.

**Blocked by:** None (can start immediately).

**Status:** resolved

**Spec coverage:** User story 44; validated preferences and nonfatal recovery.

- [x] Oversized integer values for either volume setting cannot crash startup.
- [x] Invalid values recover to safe defaults or bounded values consistent with the existing preference policy; valid best score and other preferences remain intact.
- [x] The player can start a run after recovery and subsequently save and reload valid preferences.
- [x] Regression tests reproduce the original failure and verify recovery at the existing storage boundary, using isolated saves.
- [x] Existing malformed-save, invalid-value, and persistence tests continue to pass.

## Comments

Confirmed by an isolated reproduction during the spec comparison. This ticket does not change game rules or introduce a new settings format.

Resolved: positive and negative oversized values for both volume controls first failed with OverflowError, then passed after integer-safe validation. Storage tests verify save/reload and preserved preferences; an application test verifies playing and relaunching after recovery. Full suite: 31 passed. Typechecking: passed.
