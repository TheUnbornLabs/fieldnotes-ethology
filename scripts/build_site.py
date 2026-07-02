#!/usr/bin/env python3
"""Static site generator for the 100 Ethology Books collection.

Reads the Markdown source (species-master-list.md + animals/ + birds/)
and generates a static site into docs/ for GitHub Pages.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
SITE_TITLE = "Fieldnotes in Ethology"
SITE_TAGLINE = "100 species, one behavior at a time — a public field guide to animal and bird behavior."
REPO_URL = "https://github.com/TheUnbornLabs/fieldnotes-ethology"

# ---------------------------------------------------------------------------
# Inline markdown -> HTML
# ---------------------------------------------------------------------------

def esc(text):
    return html.escape(text, quote=False)


def inline_md(text):
    """Convert a small subset of inline Markdown (bold, italic, code) to HTML.
    Input is raw markdown text (unescaped); output is safe HTML."""
    text = esc(text)
    # bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # inline code: `text`
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    # italic: *text* (single asterisk, not already consumed by bold)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


def strip_md(text):
    """Strip markdown emphasis markers, leaving plain text for JSON/search."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)(?<!\*)\*(?!\*)", r"\1", text)
    text = re.sub(r"`([^`]+?)`", r"\1", text)
    return text.strip()


def slugify_id(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s


# ---------------------------------------------------------------------------
# Species master list
# ---------------------------------------------------------------------------

def parse_master_list():
    path = ROOT / "species-master-list.md"
    text = path.read_text(encoding="utf-8")
    records = {}
    category = None
    for line in text.splitlines():
        if line.startswith("## Animals"):
            category = "animal"
            continue
        if line.startswith("## Birds"):
            category = "bird"
            continue
        m = re.match(r"\|\s*(\d{3})\s*\|\s*([\w.-]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", line)
        if not m:
            continue
        num, slug, common, sci, hook = m.groups()
        records[int(num)] = {
            "number": int(num),
            "slugHint": slug,
            "category": category,
            "commonName": strip_md(common),
            "scientificName": strip_md(sci),
            "hook": strip_md(hook),
        }
    return records


# ---------------------------------------------------------------------------
# book.md parsing / rendering
# ---------------------------------------------------------------------------

def render_book(md_text, species_title):
    """Parse book.md into a list of {id, num, title, html} sections."""
    lines = md_text.splitlines()
    # Drop the H1 title line (# Book NNN — ...)
    body_lines = [l for l in lines if not l.startswith("# ")]

    sections = []
    cur_title = None
    cur_num = None
    cur_lines = []

    def flush():
        if cur_title is None:
            return
        html_body = render_block(cur_lines)
        sec_id = f"section-{cur_num}" if cur_num else slugify_id(cur_title)
        sections.append({"id": sec_id, "num": cur_num, "title": cur_title, "html": html_body})

    for line in body_lines:
        m = re.match(r"^##\s+(\d+)\.\s+(.+)$", line)
        m2 = re.match(r"^##\s+(.+)$", line) if not m else None
        if m:
            flush()
            cur_num, cur_title = m.group(1), m.group(2).strip()
            cur_lines = []
        elif m2:
            flush()
            cur_num, cur_title = None, m2.group(1).strip()
            cur_lines = []
        else:
            cur_lines.append(line)
    flush()
    return sections


def render_block(lines):
    """Render a list of raw markdown lines (paragraphs + fenced blocks) to HTML."""
    out = []
    para = []
    in_fence = False
    fence_lines = []

    def flush_para():
        if para:
            text = " ".join(l.strip() for l in para if l.strip())
            if text:
                out.append(f"<p>{inline_md(text)}</p>")
            para.clear()

    for line in lines:
        if line.strip().startswith("```"):
            if not in_fence:
                flush_para()
                in_fence = True
                fence_lines = []
            else:
                out.append(render_fence(fence_lines))
                in_fence = False
            continue
        if in_fence:
            fence_lines.append(line)
            continue
        if not line.strip():
            flush_para()
            continue
        para.append(line)
    flush_para()
    return "\n".join(out)


def render_fence(fence_lines):
    text = "\n".join(fence_lines).strip("\n")
    myth_m = re.match(r"^Myth\s*\d*:?\s*(.+?)\nScientific reality:\s*(.+)$", text, re.S)
    if myth_m:
        myth_text, reality_text = myth_m.groups()
        return (
            '<div class="myth-block">'
            f'<p class="myth"><span class="tag tag-myth">Myth</span> {inline_md(myth_text.strip())}</p>'
            f'<p class="reality"><span class="tag tag-reality">Scientific reality</span> {inline_md(reality_text.strip())}</p>'
            "</div>"
        )
    return f"<pre>{esc(text)}</pre>"


def render_paragraphs(text):
    """Render a plain multi-paragraph markdown text block (summary.md body)."""
    paras = re.split(r"\n\s*\n", text.strip())
    return "\n".join(f"<p>{inline_md(p.strip())}</p>" for p in paras if p.strip())


# ---------------------------------------------------------------------------
# summary.md
# ---------------------------------------------------------------------------

def parse_summary(md_text):
    lines = md_text.splitlines()
    body_lines = [l for l in lines if not l.startswith("# ")]
    body = "\n".join(body_lines).strip()
    plain = strip_md(re.sub(r"\n+", " ", body))
    words = plain.split()
    teaser = " ".join(words[:45]) + ("…" if len(words) > 45 else "")
    return {"html": render_paragraphs(body), "plain": plain, "teaser": teaser}


# ---------------------------------------------------------------------------
# glossary.md
# ---------------------------------------------------------------------------

def parse_glossary(md_text):
    entries = []
    for line in md_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", line)
        if not m:
            continue
        term, rest = m.groups()
        term = term.rstrip(" :")
        rest = rest.strip()
        rest = re.sub(r"^[:—\-]\s*", "", rest)
        entries.append({"term": term, "definition": rest})
    return entries


# ---------------------------------------------------------------------------
# quiz.md
# ---------------------------------------------------------------------------

def extract_options(text):
    """Find the 4 A-D options in a question block, whichever style is used:
    multi-line ('A. text' / '- A. text' / 'A) text' on their own lines) or
    inline single-line ('a) text  b) text  c) text  d) text')."""
    opts = {}
    positions = []
    for om in re.finditer(r"(?m)^\s*(?:[-*]\s*)?([A-Da-d])[.)]\s+(.+)$", text):
        opts[om.group(1).upper()] = om.group(2).strip()
        positions.append(om.start())
    if len(opts) == 4:
        return opts, positions[0]

    opts, positions = {}, []
    for om in re.finditer(r"([A-Da-d])\)\s*(.*?)(?=\s{2,}[A-Da-d]\)|$)", text, re.S):
        letter, val = om.group(1).upper(), om.group(2).strip()
        if val:
            opts[letter] = val
            positions.append(om.start())
    if len(opts) == 4:
        return opts, positions[0]
    return {}, None


def parse_quiz(md_text):
    if "## Answer Key" in md_text:
        q_part, key_part = md_text.split("## Answer Key", 1)
    elif re.search(r"\*\*Answer Key", md_text):
        q_part, key_part = re.split(r"\*\*Answer Key[:\*]*", md_text, maxsplit=1)
    else:
        q_part, key_part = md_text, ""

    questions = []
    q_blocks = re.split(r"\n(?=\d+\.\s)", q_part.strip())
    for block in q_blocks:
        m = re.match(r"^(\d+)\.\s+(.*)$", block.strip(), re.S)
        if not m:
            continue
        qnum, rest = m.groups()
        opts, start = extract_options(rest)
        if not opts:
            continue
        stem = rest[:start].strip()
        stem = re.sub(r":\s*$", "", stem)
        questions.append({"num": int(qnum), "stem": stem, "options": opts})

    answers = {}
    for am in re.finditer(r"(\d{1,2})\s*[.\-:]\s*([A-Da-d])\b", key_part):
        answers[int(am.group(1))] = am.group(2).upper()

    return questions, answers


# ---------------------------------------------------------------------------
# references.md
# ---------------------------------------------------------------------------

def parse_references(md_text):
    lines = md_text.splitlines()
    sections = []
    cur_title = None
    cur_items = []

    def flush():
        if cur_title is not None:
            sections.append({"title": cur_title, "items": cur_items[:]})

    intro = []
    intro_items = []
    seen_heading = False
    for line in lines:
        if line.startswith("# "):
            continue
        m = re.match(r"^##\s+(.+)$", line)
        bold_m = re.match(r"^\*\*(.+?)\*\*$", line.strip())
        if m or bold_m:
            flush()
            cur_title = (m or bold_m).group(1).strip()
            cur_items = []
            seen_heading = True
            continue
        item_m = re.match(r"^-\s+(.+)$", line.strip())
        if item_m and seen_heading:
            cur_items.append(item_m.group(1).strip())
        elif item_m and not seen_heading:
            intro_items.append(item_m.group(1).strip())
        elif not seen_heading and line.strip():
            intro.append(line.strip())
    flush()

    needs_verification = "to verify" in md_text.lower()
    intro_html = render_paragraphs(" ".join(intro)) if intro else ""
    if intro_items:
        intro_html += "<ul>" + "".join(f"<li>{inline_md(it)}</li>" for it in intro_items) + "</ul>"
    return {"intro": intro_html, "sections": sections, "needsVerification": needs_verification}


# ---------------------------------------------------------------------------
# Page shell / templates
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Animals", "animals/index.html"),
    ("Birds", "birds/index.html"),
    ("Glossary", "glossary/index.html"),
    ("Quizzes", "quizzes/index.html"),
    ("About", "about/index.html"),
]


