# Project Blueprint — 100 Ethology Books

## 1. Mission

Produce 100 structured educational books about animal and bird behavior. The collection should give a curious reader a genuine grounding in ethology — the scientific study of behavior — through 100 well-chosen species, half mammals-and-other-animals, half birds.

The material must serve four audiences at once:

- **Students** who need clear, accurate, exam-useful explanations.
- **Teachers** who need ready-made lessons, glossaries, and quizzes.
- **Animal lovers** who want depth beyond popular myths.
- **General readers** who want compact science, not sentimentality.

## 2. Editorial voice

Write like a working ethologist explaining a species to an intelligent non-specialist. Serious, clear, public-friendly, and specific. Every claim should be the kind a field biologist or behavioral ecologist would accept. Avoid filler, motivational language, forced moral lessons, and heavy anthropomorphism. Use animal cognition and behavior terminology accurately, and define it in the glossary.

## 3. Scope and structure

- **100 books total**: 50 in `animals/` (001–050), 50 in `birds/` (051–100).
- Each book follows the fixed 20-section structure in `writing-template.md`.
- Each book ships with five files (book, summary, glossary, quiz, references).
- Folder names are zero-padded and slugged: `001-wolf`, `051-common-raven`.

## 4. Coverage goals

The animal set deliberately spans taxonomic and ecological diversity: mammals, reptiles, amphibians, fish, insects, arachnids, crustaceans and marine invertebrates; predators and prey; solitary and social; wild and domesticated; celebrated and neglected species. The bird set spans corvids, raptors, parrots, pigeons/doves, waterfowl, seabirds, songbirds, flightless birds, migratory and urban birds, nocturnal birds, colonial nesters, tool-users, and species with remarkable courtship or parenting. See `species-master-list.md`.

## 5. Production workflow

1. **Batch selection** — take the next five species in numeric order.
2. **Drafting** — for each species, create the folder and write all five files against the template.
3. **Self-QC** — run every file against `quality-checklist.md`.
4. **Batch note** — record completed books, scientific names, ethology focus, citations needing verification, and weak sections.
5. **Tracker update** — update `batch-progress-tracker.md`.
6. **Repeat** for the next batch.

Twenty batches of five books complete the collection.

## 6. Sourcing standard

Governed by `citation-policy.md`. Acceptable sources: peer-reviewed papers, university and museum sources, conservation organizations, government wildlife agencies, reputable field guides, and standard animal-behavior textbooks. No invented citations. Anything uncertain is explicitly flagged for verification before publication.

## 7. Quality bar

A book passes only when it is accurate, species-specific, appropriately sourced, complete across all 20 sections and five files, within length targets, and free of the failure modes listed in `quality-checklist.md` (generic AI phrasing, repetition, fake citations, overclaiming, moralizing).

## 8. Downstream use

This repository feeds a later static-website build. Content is authored so that summaries become homepage cards, glossaries feed a master glossary, quizzes feed a quiz index, and references feed citation sections. See `future-website-handoff/`. The website stage must not rewrite scientific content unless explicitly asked, and must preserve numbering and filenames.
