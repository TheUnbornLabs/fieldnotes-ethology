# Review — Batch 08, Books 036–040

Reviewer: Senior Ethology Reviewer / Scientific Editor
Verification level: LIGHT (no web search; relies on established biological knowledge; uncertain claims flagged, not fabricated)
Date: 2026-07-02

## 1. Batch Reviewed

| Book No. | Species | Scientific name | Files reviewed |
|---|---|---|---|
| 036 | Axolotl | *Ambystoma mexicanum* | book, summary, glossary, quiz, references |
| 037 | Honeybee | *Apis mellifera* | book, summary, glossary, quiz, references |
| 038 | Ants | family Formicidae | book, summary, glossary, quiz, references |
| 039 | Termites | Isoptera, within Blattodea | book, summary, glossary, quiz, references |
| 040 | Praying Mantis | order Mantodea | book, summary, glossary, quiz, references |

Overall this is a strong batch. Ethological accuracy is high throughout, anthropomorphism is well controlled (no "ruler/leader" queen framing; self-organization and emergence consistently emphasized), the waggle dance and mantis stereopsis are stated confidently as the brief required, and sexual cannibalism is presented with the correct nuance (context-dependent, often overstated, lab-inflated). Structure is consistent (title line, 20 ordered sections, species/number/folder match). No placeholders or fabricated citations found. The main defects were mechanical, not scientific: two quiz answer keys were badly skewed toward a single letter.

## 2. Major Corrections Made

- **Book 037 (Honeybee) — quiz answer-key skew.** Original key was B,C,B,B,C,B,B,B,B,B (eight of ten answers "B"). Redistributed by reordering answer options in Q3, Q6, Q7, Q9 in **both** `book.md` (Section 19) and `quiz.md`. New key: B,C,A,B,C,D,A,B,C,B (A:2, B:4, C:3, D:1). All correct answers re-verified against book content after reordering.
- **Book 038 (Ants) — quiz answer-key skew.** Original key was 1-B,2-C,3-B,4-C,5-B,6-B,7-B,8-B,9-B,10-B (seven "B"). Reordered options in Q1, Q2, Q5, Q6, Q7, Q10 in **both** `book.md` (Section 19) and `quiz.md`. New key: 1-A,2-B,3-B,4-C,5-D,6-C,7-D,8-B,9-B,10-D (A:1, B:4, C:2, D:3). All correct answers re-verified against book content.

No major scientific errors were found requiring correction; the content was accurate as drafted.

## 3. Minor Corrections Made

- None beyond the answer-key reordering above. Spelling, headings, section numbering, glossary term counts (13–15 per book), and summary word counts (all within 300–500) were already compliant. No inline "Needs verification" markers were required inside the book text because the existing "To verify before publication" reference sections already isolate the uncertain claims appropriately.

Observations noted but deliberately **not** changed (stylistic, within tolerance):
- Books 038 and 039 use an inline answer-key format ("1-B, 2-C, ...") in `book.md`; the benchmark (001-wolf) uses a vertical list. This is a house-style variation, not an error; left as-is.
- Book 037 `book.md` has no standalone "Answer Key" block after Section 19 (the key lives in `quiz.md`). This differs from the benchmark but is internally consistent within this batch's convention; the quiz.md key is present and correct. Flagged for the series editor to standardize collection-wide if desired.

## 4. Scientific Claims Requiring Verification

| Book No. | Species | Claim | Why It Needs Verification | Suggested Source Type |
|---|---|---|---|---|
| 036 | Axolotl | Axolotls possess electroreception used to detect prey | Electroreception is well established in some amphibians/salamander larvae, but the strength of evidence specifically for *Ambystoma mexicanum* as a routine hunting sense is less firmly documented than the lateral line; stated a touch confidently | Peer-reviewed sensory-biology literature on *Ambystoma* / amphibian electroreception |
| 036 | Axolotl | Regeneration extends to "portions of heart and brain" | Limb, tail, spinal-cord and jaw regeneration are strongly documented; heart/brain-tissue regeneration is real but more limited and specialized than the phrasing may imply | Peer-reviewed regeneration reviews (blastema biology) |
| 037 | Honeybee | Cognition results: concept of "zero," same/different rules, string-pulling, ball-rolling | Individually published but specialized/recent; exact study attribution needed | Peer-reviewed cognition papers (already flagged in references.md) |
| 037 | Honeybee | Sublethal pesticide (neonicotinoid) effects on navigation/foraging | Active, sometimes contested research area; magnitude debated | Peer-reviewed toxicology/ecotoxicology reviews |
| 038 | Ants | Shortest-path selection (double-bridge) and Ant Colony Optimization lineage | Well-known but specific experimental/foundational citations must be confirmed, not invented | Primary experimental papers; ACO foundational literature |
| 038 | Ants | *Cataglyphis* path integration and step-counting ("odometer") | Well supported but specific claims (step integration) should be tied to the actual studies | Peer-reviewed desert-ant navigation papers |
| 039 | Termites | *Macrotermes* mound ventilation mechanism (tidal/pendulum vs older thermosiphon models) | Mechanism has been revised in the literature; current standing should be stated precisely | J. Scott Turner and successor ventilation studies |
| 039 | Termites | Phylogenetic placement of Isoptera within Blattodea; sister to *Cryptocercus* | Now mainstream consensus, but as a specific systematic claim it should cite the phylogenetic source | Molecular phylogenetics review |
| 040 | Praying Mantis | True stereoscopic (3-D) vision; motion-tuned; "insect 3-D glasses" (Nityananda, Read et al.) | Well supported — state confidently — but exact paper (title/year/journal, e.g. *Current Biology*) must be confirmed before citing | Primary vision-science papers |
| 040 | Praying Mantis | Orchid mantis (*Hymenopus coronatus*) as aggressive floral mimicry attracting pollinators | Supported by specific field studies; attribution needed | Peer-reviewed mimicry/behavioral-ecology papers |
| 040 | Praying Mantis | Cyclopean ultrasonic ear and bat-evasion diving | Well established for many mantises; confirm specific citations | Peer-reviewed neuroethology papers |

