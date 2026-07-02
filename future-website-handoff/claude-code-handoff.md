# Claude Code Handoff — Website Build Stage

This document is written for the later stage, when Claude Code turns this repository into a static GitHub Pages website. **Read this before building the site.**

## What this repository is

This is a **document preparation repository**, not a website. All book content is authored in **Markdown**. Nothing here is HTML yet. Your job at the website stage is to convert and present this content — not to rewrite it.

## Do-not-break rules

1. **Do not rewrite the scientific content** unless explicitly asked. Fix obvious typos only if instructed.
2. **Preserve folder numbering and filenames exactly.** `animals/001-wolf/book.md` must keep its number and slug; these drive URLs and ordering.
3. Keep the animals (001–050) / birds (051–100) split.
4. Keep the five-file contract per species: `book.md`, `summary.md`, `glossary.md`, `quiz.md`, `references.md`.

## How each file maps to the site

| Source file | Website use |
|---|---|
| `book.md` | One static HTML page per species (the full book). Convert Markdown → HTML; keep the 20-section structure and heading anchors for in-page navigation. |
| `summary.md` | Homepage and category-index **cards** (short teaser per species). |
| `glossary.md` | Feed a **master glossary page** aggregating terms across all books; also show per-book glossary on each species page. |
| `quiz.md` | Feed a **quiz index page**; render each quiz interactively, with the answer key hidden until submit. |
| `references.md` | Render as the **citation / further-reading section** on each species page. Preserve "to verify" flags visibly. |

## Suggested site structure

- Home: project intro + featured/searchable cards from `summary.md`.
- `/animals/` and `/birds/`: category index pages (cards, ordered by number).
- `/animals/001-wolf/`: species page built from `book.md` (+ its glossary, quiz, references).
- `/glossary/`: master glossary.
- `/quizzes/`: quiz index.
- `/about/`: adapt `README.md` and `project-blueprint.md`.

## Data the site can generate

- A **catalog / manifest** (JSON) of all 100 books: number, name, scientific name, category, slug, path, and one-line hook (from `species-master-list.md`).
- A **glossary index** merging all `glossary.md` terms with back-links to source books.
- A **quiz manifest** listing all quizzes for the quiz index.

## Technical suggestions (non-binding)

- A simple static generator (or a small custom script) is enough; the content is plain Markdown.
- Keep it dependency-light for GitHub Pages. Client-side search over the manifest JSON is sufficient.
- Preserve heading IDs so the 20 sections are individually linkable.
- Show the citation-verification flags to readers rather than hiding them.

## Companion handoff files

- `html-conversion-notes.md` — Markdown→HTML conversion specifics.
- `catalog-data-plan.md` — the manifest/JSON data model.
- `static-site-requirements.md` — hosting and structural requirements.
