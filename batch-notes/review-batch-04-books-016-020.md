# Review — Batch 04, Books 016–020

Reviewer: Senior Ethology Reviewer / Scientific Editor
Verification level: LIGHT (established biological knowledge; no web search)
Date: 2026-07-02

## 1. Batch Reviewed

| Book No. | Species | Scientific Name | Folder |
|---|---|---|---|
| 016 | Domestic Cat | *Felis catus* | animals/016-domestic-cat |
| 017 | Horse | *Equus caballus* | animals/017-horse |
| 018 | Cattle | *Bos taurus* | animals/018-cow |
| 019 | Pig | *Sus domesticus* | animals/019-pig |
| 020 | Goat | *Capra hircus* | animals/020-goat |

All five folders contain the full set: book.md, summary.md, glossary.md, quiz.md, references.md. Every book has the required 20 ordered sections, a correct title line, and folder/number/species agreement. This is a strong, consistent batch: the writing is species-accurate, anthropomorphism is well controlled, livestock welfare claims are stated cautiously with debated points explicitly flagged, and no fabricated citations were found. Named researchers are real and correctly attributed.

## 2. Major Corrections Made

- **Book 016 (Domestic Cat) — file-integrity fix.** book.md contained a stray NUL (0x00) byte appended at the end of the file (byte position 25083), which caused tools to classify the otherwise-UTF-8 file as binary and would have risked breaking downstream publishing/rendering. The trailing null byte was stripped and a clean terminating newline ensured. Content was unaffected; the file is now valid UTF-8. No other file in the batch had null bytes (all rescanned; clean).

No other major (content-level) corrections were required. The scientific substance of all five books was sound.

## 3. Minor Corrections Made

- **Book 016 (Domestic Cat), Section 8 (Communication) — grammar.** "an adjusted signal that developing alongside human households" corrected to "an adjusted signal that developed alongside human households."

No other minor edits were needed. Glossaries (14–16 terms each) are relevant and clear; summaries fall within the 300–500 word target and are non-generic; quizzes are 10 MCQs with four options and one correct answer, and every answer key matches both the standalone quiz.md and the book's Section 19 (verified item by item). Myth-vs-reality sections are accurate and appropriately non-sentimental.

## 4. Scientific Claims Requiring Verification

All items below are already flagged in-book/in-references with the standard "Further reading to verify before final publication" marker; they are correctly presented as cautious. None are errors — they are specific empirical/citation claims that a light review cannot fully confirm without database access.

| Book No. | Species | Claim | Why It Needs Verification | Suggested Source Type |
|---|---|---|---|---|
| 016 | Domestic Cat | Cat domestication timing (~10,000 yrs, Near East, largely self-domestication via grain-store rodents) | Active archaeological/genetic field; dates and "self-domestication" framing are refined over time | Peer-reviewed genetics/archaeology (e.g. Driscoll et al. lineage work) |
| 016 | Domestic Cat | Slow-blink functions as affiliative signal and elicits reciprocal response from cats | Based on a small number of recent studies; effect robustness still developing | Peer-reviewed feline behavior journal |
| 016 | Domestic Cat | Meow largely redirected to humans (rare adult cat-to-cat) | Widely repeated but rests on limited formal study | Peer-reviewed bioacoustics/behavior |
| 016 | Domestic Cat | TNR effectiveness "remains debated among ecologists" | Genuinely contested; magnitude claims vary by study | Ecology/wildlife-management literature |
| 017 | Horse | DOM2 lineage arose on western Eurasian steppe, spread from ~4,200 yrs ago, replaced other populations (Orlando/Librado) | Active, evolving field; specific dates/geography still being refined | Ancient-DNA genetics (Orlando/Librado group) |
| 017 | Horse | EquiFACS validated and linked to pain/emotional state | Real tool; exact validation studies need confirming | Peer-reviewed equine welfare/FACS papers |
| 017 | Horse | ~350° field of view; dichromatic (blue/yellow) vision | Standard figures but exact degrees vary by source | Equine vision physiology literature |
| 017 | Horse | Leadership is shared/fluid; no permanent despotic "lead mare" | Correct current consensus but specific collective-movement studies should be cited | Behavioral ecology (feral horse studies) |
| 018 | Cattle | "Eureka"/learning-related excitement in heifers (attributed to Hagen & Broom) | Real study; exact authors/year/journal to confirm | Applied animal behaviour science journal |
| 018 | Cattle | Domestic cattle from a small founding aurochs population (~10,000 yrs, Near East) | Genetic estimate; founder-size figures debated | Cattle genomics/archaeology |
| 018 | Cattle | Last wild aurochs died 1627 in Poland (Jaktorów) | Well-established historically; date is safe but worth a source note | Historical/zoological reference |
| 018 | Cattle | Cattle recognize "dozens" of individual faces; social licking directed to preferred partners | Supported but specific quantitative claims need citing | Peer-reviewed cattle behavior studies |
| 019 | Pig | Joystick/cursor task (Curtis, Croney, colleagues) | Real study; confirm exact citation details | Applied animal behaviour science |
| 019 | Pig | Mirror food-finding task (Broom and colleagues) — information-use, not mark test | Real study; correctly distinguished from self-recognition; confirm article | Animal Behaviour / Broom group |
| 019 | Pig | Tactical use of social information in foraging (Held and colleagues) | Real research program; confirm specific studies | Applied ethology literature |
| 019 | Pig | "Thinking Pigs" review (Marino & Colvin) placing pig cognition alongside dogs | Real review; confirm title/journal/year | Int. Journal of Comparative Psychology (verify) |
| 019 | Pig | Independent domestication in Near East and East Asia (~9,000–10,000 yrs); rapid feralization | Active genetics field | Pig genomics/archaeology |
| 020 | Goat | Lever-and-cup task learned by trial-and-error, retained many months (McElligott et al.) | Real study; confirm citation details | Frontiers in Zoology / McElligott group |
| 020 | Goat | Human-directed / audience-directed gaze when task unsolvable (Nawroth, McElligott) | Real study; confirm citation | Biology Letters (verify) |
| 020 | Goat | Vocal plasticity / group "accents" among goats raised together | Real finding; confirm study details | Animal Behaviour (verify) |
| 020 | Goat | Goat domestication ~10,000–11,000 yrs, bezoar goat (*Capra aegagrus*) progenitor | Active field; broad claim safe, specifics to confirm | Caprine genetics/archaeology |

