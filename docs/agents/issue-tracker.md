# Issue tracker: Local Markdown

Issues and specs live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`.
- Specs: `.scratch/<feature-slug>/spec.md`.
- Tickets: `.scratch/<feature-slug>/issues/<NN>-<slug>.md`,
  numbered from 01, with one file per ticket.
- Record issue state in a `Status:` line near the top.
- Append conversation history under `## Comments`.

## Publishing and fetching

When publishing to the issue tracker, create the appropriate file
under `.scratch/<feature-slug>/`, creating directories as needed.

When fetching a ticket, read the referenced file. If given only a
number, locate it in the relevant feature's issues directory.

## Wayfinding operations

- Map: `.scratch/<effort>/map.md`, with Notes, Decisions-so-far,
  and Fog sections.
- Child ticket: `.scratch/<effort>/issues/NN-<slug>.md`,
  numbered from 01, with the question in the body.
- Type: a `Type:` line containing research, prototype, grilling,
  or task.
- State: a `Status:` line containing open, claimed, or resolved.
- Blocking: a `Blocked by: NN, NN` line. A ticket is unblocked
  when all listed tickets are resolved.
- Frontier: select open, unblocked, unclaimed tickets in
  numerical order.
- Claim: set `Status: claimed` and save before starting work.
- Resolve: append the answer under `## Answer`, set
  `Status: resolved`, then append a summary and ticket link
  to the map's Decisions-so-far section.
