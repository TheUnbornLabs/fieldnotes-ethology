# Catalog Data Plan

A plan for the machine-readable catalog the website stage should generate from this repository. Nothing here needs to be built now; this documents the intended data model.

## Purpose

A single `catalog.json` (plus derived indexes) lets the site render cards, category pages, search, a master glossary, and a quiz index without re-parsing every Markdown file at request time.

## Book record

One object per species, ordered by `number`:

```json
{
  "number": 1,
  "slug": "001-wolf",
  "category": "animal",
  "commonName": "Gray Wolf",
  "scientificName": "Canis lupus",
  "hook": "Cooperative pack predator; a model for social carnivore behavior.",
  "paths": {
    "book": "animals/001-wolf/book.md",
    "summary": "animals/001-wolf/summary.md",
    "glossary": "animals/001-wolf/glossary.md",
    "quiz": "animals/001-wolf/quiz.md",
    "references": "animals/001-wolf/references.md"
  },
  "summaryText": "…first ~300 words…",
  "glossaryTermCount": 15,
  "quizQuestionCount": 10,
  "referencesNeedVerification": true
}
```

Source of truth for `number`, `slug`, `category`, `commonName`, `scientificName`, and `hook` is `species-master-list.md`.

## Derived indexes

- **glossary-index.json** — every term across all books: `{ term, definition, bookNumber, slug }`, alphabetized, for the master glossary page and cross-linking.
- **quiz-manifest.json** — `{ bookNumber, slug, questionCount, path }` for the quiz index page.
- **references-flags.json** — books whose `references.md` still contains "to verify" entries, to drive an editorial dashboard.

## Generation approach

- Parse `species-master-list.md` for the 100 base records.
- For each species folder, read the five files to fill counts, summary text, and the verification flag.
- Emit `catalog.json` and the derived indexes at build time.
- Regenerate whenever content changes; do not hand-edit the JSON.