def page_shell(base, title, description, body_html, active=None, extra_head=""):
    nav = []
    for label, href in NAV_ITEMS:
        cls = ' class="active"' if label == active else ""
        nav.append(f'<a href="{base}{href}"{cls}>{label}</a>')
    nav_html = "\n      ".join(nav)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="{base}assets/style.css">
{extra_head}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{base}index.html">{esc(SITE_TITLE)}</a>
    <nav class="site-nav">
      {nav_html}
    </nav>
  </div>
</header>
<main id="main">
{body_html}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>{esc(SITE_TITLE)} — 100 species, editorially reviewed and citation-checked. Source and full citation notes on <a href="{REPO_URL}">GitHub</a>.</p>
  </div>
</footer>
<script src="{base}assets/site.js"></script>
</body>
</html>
"""


def card_html(base, rec, depth_prefix=""):
    href = f"{base}{rec['category']}s/{rec['slug']}/index.html"
    return f"""<a class="card" href="{href}">
  <span class="card-num">{rec['number']:03d}</span>
  <h3>{esc(rec['commonName'])}</h3>
  <p class="sci">{inline_md('*' + rec['scientificName'] + '*') if not rec['scientificName'].startswith('*') else inline_md(rec['scientificName'])}</p>
  <p class="hook">{esc(rec['hook'])}</p>
  <p class="teaser">{esc(rec['teaser'])}</p>