## 5. Citation Status — per book

- **036 Axolotl:** Clean. Well-established sources (IUCN Red List, AmphibiaWeb, Animal Diversity Web, standard herpetology texts) correctly separated from "to verify" items. No fabrication. References explicitly instruct not to invent editions/pages. Status: acceptable, pending routine verification.
- **037 Honeybee:** Strong. Named foundational works (von Frisch, *Dance Language*; Seeley, *Honeybee Democracy* and *The Wisdom of the Hive*; Winston, *Biology of the Honey Bee*) are genuine, appropriate, and safe to name. "To verify" section correctly isolates *Varroa*, pesticide, cognition, stop-signal, and haplodiploidy literature. No fabrication.
- **038 Ants:** Strong. Hölldobler & Wilson (*The Ants*, *The Superorganism*), Gordon (*Ant Encounters*), AntWiki, ADW, Alcock all real and appropriate. Ten specific empirical claims correctly deferred to verification. No fabrication.
- **039 Termites:** Strong. Turner (*The Extended Organism*) named specifically; Hölldobler & Wilson and a generic *Biology of Termites* volume flagged for edition confirmation (handled honestly). Eight items deferred to verification, including the phylogeny and mound-ventilation mechanism. No fabrication.
- **040 Praying Mantis:** Strong. Prete (ed.), *The Praying Mantids*; Nityananda/Read stereopsis work; Alcock; ADW — all genuine and appropriate. Four "to verify" items with explicit instruction to confirm title/year/journal. No fabrication.

## 6. Publication Readiness Score

| Book No. | Species | Score | Reason |
|---|---|---|---|
| 036 | Axolotl | 5/5 | Accurate, well-structured, neoteny and Critically Endangered status correct; balanced quiz key; two minor claims (electroreception, heart/brain regeneration) flagged only for routine citation verification |
| 037 | Honeybee | 5/5 | Waggle dance stated confidently, queen-as-reproductive-not-ruler handled well, self-organization emphasized; skewed quiz key fixed |
| 038 | Ants | 5/5 | Excellent on emergence/stigmergy, no top-down "ruler," termites correctly noted as non-haplodiploid eusocial; skewed quiz key fixed |
| 039 | Termites | 5/5 | Correctly Blattodea (not Hymenoptera), convergent eusociality, mound as self-organized ventilation structure not a "palace"; balanced quiz key |
| 040 | Praying Mantis | 5/5 | Sexual cannibalism given correct real-frequency/context nuance; stereopsis confident and correctly attributed; balanced quiz key |

All scores are contingent on the routine citation verification listed in Sections 4–5, which is the standard pre-publication step for the whole collection (tracker status "Drafted → Verified").

## 7. Final Batch Verdict

Batch 08 is one of the cleaner batches: scientifically sound, well-written, free of AI-slop padding and anthropomorphic overreach, and structurally compliant with the benchmark. The species-specific requirements were all met — axolotl neoteny and Critically Endangered wild status; confident waggle dance; ant pheromone trails and non-command division of labour; termites as Blattodea with convergent eusociality and self-organized mound-building; and mantis sexual cannibalism stated as context-dependent rather than universal. The only substantive editorial fixes were the two quiz answer-key redistributions (Books 037 and 038), now corrected in both `book.md` and `quiz.md` with all answers re-verified. No fabricated citations were found and none were introduced. All five books are publication-ready drafts pending the collection-wide citation-verification pass.