## 5. Citation Status — per book

- **Book 016 (Cat):** references.md properly separates well-established sources (Bradshaw *Cat Sense*; Turner & Bateson *The Domestic Cat*; IUCN *Felis lybica*) from four "to verify" topic areas. No invented citations. Compliant. Book Section 20 mirrors references.md.
- **Book 017 (Horse):** Strong. Names safe sources (McDonnell *Equid Ethogram*; Waring *Horse Behavior*; IUCN *Equus przewalskii*; ADW; Alcock) and lists eight "to verify" items including DOM2. Explicit statement that nothing was invented. Compliant.
- **Book 018 (Cattle):** Safe sources (Grandin; Webster; Dawkins; ADW; general aurochs genetics field). "Eureka" study attributed to Hagen & Broom and flagged for verification. Compliant, no fabrication.
- **Book 019 (Pig):** Thorough. Real researchers (Marino & Colvin; Broom; Held; Curtis/Croney) named at the level of researcher + topic and flagged for detail verification; IUCN *Sus scrofa*; ADW. Eleven "to verify" items. Compliant.
- **Book 020 (Goat):** Real researchers (McElligott; Nawroth) plus FAO, IUCN *Capra aegagrus*, ADW, Alcock. Eleven "to verify" items. Compliant, no fabrication.

Overall citation posture across the batch is exemplary and consistent with the collection's policy of naming only safe sources and flagging specifics.

## 6. Publication Readiness Score

| Book No. | Species | Score | Reason |
|---|---|---|---|
| 016 | Domestic Cat | 5/5 | Excellent, accurate, well-controlled anthropomorphism; only a stray trailing NUL byte and one grammar slip, both fixed. Citations need routine verification. |
| 017 | Horse | 5/5 | Exemplary; nuanced dominance-vs-leadership treatment, cautious DOM2 handling, fully consistent files. No content edits needed. |
| 018 | Cattle | 5/5 | Strong applied-ethology framing (Grandin), correct aurochs facts, honest welfare treatment, consistent files. No edits needed. |
| 019 | Pig | 5/5 | Careful cognition claims (mirror food-use vs mark test correctly distinguished), real attributions, consistent files. No edits needed. |
| 020 | Goat | 5/5 | Thorough, species-accurate browser/social-learning treatment, myotonia and "eats anything" myths handled well, consistent files. No edits needed. |

## 7. Final Batch Verdict

Batch 04 is a high-quality, publication-ready-draft batch. All five books are ethologically accurate, species-correct, and free of anthropomorphic overreach or welfare over-claiming; debated points (TNR efficacy, Yellowstone-style ecosystem claims are absent here, cognition ceilings, DOM2 dating) are explicitly flagged rather than asserted. Structure is fully compliant (20 sections, correct titles, matching quizzes/answer keys, relevant glossaries, non-generic summaries). No fabricated citations were found; every specific empirical claim is already marked for verification.

Two edits were made: (1) stripped a corrupting trailing NUL byte from book 016's book.md (file-integrity fix), and (2) fixed one grammatical error in book 016. No other files required changes. The only outstanding work before final publication is the standard database verification of the flagged citations and empirical specifics listed in Section 4 — none of which are errors, and none of which block a publication-ready draft.