</a>"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def load_species():
    master = parse_master_list()
    species = []
    for cat_dir, category in (("animals", "animal"), ("birds", "bird")):
        for folder in sorted((ROOT / cat_dir).iterdir()):
            if not folder.is_dir():
                continue
            m = re.match(r"^(\d{3})-(.+)$", folder.name)
            if not m:
                continue
            number = int(m.group(1))
            meta = master.get(number, {})
            book_md = (folder / "book.md").read_text(encoding="utf-8")
            summary_md = (folder / "summary.md").read_text(encoding="utf-8")
            glossary_md = (folder / "glossary.md").read_text(encoding="utf-8")
            quiz_md = (folder / "quiz.md").read_text(encoding="utf-8")
            refs_md = (folder / "references.md").read_text(encoding="utf-8")

            title_m = re.search(r"^#\s+Book\s+\d+\s+—\s+(.+)$", book_md, re.M)
            book_title = title_m.group(1).strip() if title_m else meta.get("commonName", folder.name)

            summary = parse_summary(summary_md)
            glossary = parse_glossary(glossary_md)
            questions, answers = parse_quiz(quiz_md)
            references = parse_references(refs_md)
            sections = render_book(book_md, book_title)

            species.append({
                "number": number,
                "slug": folder.name,
                "category": category,
                "commonName": meta.get("commonName", folder.name),
                "scientificName": meta.get("scientificName", ""),
                "hook": meta.get("hook", ""),
                "bookTitle": book_title,
                "teaser": summary["teaser"],
                "summaryHtml": summary["html"],
                "summaryPlain": summary["plain"],
                "glossary": glossary,
                "questions": questions,
                "answers": answers,
                "references": references,
                "sections": sections,
                "referencesNeedVerification": references["needsVerification"],
            })
    species.sort(key=lambda r: r["number"])
    return species


