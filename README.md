# 100 Ethology Books: 50 Animals + 50 Birds

A structured, publication-ready document library of 100 educational books about animal and bird behavior (ethology). Each book is written for students, teachers, animal lovers, and general readers who want compact, scientifically grounded public science education — not a children's encyclopedia and not academic jargon.

## What this repository is

This is a **document preparation repository**, not a website. All content is authored in Markdown and organized into numbered folders. A later stage (handled separately by Claude Code) will convert this material into a static GitHub Pages website. Until then, the goal is to write, organize, quality-check, and store the documents correctly.

## Repository layout

```text
100-ethology-books-documents/
├── README.md                     ← you are here
├── project-blueprint.md          ← full editorial and production plan
├── species-master-list.md        ← the confirmed 100-species list (001–100)
├── writing-template.md           ← the exact 20-section book structure
├── citation-policy.md            ← rules for honest, verifiable sourcing
├── quality-checklist.md          ← pre-publication QC gate for every book
├── batch-progress-tracker.md     ← live status table for all 100 books
│
├── animals/                      ← books 001–050 (one folder each)
│   └── NNN-slug/ { book.md, summary.md, glossary.md, quiz.md, references.md }
├── birds/                        ← books 051–100 (one folder each)
│   └── NNN-slug/ { book.md, summary.md, glossary.md, quiz.md, references.md }
│
├── batch-notes/                  ← one note per 5-book batch (01–20)
└── future-website-handoff/       ← instructions for the website build stage
```

## The five files in every species folder

| File | Purpose | Target size |
|---|---|---|
| `book.md` | Full 20-section educational book | 2,500–5,000 words |
| `summary.md` | Standalone short overview | 300–500 words |
| `glossary.md` | Key behavioral/biological terms | 10–20 terms |
| `quiz.md` | Multiple-choice quiz + answer key | 10 questions |
| `references.md` | Real sources or flagged suggestions | credible sources only |

## Production method

Work proceeds in **batches of five books**. After each batch, the author writes a batch note (`batch-notes/`) and updates `batch-progress-tracker.md`. Batch 1 covers books 001–005 (Wolf, African Elephant, Chimpanzee, Bonobo, Gorilla).

## Non-negotiable rules

1. Write real content, not placeholders or descriptions of content.
2. Never invent citations. Uncertain sources are flagged: *"Further reading to verify before final publication."*
3. Keep writing species-specific — avoid generic paragraphs recycled across books.
4. Correct myths calmly and scientifically; never mock readers.
5. Preserve folder numbering and filenames exactly (the website stage depends on them).

## Status

Batch 1 (books 001–005) drafted. See `batch-progress-tracker.md` for the live status of all 100 books.
