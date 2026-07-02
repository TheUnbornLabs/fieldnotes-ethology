# Review — Batch 09, Books 041–045

**Reviewer:** Senior Ethology Reviewer / Scientific Editor
**Verification level:** LIGHT (established biological knowledge; no web search)
**Date:** 2026-07-02

---

## 1. Batch Reviewed

| No. | Species | Folder | Files reviewed |
|-----|---------|--------|----------------|
| 041 | Dragonfly (Anisoptera / Odonata) | animals\041-dragonfly | book, summary, glossary, quiz, references |
| 042 | Monarch butterfly (*Danaus plexippus*) | animals\042-monarch-butterfly | book, summary, glossary, quiz, references |
| 043 | Jumping spider (Salticidae) | animals\043-jumping-spider | book, summary, glossary, quiz, references |
| 044 | Emperor scorpion (*Pandinus imperator*) | animals\044-emperor-scorpion | book, summary, glossary, quiz, references |
| 045 | Fiddler crab (Ocypodidae; *Uca* s.l.) | animals\045-fiddler-crab | book, summary, glossary, quiz, references |

Overall this is a strong batch. Ethological content is accurate and appropriately cautious across all five books; anthropomorphism is well controlled; the "confident vs cautious" register is handled unusually well (dragonfly internal-model claims, *Portia* cognition, scorpion fluorescence uncertainty, monarch innate navigation). No AI-slop, no placeholders, no fabricated citations. The problems found were mechanical, concentrated in the quiz answer keys and one missing answer-key section.

---

## 2. Major Corrections Made

- **042 Monarch — uniform answer key (book.md + quiz.md).** The quiz answer key was 9 of 10 correct answers on option "B" (key: B,B,A,C,B,B,B,B,B,B). All answers were factually correct but the distribution violated the anti-uniform-key rule. I reordered the option lists for Q2, Q6, Q7, Q9, Q10 in **both** book.md and quiz.md (keeping content identical, only shuffling which letter holds the correct answer) so the key is now **B,D,A,C,B,A,C,B,D,C** (A×2, B×3, C×3, D×2). book.md and quiz.md are now mutually consistent, and quiz.md was upgraded to include one-line answer rationales matching the collection style.

- **043 Jumping spider — missing answer key + book/quiz mismatch.** book.md Section 19 had NO "## Answer Key" block at all (a structural gap versus the benchmark and the rest of the batch), and its quiz options were ordered so that the intended key was all "B." The companion quiz.md had already been given a correctly redistributed key (B,A,C,D,B,C,D,B,B,C) but with reordered options, so the two files disagreed. I brought book.md into sync with quiz.md: reordered options for Q2, Q3, Q4, Q6, Q7, Q10 and **added the missing Answer Key** (B,A,C,D,B,C,D,B,B,C) with rationales. All ten answers verified correct against the book text.

## 3. Minor Corrections Made