def render_species_page(rec):
    base = "../../"
    toc_items = "\n".join(
        f'<li><a href="#{s["id"]}">{esc((s["num"] + ". " if s["num"] else "") + s["title"])}</a></li>'
        for s in rec["sections"]
    )
    sections_html = "\n".join(
        f'<section id="{s["id"]}"><h2>{esc((s["num"] + ". " if s["num"] else "") + s["title"])}</h2>\n{s["html"]}</section>'
        for s in rec["sections"]
    )

    glossary_html = "".join(
        f'<div class="gloss-entry"><dt>{esc(g["term"])}</dt><dd>{inline_md(g["definition"])}</dd></div>'
        for g in rec["glossary"]
    )

    quiz_html = render_quiz_widget(rec, f"quiz-{rec['slug']}")

    ref_html = ""
    if rec["references"]["intro"]:
        ref_html += rec["references"]["intro"]
    for sec in rec["references"]["sections"]:
        items = "".join(
            f'<li>{inline_md(it)}{" <span class=\"badge\">to verify</span>" if "to verify" in it.lower() else ""}</li>'
            for it in sec["items"]
        )
        ref_html += f'<h3>{esc(sec["title"])}</h3><ul>{items}</ul>'

    sci_html = inline_md(f"*{rec['scientificName']}*") if rec["scientificName"] and not rec["scientificName"].startswith("*") else inline_md(rec["scientificName"])

    body = f"""
<div class="wrap species-page">
  <nav class="breadcrumb"><a href="{base}index.html">Home</a> / <a href="{base}{rec['category']}s/index.html">{rec['category'].capitalize()}s</a> / {esc(rec['commonName'])}</nav>
  <header class="species-hero">
    <span class="card-num">{rec['number']:03d}</span>
    <h1>{esc(rec['bookTitle'])}</h1>
    <p class="sci">{sci_html}</p>
    <p class="hook">{esc(rec['hook'])}</p>
  </header>

  <div class="species-layout">
    <aside class="toc">
      <h2>Contents</h2>
      <ul>{toc_items}</ul>
      <ul class="toc-jump">
        <li><a href="#glossary">Glossary</a></li>
        <li><a href="#quiz">Quiz</a></li>
        <li><a href="#references">References</a></li>
      </ul>
    </aside>
    <article class="book-body">
      {sections_html}

      <section id="glossary">
        <h2>Glossary</h2>
        <dl class="glossary-list">{glossary_html}</dl>
      </section>

      <section id="quiz">
        <h2>Short Quiz</h2>
        {quiz_html}
      </section>

      <section id="references">
        <h2>References / Further Reading</h2>
        {ref_html}
      </section>
    </article>
  </div>
</div>
"""
    return page_shell(base, f"{rec['bookTitle']} — {SITE_TITLE}",
                       f"{rec['commonName']} ({rec['scientificName']}): {rec['hook']}", body)


def render_quiz_widget(rec, widget_id):
    q_html = []
    for q in rec["questions"]:
        opts = "".join(
            f'''<label class="quiz-opt">
                <input type="radio" name="{widget_id}-q{q['num']}" value="{letter}">
                <span>{letter}. {inline_md(text)}</span>
              </label>'''
            for letter, text in sorted(q["options"].items())
        )
        q_html.append(f'''<fieldset class="quiz-question" data-qnum="{q['num']}">
          <legend>{q['num']}. {inline_md(q['stem'])}</legend>
          {opts}
          <p class="quiz-feedback" hidden></p>
        </fieldset>''')
    answers_json = json.dumps(rec["answers"])
    return f'''<form class="quiz-widget" id="{widget_id}" data-answers='{answers_json}'>
      {"".join(q_html)}
      <div class="quiz-controls">
        <button type="submit" class="btn">Check answers</button>
        <span class="quiz-score" hidden></span>
      </div>
    </form>'''


def render_category_index(species, category, base):
    label = "Animals" if category == "animal" else "Birds"
    lo, hi = (1, 50) if category == "animal" else (51, 100)
    items = [r for r in species if r["category"] == category]
    cards = "\n".join(card_html(base, r) for r in items)
    body = f"""
<div class="wrap">
  <h1>{label} ({lo:03d}–{hi:03d})</h1>
  <p class="lede">{len(items)} species, ordered by catalog number.</p>
  <div class="card-grid">{cards}</div>
</div>
"""
    return page_shell(base, f"{label} — {SITE_TITLE}", f"Index of all {len(items)} {label.lower()} covered in {SITE_TITLE}.", body, active=label)


def render_home(species, base):
    featured = species[:3] + [r for r in species if r["category"] == "bird"][:3]
    cards = "\n".join(card_html(base, r) for r in featured)
    body = f"""
<div class="hero">
  <div class="wrap">
    <h1>{esc(SITE_TITLE)}</h1>
    <p class="tagline">{esc(SITE_TAGLINE)}</p>
    <div class="search-box">
      <input type="search" id="site-search" placeholder="Search by species, scientific name, or behavior…" autocomplete="off">
      <div id="search-results" class="search-results" hidden></div>
    </div>
    <div class="hero-stats">
      <div><strong>50</strong><span>Animals</span></div>
      <div><strong>50</strong><span>Birds</span></div>
      <div><strong>100</strong><span>Verified quizzes</span></div>
    </div>
  </div>
</div>
<div class="wrap">
  <h2>Featured species</h2>
  <div class="card-grid">{cards}</div>
  <p class="browse-links">
    <a class="btn" href="{base}animals/index.html">Browse all animals →</a>
    <a class="btn" href="{base}birds/index.html">Browse all birds →</a>
  </p>
</div>
"""
    return page_shell(base, SITE_TITLE, SITE_TAGLINE, body, active="Home")


