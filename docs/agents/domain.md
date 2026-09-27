# Domain Docs

## Layout

This repo uses a single-context layout:

- `CONTEXT.md` at the repo root: domain vocabulary and context.
- `docs/adr/`: architectural decision records.

## Before exploring

Read `CONTEXT.md` and ADRs relevant to the area being explored.

If these files do not exist, proceed silently. Do not flag their
absence or suggest creating them upfront. The domain-modeling
skill, reached through grill-with-docs and
improve-codebase-architecture, creates them lazily as domain
terms and decisions are resolved.

## Use the glossary's vocabulary

Use terms defined in `CONTEXT.md` when naming domain concepts
in issues, proposals, hypotheses, and tests. Avoid synonyms the
glossary explicitly excludes.

If a needed concept is absent, reconsider whether it belongs
to the domain or note the gap for domain-modeling.

## Flag ADR conflicts

Explicitly identify any proposal that contradicts an existing
ADR, citing the ADR and explaining why it should be revisited.
