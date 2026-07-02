# Review — Batch 12, Books 056–060 (Birds)

Reviewer: Senior Ethology Reviewer / Scientific Editor
Verification level: LIGHT (no web search; established biological knowledge; uncertain items flagged)
Date: 2026-07-02

## 1. Batch Reviewed

| No. | Species | Folder | Files checked |
|-----|---------|--------|---------------|
| 056 | Budgerigar (*Melopsittacus undulatus*) | birds/056-budgerigar | book, summary, glossary, quiz, references |
| 057 | Domestic / Rock Pigeon (*Columba livia*) | birds/057-domestic-pigeon | book, summary, glossary, quiz, references |
| 058 | Mourning Dove (*Zenaida macroura*) | birds/058-mourning-dove | book, summary, glossary, quiz, references |
| 059 | Barn Owl (*Tyto alba*) | birds/059-barn-owl | book, summary, glossary, quiz, references |
| 060 | Eurasian Eagle-Owl (*Bubo bubo*) | birds/060-eurasian-eagle-owl | book, summary, glossary, quiz, references |

All folders/numbers/species match the master list. All books carry a correct title line, 20 ordered sections, consistent headings, and no placeholders. Summaries are within the 300–500 word range and non-generic; glossaries carry 14–15 relevant terms that appear in each book; references separate well-established sources from those to verify and contain no fabricated citations.

Ethological content is strong across the batch. All the flagged species-specific requirements were already satisfied in the drafts: budgerigar flock/vocal-learning/contact-call biology; pigeon multi-cue homing (sun compass + magnetoreception + olfaction + landmarks + possible infrasound, presented as an integrated system with no single-mechanism overclaim) and an explicit, well-argued correction of the "stupid pigeon" myth; mourning-dove seasonal monogamy, biparental crop milk, and perch-coo; barn-owl asymmetric ears and sound-localisation hunting; and eagle-owl apex nocturnal predation, intraguild predation, and territoriality. No book treats birds as "instinct-only"; anthropomorphism is controlled and debated points (magnetoreception mechanism, nestling "negotiation," wolf-style role assignment analogues) are appropriately hedged. No AI-slop patterns found.

## 2. Major Corrections Made

The only substantive issue across the batch was **clustered/uniform quiz answer keys** — a publishing-quality defect flagged in the review scope. In four of the five books the correct answer sat on option B far too often. These were redistributed by **reordering answer options only (content preserved)**, and the changes were mirrored identically in both `book.md` (Section 19 + Answer Key) and `quiz.md`:

- **057 Pigeon** — key was B×5 (1B 2B 3B 4B 5C 6A 7B 8C 9B 10C). Reordered Q2, Q3, Q7, Q9. New key: 1-B 2-A 3-D 4-B 5-C 6-A 7-D 8-C 9-C 10-C (A×2 B×2 C×4 D×2).
- **058 Mourning Dove** — key was B×7 (1B 2C 3B 4C 5B 6B 7B 8B 9B 10C). Reordered Q3, Q5, Q6, Q7, Q9. New key: 1-B 2-C 3-A 4-C 5-A 6-D 7-D 8-B 9-C 10-C (A×2 B×2 C×4 D×2).
- **059 Barn Owl** — key was B×8 (1B 2C 3B 4B 5B 6B 7B 8B 9C 10B). Reordered Q1, Q3, Q4, Q6, Q7. New key: 1-A 2-C 3-D 4-A 5-B 6-C 7-D 8-B 9-C 10-B (A×2 B×3 C×3 D×2).
- **060 Eagle-Owl** — key was B×6 (1B 2D 3B 4A 5B 6C 7B 8B 9B 10B). Reordered Q3, Q5, Q7, Q8. New key: 1-B 2-D 3-A 4-A 5-C 6-C 7-D 8-C 9-B 10-B (A×2 B×3 C×3 D×2).

For every affected question, the correct-answer text was verified to still match the book's own explanation, and each still has exactly one correct option. Book.md and quiz.md are identical per book after the edits.

**056 Budgerigar** needed no quiz change — its key (B C B B B C D B D B) was already reasonably distributed and correct.

## 3. Minor Corrections Made