def render_glossary_page(species, base):
    all_terms = []
    for r in species:
        for g in r["glossary"]:
            all_terms.append({**g, "slug": r["slug"], "category": r["category"], "commonName": r["commonName"]})
    all_terms.sort(key=lambda t: t["term"].lower())

    groups = {}
    for t in all_terms:
        letter = t["term"][0].upper() if t["term"] else "#"
        if not letter.isalpha():
            letter = "#"
        groups.setdefault(letter, []).append(t)

    sections = []
    letters_nav = " ".join(f'<a href="#letter-{l}">{l}</a>' for l in sorted(groups))
    for letter in sorted(groups):
        entries = "".join(
            f'<div class="gloss-entry"><dt>{esc(t["term"])}</dt>'
            f'<dd>{inline_md(t["definition"])} '
            f'<a class="source-link" href="{base}{t["category"]}s/{t["slug"]}/index.html">— {esc(t["commonName"])}</a></dd></div>'
            for t in groups[letter]
        )
        sections.append(f'<section id="letter-{letter}"><h2>{letter}</h2><dl class="glossary-list">{entries}</dl></section>')

    body = f"""
<div class="wrap">
  <h1>Master Glossary</h1>
  <p class="lede">{len(all_terms)} behavioral and biological terms across all 100 books, alphabetized with links back to their source species.</p>
  <nav class="alpha-nav">{letters_nav}</nav>
  {"".join(sections)}
</div>
"""
    return page_shell(base, f"Master Glossary — {SITE_TITLE}", "Every glossary term across all 100 ethology books, alphabetized.", body, active="Glossary")


def render_quiz_index(species, base):
    items = "\n".join(
        f'<li class="quiz-index-item"><a href="{base}{r["category"]}s/{r["slug"]}/index.html#quiz">'
        f'<span class="card-num">{r["number"]:03d}</span> {esc(r["commonName"])} '
        f'<span class="sci">{inline_md("*" + r["scientificName"] + "*")}</span></a></li>'
        for r in species
    )
    body = f"""
<div class="wrap">
  <h1>Quiz Index</h1>
  <p class="lede">All 100 quizzes (10 questions each). Click a species to take its quiz on its book page.</p>
  <ul class="quiz-index">{items}</ul>
</div>
"""
    return page_shell(base, f"Quiz Index — {SITE_TITLE}", "Index of all 100 species quizzes.", body, active="Quizzes")


def render_about(base):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    blueprint = (ROOT / "project-blueprint.md").read_text(encoding="utf-8")

    def md_to_html_simple(text):
        lines = text.splitlines()
        out = []
        para = []

        def flush():
            if para:
                t = " ".join(l.strip() for l in para if l.strip())
                if t:
                    out.append(f"<p>{inline_md(t)}</p>")
                para.clear()

        for line in lines:
            if line.startswith("```") or line.startswith("|") or line.startswith("├") or line.startswith("└"):
                continue
            hm = re.match(r"^(#{1,3})\s+(.+)$", line)
            if hm:
                flush()
                level = min(len(hm.group(1)) + 1, 4)
                out.append(f"<h{level}>{inline_md(hm.group(2))}</h{level}>")
            elif re.match(r"^\d+\.\s", line.strip()) or line.strip().startswith("- "):
                flush()
                out.append(f"<li>{inline_md(re.sub(r'^(\\d+\\.|-)\\s+', '', line.strip()))}</li>")
            elif not line.strip():
                flush()
            else:
                para.append(line)
        flush()
        return "\n".join(out)

    body = f"""
<div class="wrap about-page">
  <h1>About This Project</h1>
  {md_to_html_simple(readme)}
  <hr>
  {md_to_html_simple(blueprint)}
</div>
"""
    return page_shell(base, f"About — {SITE_TITLE}", "About the Fieldnotes in Ethology project: mission, scope, and editorial process.", body, active="About")


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------