- **045 Fiddler crab — stray Markdown code fence.** Removed an orphan closing ```` ``` ```` on the final line of book.md (after the references list), which was not opening any block and would render as stray text.
- Verified 041 answer key (B,C,C,B,B,C,B,B,B,C): all correct. Distribution is B-heavy (6 of 10) but every answer is genuinely correct and options are content-appropriate; left as-is (within tolerance, not a uniform key). 041 quiz.md matches book.md.
- Verified 044 answer key (B,B,C,B,C,B,A,C,B,B): correct and adequately varied; book.md and quiz.md consistent. No change.
- Confirmed all five books: correct title line, exactly 20 ordered numbered sections, consistent heading style, folder/number/species alignment, no placeholders, glossaries of 16 terms each (within 10–20), summaries within 300–500 words and non-generic.

## 4. Scientific Claims Requiring Verification

| Book No. | Species | Claim | Why It Needs Verification | Suggested Source Type |
|----------|---------|-------|---------------------------|------------------------|
| 041 | Dragonfly | Capture success "can exceed" most vertebrate predators / "more often than not" | Widely cited (~95% in Leonardo/Mischiati work) but exact figure is species- and study-specific; book already hedges | Peer-reviewed *Nature*/*J. Exp. Biol.* interception studies |
| 041 | Dragonfly | Compound eye "up to ~30,000 ommatidia" | Correct order of magnitude for large aeshnids; confirm upper figure and species | Odonata morphology reference (Corbet) |
| 041 | Dragonfly | STMD selective-attention neurons (Wiederman & O'Carroll) | Attribution correct; confirm specific paper title/year | Primary neuroscience paper (Univ. Adelaide) |
| 041 | Dragonfly | *Pantala flavescens* "one of the longest known insect migrations" | Established but transoceanic-route/genetic-connectivity specifics debated | Peer-reviewed migration/population-genetics study |
| 042 | Monarch | Migratory monarch IUCN "threatened" status | Status has shifted recently; must be checked against live listing (book flags this) | IUCN Red List live entry |
| 042 | Monarch | Antennal circadian clocks essential to sun compass (Reppert) | Attribution sound; confirm exact paper | Primary paper (Reppert lab, *PLoS Biology*/*Science*) |
| 042 | Monarch | Light-dependent magnetic compass as "backup" | Real finding; mechanism (cryptochrome) still researched | Peer-reviewed magnetoreception study |
| 043 | Jumping spider | *Portia* detour route planning / trial-and-error mimicry | Attribution to Jackson & Cross correct and appropriately cautious; confirm specific experiments | Primary papers (Jackson & Cross) |
| 043 | Jumping spider | Salticidae ">6,000 species / ~600 genera / ~1 in 8 spiders" | Counts drift with taxonomy; verify against World Spider Catalog | World Spider Catalog (NHM Bern) |
| 043 | Jumping spider | *Maratus* "~100 described species" | Genus is being described rapidly; number is a moving target | Recent salticid taxonomy / WSC |
| 044 | Emperor scorpion | Cuticular fluorescence from beta-carboline; function debated | Compound identity and open-question framing correct; confirm compound and hypotheses | Scorpion biology literature (Polis, ed.) |
| 044 | Emperor scorpion | CITES Appendix II listing | Correct in principle; confirm current listing details | CITES Appendices (live) |
| 044 | Emperor scorpion | "Inverse relationship" pincer size vs venom potency | A real recognized tendency, NOT an absolute law; book hedges with "frequent/often" — keep hedged | Comparative venom/functional-morphology review |
| 045 | Fiddler crab | Endogenous tidal + circadian dual clocks, tidal colour-change in constant conditions | Classic result; confirm specific chronobiology citations | Chronobiology primary literature |
| 045 | Fiddler crab | Hood/pillar "sensory trap" exploiting escape reflex (Christy) | Attribution correct; confirm specific papers | Primary papers (J. Christy) |
| 045 | Fiddler crab | *Uca* split into *Leptuca*/*Austruca*/*Minuca*/*Gelasimus* etc. | Taxonomy genuinely revised (Shih et al.); confirm authoritative reference | Crustacean systematics revision |

All the above are standard "verify the exact citation/current status" flags, not errors. Every book already contains an explicit "To verify before publication" section with matching inline markers; no additional inline markers were required.

## 5. Citation Status — per book

- **041 Dragonfly:** No fabricated citations. Well-established sources (Corbet; Leonardo/Mischiati; Wiederman/O'Carroll; ADW; IUCN) named appropriately; specific papers correctly deferred to "to verify." **Clean.**
- **042 Monarch:** No fabrications. Reppert, Brower, Journey North, Xerces, IUCN named safely; all specific literature and the current IUCN listing correctly flagged. **Clean.**
- **043 Jumping spider:** No fabrications. Foelix, Herberstein, Maddison, Jackson & Cross, Elias, ADW, World Spider Catalog, IUCN named; specifics deferred. references.md also states the citation policy explicitly. **Clean.**
- **044 Emperor scorpion:** No fabrications. Polis (ed.), Alcock, ADW, IUCN/CITES named; fluorescence, maternal-care, venom-comparison, and listing specifics flagged. **Clean.**
- **045 Fiddler crab:** No fabrications. Christy, Zeil, Salmon, Alcock, ADW, IUCN named; synchrony, chronobiology, path-integration, regeneration, bioturbation, and *Uca* taxonomy specifics flagged. **Clean.**

## 6. Publication Readiness Score

| Book No. | Species | Score | Reason |
|----------|---------|-------|--------|
| 041 | Dragonfly | 5/5 | Accurate, well-structured, cautious about internal-model/intelligence claims; key correct and acceptably varied; no edits needed beyond verification flags |
| 042 | Monarch butterfly | 5/5 | Excellent content; uniform answer key corrected and redistributed in both files; now publication-ready pending citation verification |
| 043 | Jumping spider | 5/5 | Outstanding, careful handling of *Portia* cognition; missing answer key added and book/quiz synchronised; now complete |
| 044 | Emperor scorpion | 5/5 | Accurate, honest on mild venom and fluorescence uncertainty; key well distributed; no substantive edits needed |
| 045 | Fiddler crab | 5/5 | Strong on sexual selection, honest signalling, dual clocks; only a stray code fence removed |

## 7. Final Batch Verdict

A high-quality, publication-ready batch. All five books are scientifically accurate at LIGHT verification, free of anthropomorphism and AI-slop, structurally complete (title line, 20 sections, consistent headings, no placeholders), and free of fabricated citations. Corrections were mechanical: the monarch's uniform answer key was redistributed, the jumping spider's missing answer key was added and synchronised with its quiz file, and a stray fiddler-crab code fence was removed. Remaining items are routine citation/status verifications already flagged inside each book. Recommended tracker status: all five **Publication-ready draft**, contingent only on the standard pre-publication citation checks.
