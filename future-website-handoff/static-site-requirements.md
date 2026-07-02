# Static Site Requirements

Requirements and constraints for the eventual GitHub Pages website. Non-binding on implementation details, binding on outcomes.

## Hosting

- Must run as a **static site on GitHub Pages** (no server-side runtime).
- Keep dependencies light; prefer plain static HTML/CSS/JS or a lightweight static generator.
- All interactivity (quizzes, search) must work client-side.

## Must-have pages

1. **Home** — project intro plus searchable/browsable cards (from `summary.md`).
2. **Animals index** (001–050) and **Birds index** (051–100) — cards ordered by number.
3. **Species page** per book — full `book.md` with a table of contents, plus that book's glossary, quiz, and references.
4. **Master glossary** — all terms aggregated, alphabetized, linking back to source books.
5. **Quiz index** — all quizzes, each rendered interactively with a hidden answer key.
6. **About** — adapted from `README.md` / `project-blueprint.md`.

## Content integrity

- Preserve all folder numbers, slugs, and filenames; use them for stable URLs.
- Do not rewrite scientific content unless explicitly asked.
- Keep citation "to verify" flags visible to readers.
- Maintain the animals/birds split and the 001–100 ordering everywhere.

## UX

- Readable typography optimized for long-form study content.
- Per-page table of contents from the 20 sections.
- Client-side search over the catalog (name, scientific name, category, hook).
- Mobile-friendly, accessible (semantic HTML, keyboard navigable, sufficient contrast).

## Quiz behavior

- Render 10 MCQs per quiz; reveal correct answers only after the reader submits or opts to reveal.
- Optionally show a score; do not require accounts or storage.

## Out of scope for the website stage

- Authoring new book content.
- Changing the species list or numbering.
- Adding claims or citations not present in the source Markdown.