CSS = """
:root{
  --bg:#faf8f4; --bg-alt:#f1ede4; --text:#20241f; --text-muted:#5a5f56;
  --accent:#3b6b4f; --accent-dark:#274a37; --border:#ddd6c8;
  --card-bg:#ffffff; --myth:#8a4a2a; --reality:#2a5f3f;
  --max:1080px; --radius:10px;
  --font-body: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
  --font-ui: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#181a17; --bg-alt:#20231e; --text:#e9e7de; --text-muted:#a9ab9f;
    --accent:#7fbf9c; --accent-dark:#a6d9bd; --border:#33372f; --card-bg:#20231e;
    --myth:#d98a5f; --reality:#7fbf9c;
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-body);line-height:1.65;font-size:18px}
.wrap{max-width:var(--max);margin:0 auto;padding:0 24px}
a{color:var(--accent-dark)}
a:hover{color:var(--accent)}
.skip-link{position:absolute;left:-999px;top:0;background:var(--accent);color:#fff;padding:8px 16px;z-index:100}
.skip-link:focus{left:0}

.site-header{background:var(--bg-alt);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:10}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;padding:14px 24px;flex-wrap:wrap;gap:10px}
.brand{font-family:var(--font-ui);font-weight:700;font-size:1.15rem;text-decoration:none;color:var(--text)}
.site-nav{display:flex;gap:18px;font-family:var(--font-ui);font-size:0.95rem}
.site-nav a{text-decoration:none;color:var(--text-muted)}
.site-nav a:hover,.site-nav a.active{color:var(--accent-dark);font-weight:600}

main{min-height:60vh}
h1,h2,h3,h4{font-family:var(--font-ui);color:var(--text);line-height:1.25}
h1{font-size:2rem;margin:0.4em 0 0.3em}
h2{font-size:1.4rem;margin-top:2em;border-bottom:2px solid var(--border);padding-bottom:.3em}
h3{font-size:1.1rem;margin-top:1.5em}
.lede{color:var(--text-muted);font-family:var(--font-ui)}

.hero{background:linear-gradient(180deg,var(--bg-alt),var(--bg));padding:56px 0 40px;border-bottom:1px solid var(--border)}
.hero h1{font-size:2.6rem;margin-bottom:6px}
.tagline{font-family:var(--font-ui);color:var(--text-muted);font-size:1.15rem;max-width:640px}
.hero-stats{display:flex;gap:32px;margin-top:24px;font-family:var(--font-ui)}
.hero-stats div{display:flex;flex-direction:column}
.hero-stats strong{font-size:1.6rem;color:var(--accent-dark)}
.hero-stats span{color:var(--text-muted);font-size:.85rem;text-transform:uppercase;letter-spacing:.05em}

.search-box{position:relative;max-width:520px;margin-top:24px}
#site-search{width:100%;padding:12px 14px;font-size:1rem;border:1px solid var(--border);border-radius:var(--radius);font-family:var(--font-ui);background:var(--card-bg);color:var(--text)}
.search-results{position:absolute;top:100%;left:0;right:0;background:var(--card-bg);border:1px solid var(--border);border-radius:0 0 var(--radius) var(--radius);max-height:360px;overflow:auto;z-index:20;box-shadow:0 8px 24px rgba(0,0,0,.15)}
.search-results a{display:block;padding:10px 14px;text-decoration:none;color:var(--text);border-bottom:1px solid var(--border);font-family:var(--font-ui);font-size:.95rem}
.search-results a:hover{background:var(--bg-alt)}
.search-results .sr-empty{padding:14px;color:var(--text-muted);font-family:var(--font-ui)}

.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin:24px 0}
.card{display:block;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;text-decoration:none;color:var(--text);transition:transform .12s, box-shadow .12s}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.08)}
.card-num{display:inline-block;font-family:var(--font-ui);font-size:.75rem;color:var(--accent-dark);background:var(--bg-alt);padding:2px 8px;border-radius:20px;margin-bottom:8px}
.card h3{margin:0 0 4px;font-size:1.1rem}
.card .sci{font-style:italic;color:var(--text-muted);font-size:.9rem;margin:0 0 6px;font-family:var(--font-ui)}
.card .hook{font-family:var(--font-ui);font-size:.85rem;color:var(--accent-dark);margin:0 0 8px}
.card .teaser{font-size:.9rem;color:var(--text-muted);margin:0;line-height:1.5}

.btn{display:inline-block;font-family:var(--font-ui);background:var(--accent);color:#fff;padding:10px 18px;border-radius:var(--radius);text-decoration:none;border:none;font-size:.95rem;cursor:pointer}
.btn:hover{background:var(--accent-dark);color:#fff}
.browse-links{display:flex;gap:14px;margin:28px 0 48px}

.breadcrumb{font-family:var(--font-ui);font-size:.85rem;color:var(--text-muted);margin:18px 0}
.species-hero{padding:20px 0 10px;border-bottom:1px solid var(--border)}
.species-hero .sci{font-style:italic;font-size:1.1rem;color:var(--text-muted);font-family:var(--font-ui)}
.species-hero .hook{font-family:var(--font-ui);color:var(--accent-dark)}

.species-layout{display:grid;grid-template-columns:220px 1fr;gap:36px;margin:24px 0 60px;align-items:start}
.toc{position:sticky;top:80px;font-family:var(--font-ui);font-size:.88rem}
.toc h2{font-size:.85rem;text-transform:uppercase;letter-spacing:.05em;border:none;margin-top:0;color:var(--text-muted)}
.toc ul{list-style:none;padding:0;margin:0 0 16px}
.toc li{margin-bottom:6px}
.toc a{text-decoration:none;color:var(--text-muted)}
.toc a:hover{color:var(--accent-dark)}
.toc-jump{border-top:1px solid var(--border);padding-top:10px}

.book-body p{margin:0 0 1em}
.myth-block{background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px;margin:16px 0}
.myth-block .myth{color:var(--myth)}
.myth-block .reality{color:var(--reality);margin-bottom:0}
.tag{font-family:var(--font-ui);font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;font-weight:700;margin-right:6px}
.tag-myth{color:var(--myth)}
.tag-reality{color:var(--reality)}
pre{background:var(--bg-alt);border-radius:var(--radius);padding:14px;overflow:auto;white-space:pre-wrap;font-family:var(--font-ui);font-size:.9rem}

.glossary-list{margin:0}
.gloss-entry{margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid var(--border)}
.gloss-entry dt{font-weight:700;font-family:var(--font-ui);display:inline}
.gloss-entry dd{margin:2px 0 0;display:block}
.source-link{font-family:var(--font-ui);font-size:.82rem}

.badge{display:inline-block;font-family:var(--font-ui);font-size:.7rem;background:#e8b84b;color:#3a2c00;padding:1px 8px;border-radius:20px;margin-left:6px;vertical-align:middle}

.quiz-widget{margin-top:8px}
.quiz-question{border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px;margin-bottom:14px;background:var(--card-bg)}
.quiz-question legend{font-family:var(--font-ui);font-weight:600;padding:0 6px}
.quiz-opt{display:block;font-family:var(--font-ui);padding:6px 4px;cursor:pointer;border-radius:6px}
.quiz-opt:hover{background:var(--bg-alt)}
.quiz-opt input{margin-right:8px}
.quiz-question.correct{border-color:var(--reality)}
.quiz-question.incorrect{border-color:var(--myth)}
.quiz-feedback{font-family:var(--font-ui);font-size:.85rem;margin:8px 0 0}
.quiz-question.correct .quiz-feedback{color:var(--reality)}
.quiz-question.incorrect .quiz-feedback{color:var(--myth)}
.quiz-controls{display:flex;align-items:center;gap:16px;margin-top:8px}
.quiz-score{font-family:var(--font-ui);font-weight:700}

.alpha-nav{display:flex;flex-wrap:wrap;gap:8px;font-family:var(--font-ui);margin:18px 0;position:sticky;top:70px;background:var(--bg);padding:8px 0}
.alpha-nav a{text-decoration:none;border:1px solid var(--border);border-radius:6px;padding:2px 9px;font-size:.85rem}

.quiz-index{list-style:none;padding:0;columns:2;gap:24px}
.quiz-index-item{break-inside:avoid;margin-bottom:8px}
.quiz-index-item a{text-decoration:none;font-family:var(--font-ui);color:var(--text)}
.quiz-index-item .sci{font-style:italic;color:var(--text-muted);font-size:.85rem}

.about-page li{margin-bottom:6px}

.site-footer{border-top:1px solid var(--border);margin-top:60px;padding:24px 0;font-family:var(--font-ui);font-size:.85rem;color:var(--text-muted)}

@media (max-width: 800px){
  .species-layout{grid-template-columns:1fr}
  .toc{position:static}
  .quiz-index{columns:1}
  .site-nav{gap:12px;font-size:.85rem}
}
"""

