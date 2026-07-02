# HTML Conversion Notes

Guidance for converting the Markdown books to static HTML at the website stage.

## General

- Source is CommonMark-style Markdown. A standard Markdown→HTML converter is sufficient.
- Do not alter wording during conversion. Structure and text are authored deliberately.
- Every `book.md` uses one H1 title line and 20 numbered section headings. Preserve these as `<h1>`/`<h2>` with stable `id` attributes so each section is individually linkable and a table of contents can be auto-generated.

## Per-file handling

- **book.md** → one full HTML page. Auto-build an in-page table of contents from the 20 section headings. Keep the "Myth / Scientific reality" blocks visually distinct.
- **summary.md** → strip to plain text/HTML for card teasers; keep it short.
- **glossary.md** → render as a definition list (`<dl>`); also contribute terms to the master glossary with a back-link to the source book.
- **quiz.md** → parse into structured questions and options; render the answer key collapsed/hidden until the reader submits or reveals.
- **references.md** → render as a list; keep any "Further reading to verify before final publication." flag visible (e.g. as a small badge), do not silently drop it.

## Parsing conventions to rely on

- Section headings in `book.md` are numbered `1.`–`20.` and named exactly as in `writing-template.md`.
- Quiz questions are numbered `1`–`10`, each with options `A`–`D`, followed by an "Answer Key" block.
- Glossary entries are `**Term** — definition` lines.

## Accessibility and portability

- Emit semantic HTML (headings, lists, `<dl>`), not div soup.
- Keep pages usable without JavaScript; use JS only to enhance (quiz interactivity, search, TOC).
- Keep asset footprint small for GitHub Pages.