- **060 Eagle-Owl, Section 14:** the six myth blocks were enclosed in a single ```text fence (opened at Myth 1, closed only after Myth 6). Reformatted into six separate fenced blocks to match the per-myth convention used in Book 059 and the collection benchmark (Book 001). No wording changed.
- No other wording, factual, or structural edits were required; the prose in all five books met the quality benchmark (Book 001 wolf) for depth, tone, and scientific caution.

## 4. Scientific Claims Requiring Verification

| Book No. | Species | Claim | Why It Needs Verification | Suggested Source Type |
|----------|---------|-------|---------------------------|-----------------------|
| 056 | Budgerigar | First non-mammal shown to exhibit contagious yawning (Gallup et al.) | Real finding but exact authorship/title/journal/year not confirmed under LIGHT review | Peer-reviewed primary article (PubMed/Google Scholar) |
| 056 | Budgerigar | Females bias mate choice toward males that solve a puzzle-box foraging task | Widely reported but specific study details unconfirmed; a related budgerigar mate-choice retraction/controversy exists in the literature and should be checked | Primary article + any published corrigendum/replication |
| 056 | Budgerigar | UV/fluorescent crown-cheek plumage acts as a mate-choice signal | Real research area; specific study details need confirming | Peer-reviewed behavioural-ecology article |
| 057 | Pigeon | Trained pigeons detect abnormalities in medical images (pathology/mammography) at levels rivalling people | Real study exists but article-level details unverified; "rivals trained people on some tasks" should be checked for scope | Primary article (e.g., PLOS ONE) |
| 057 | Pigeon | Magnetoreception mechanism (magnetite/trigeminal vs cryptochrome) | Genuinely unresolved; text correctly presents as debated — verify current consensus wording | Review article in avian navigation |
| 057 | Pigeon | Pigeons may detect infrasound contributing to orientation | Hypothesis, not settled fact; text hedges appropriately | Primary/review article |
| 058 | Mourning Dove | Wing-whistle functions as an honest, automatic alarm signal | The landmark wing-whistle-as-alarm work is on the **crested pigeon** (*Ocyphaps lophotes*); direct demonstration in *Zenaida macroura* is weaker. References already flag this caveat — retain the flag | Primary articles (Magrath/Murray et al.) + dove-specific study |
| 058 | Mourning Dove | Most heavily hunted game bird in North America; harvest sustainable | Plausible and widely stated; specific harvest figures need current agency data | USFWS / state wildlife-agency reports |
| 059 | Barn Owl | "Arguably the most acute directional hearing measured in any animal" | Strong superlative; defensible from Konishi/Knudsen work but wording should be checked against source | Neuroethology primary literature |
| 059 | Barn Owl | Auditory space map, ITD/ILD processing, experience-dependent map calibration (Konishi, Knudsen) | Foundational and real; exact papers/details unverified under LIGHT review | Primary articles / review |
| 059 | Barn Owl | Nestling vocal "negotiation" over food (Roulin) | Real research programme; specific papers unverified | Primary articles (Roulin et al.) |
| 060 | Eagle-Owl | Captive individuals "have lived beyond 50 years" | High-end longevity figure; verify against a longevity database before publication | AnAge / zoo longevity records |
| 060 | Eagle-Owl | Regularly preys on other raptors/owls (intraguild predation) influencing where smaller raptors nest | Well-supported in principle; specific distributional-effect claim needs a source | Primary ecology article |

## 5. Citation Status — per book

- **056 Budgerigar:** references.md well structured; splits established sources (IUCN, Cornell) from studies to verify; all uncertain primary studies flagged; no fabrication. Status: acceptable, verification pending.
- **057 Pigeon:** references.md names real researchers (Walcott, Papi, Watanabe, Skinner) generally without inventing article-level detail; explicitly flags magnetoreception, medical-imaging, and infrasound work for verification. Status: acceptable, verification pending.
- **058 Mourning Dove:** references.md solid; notably honest about the wing-whistle alarm evidence (attributes related work to Magrath/Murray and flags whether it applies directly to *Zenaida macroura*). Status: acceptable, verification pending.
- **059 Barn Owl:** references.md exemplary; Konishi, Knudsen, Roulin named generally with all specific claims itemised for verification; no fabrication. Status: acceptable, verification pending.
- **060 Eagle-Owl:** references.md acceptable; relies on Cornell, IUCN, HBW, Alcock as established anchors and flags diet, intraguild-predation, reintroduction, and hearing studies for verification. Status: acceptable, verification pending.

No fabricated citations detected in any book. All conform to the collection's "well-established vs to-verify" citation policy.

## 6. Publication Readiness Score

| Book No. | Species | Score | Reason |
|----------|---------|-------|--------|
| 056 | Budgerigar | 5/5 | Accurate, well-structured, balanced quiz key, honest references; no edits needed. Pending only routine citation verification. |
| 057 | Pigeon | 5/5 | Strong multi-cue navigation and intelligence-myth correction; quiz key redistributed and consistent across files. |
| 058 | Mourning Dove | 5/5 | Accurate columbid biology; quiz key redistributed; references honestly flag the wing-whistle caveat. |
| 059 | Barn Owl | 5/5 | Excellent neuroethology treatment; quiz key redistributed; exemplary citation handling. |
| 060 | Eagle-Owl | 4/5 | Accurate and thorough; quiz key redistributed and myth blocks reformatted; docked one point pending the 50-year captive-longevity figure and the intraguild-distribution claim. |

## 7. Final Batch Verdict

A high-quality batch. All five books were already ethologically accurate, appropriately cautious, free of anthropomorphism and AI-slop, and structurally complete against the 20-section template and the Book 001 benchmark. The species-specific accuracy targets in scope (budgerigar vocal learning/flocking; pigeon multi-cue homing and intelligence rehabilitation; dove monogamy/crop milk/perch-coo; barn-owl asymmetric-ear sound localisation; eagle-owl apex/intraguild predation) were all met without correction.

The one systemic defect was clustered quiz answer keys (books 057–060 overweighted option B, up to 8/10 in Book 059). All four were redistributed by option reordering with content preserved and mirrored identically in book.md and quiz.md; Book 056 needed none. A minor myth-block formatting fix was applied to Book 060.

Remaining work is limited to routine citation verification (no fabricated sources exist) and confirming two quantitative/ecological claims in Book 060. Books 056–059 are publication-ready drafts; Book 060 is a publication-ready draft pending two verifications.