JS = """
(function(){
  var quizzes = document.querySelectorAll('.quiz-widget');
  quizzes.forEach(function(form){
    var answers = JSON.parse(form.dataset.answers || '{}');
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var questions = form.querySelectorAll('.quiz-question');
      var correct = 0;
      questions.forEach(function(q){
        var num = q.dataset.qnum;
        var checked = q.querySelector('input[type=radio]:checked');
        var feedback = q.querySelector('.quiz-feedback');
        var answer = answers[num];
        q.classList.remove('correct','incorrect');
        if(!checked){
          feedback.hidden = false;
          feedback.textContent = 'No answer selected. Correct answer: ' + answer;
          q.classList.add('incorrect');
          return;
        }
        var isCorrect = checked.value === answer;
        if(isCorrect){ correct++; q.classList.add('correct'); }
        else { q.classList.add('incorrect'); }
        feedback.hidden = false;
        feedback.textContent = isCorrect ? 'Correct!' : ('Incorrect. Correct answer: ' + answer);
      });
      var scoreEl = form.querySelector('.quiz-score');
      scoreEl.hidden = false;
      scoreEl.textContent = 'Score: ' + correct + ' / ' + questions.length;
    });
  });

  var searchInput = document.getElementById('site-search');
  if(searchInput){
    var base = searchInput.dataset.base || '';
    var results = document.getElementById('search-results');
    var catalog = null;
    fetch(base + 'catalog.json').then(function(r){ return r.json(); }).then(function(data){ catalog = data; });

    function render(items){
      if(!items.length){
        results.innerHTML = '<div class="sr-empty">No matches.</div>';
        results.hidden = false;
        return;
      }
      results.innerHTML = items.slice(0,12).map(function(r){
        var href = base + r.category + 's/' + r.slug + '/index.html';
        return '<a href="' + href + '">' + String(r.number).padStart(3,'0') + ' — ' + r.commonName + ' (' + r.scientificName + ')</a>';
      }).join('');
      results.hidden = false;
    }

    searchInput.addEventListener('input', function(){
      var q = searchInput.value.trim().toLowerCase();
      if(!q || !catalog){ results.hidden = true; return; }
      var items = catalog.filter(function(r){
        return (r.commonName + ' ' + r.scientificName + ' ' + r.hook + ' ' + r.summaryText).toLowerCase().indexOf(q) !== -1;
      });
      render(items);
    });
    document.addEventListener('click', function(e){
      if(!results.contains(e.target) && e.target !== searchInput){ results.hidden = true; }
    });
  }
})();
"""


def main():
    print("Loading species...")
    species = load_species()
    print(f"Loaded {len(species)} species.")

    if OUT.exists():
        import shutil
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "assets").mkdir()
    (OUT / "animals").mkdir()
    (OUT / "birds").mkdir()
    (OUT / "glossary").mkdir()
    (OUT / "quizzes").mkdir()
    (OUT / "about").mkdir()

    (OUT / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "site.js").write_text(JS, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    # species pages
    for rec in species:
        folder = OUT / f"{rec['category']}s" / rec["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(render_species_page(rec), encoding="utf-8")

    (OUT / "index.html").write_text(render_home(species, ""), encoding="utf-8")
    (OUT / "animals" / "index.html").write_text(render_category_index(species, "animal", "../"), encoding="utf-8")
    (OUT / "birds" / "index.html").write_text(render_category_index(species, "bird", "../"), encoding="utf-8")
    (OUT / "glossary" / "index.html").write_text(render_glossary_page(species, "../"), encoding="utf-8")
    (OUT / "quizzes" / "index.html").write_text(render_quiz_index(species, "../"), encoding="utf-8")
    (OUT / "about" / "index.html").write_text(render_about("../"), encoding="utf-8")

    # inject search base into home page's input (data-base) via simple string patch
    home_path = OUT / "index.html"
    home_html = home_path.read_text(encoding="utf-8")
    home_html = home_html.replace('id="site-search"', 'id="site-search" data-base=""')
    home_path.write_text(home_html, encoding="utf-8")

    # catalog.json + derived indexes
    catalog = [{
        "number": r["number"],
        "slug": r["slug"],
        "category": r["category"],
        "commonName": r["commonName"],
        "scientificName": r["scientificName"],
        "hook": r["hook"],
        "summaryText": r["summaryPlain"][:400],
        "glossaryTermCount": len(r["glossary"]),
        "quizQuestionCount": len(r["questions"]),
        "referencesNeedVerification": r["referencesNeedVerification"],
    } for r in species]
    (OUT / "catalog.json").write_text(json.dumps(catalog, indent=2), encoding="utf-8")

    glossary_index = []
    for r in species:
        for g in r["glossary"]:
            glossary_index.append({"term": g["term"], "definition": g["definition"], "bookNumber": r["number"], "slug": r["slug"], "category": r["category"]})
    glossary_index.sort(key=lambda t: t["term"].lower())
    (OUT / "glossary-index.json").write_text(json.dumps(glossary_index, indent=2), encoding="utf-8")

    quiz_manifest = [{"bookNumber": r["number"], "slug": r["slug"], "category": r["category"], "questionCount": len(r["questions"]), "path": f"{r['category']}s/{r['slug']}/index.html"} for r in species]
    (OUT / "quiz-manifest.json").write_text(json.dumps(quiz_manifest, indent=2), encoding="utf-8")

    print(f"Wrote site to {OUT}")
    print(f"  species pages: {len(species)}")
    print(f"  glossary terms: {len(glossary_index)}")


if __name__ == "__main__":
    main()
