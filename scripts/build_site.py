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
# Inline SVG icon set (feather-style, inherits color via currentColor)
# ---------------------------------------------------------------------------

def icon(name, cls=""):
    paths = {
        "paw": '<path d="M9 10c1.1 0 2-1.12 2-2.5S10.1 5 9 5s-2 1.12-2 2.5S7.9 10 9 10zm6 0c1.1 0 2-1.12 2-2.5S16.1 5 15 5s-2 1.12-2 2.5S13.9 10 15 10zM5 14c.9 0 1.6-.9 1.6-2S5.9 10 5 10s-1.6.9-1.6 2S4.1 14 5 14zm14 0c.9 0 1.6-.9 1.6-2S19.9 10 19 10s-1.6.9-1.6 2S18.1 14 19 14zm-7-.5c-2.4 0-6 1.7-6 4.4 0 1.2 1 2.1 2.2 2.1.9 0 1.4-.3 2.2-.3.7 0 1.3.3 1.6.3.3 0 .9-.3 1.6-.3.8 0 1.3.3 2.2.3 1.2 0 2.2-.9 2.2-2.1 0-2.7-3.6-4.4-6-4.4z"/>',
        "feather": '<path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"/><line x1="16" y1="8" x2="2" y2="22"/><line x1="17.5" y1="15" x2="9" y2="15"/>',
        "search": '<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
        "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
        "quiz": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 2-3 4"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
        "tag": '<path d="M20.59 13.41 13.42 20.6a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>',
        "arrow-up": '<line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/>',
        "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
        "x-circle": '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
        "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
        "chevron-right": '<polyline points="9 18 15 12 9 6"/>',
        "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    }
    return f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


CATEGORY_META = {
    "animal": {"label": "Animal", "icon": "paw"},
    "bird": {"label": "Bird", "icon": "feather"},
}


def category_badge(category):
    meta = CATEGORY_META[category]
    return f'<span class="cat-badge cat-{category}">{icon(meta["icon"])}{meta["label"]}</span>'


def reading_minutes(sections):
    words = sum(len(re.sub(r"<[^>]+>", " ", s["html"]).split()) for s in sections)
    return max(1, round(words / 220))

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
            f'<p class="myth">{icon("x-circle")}<span class="tag tag-myth">Myth</span> {inline_md(myth_text.strip())}</p>'
            f'<p class="reality">{icon("check-circle")}<span class="tag tag-reality">Scientific reality</span> {inline_md(reality_text.strip())}</p>'
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


FAVICON_SVG = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%232d5a3d'%3E"
    "%3Cpath d='M9 10c1.1 0 2-1.12 2-2.5S10.1 5 9 5s-2 1.12-2 2.5S7.9 10 9 10zm6 0c1.1 0 2-1.12 2-2.5S16.1 5 15 5s-2 1.12-2 2.5S13.9 10 15 10zM5 14c.9 0 1.6-.9 1.6-2S5.9 10 5 10s-1.6.9-1.6 2S4.1 14 5 14zm14 0c.9 0 1.6-.9 1.6-2S19.9 10 19 10s-1.6.9-1.6 2S18.1 14 19 14zm-7-.5c-2.4 0-6 1.7-6 4.4 0 1.2 1 2.1 2.2 2.1.9 0 1.4-.3 2.2-.3.7 0 1.3.3 1.6.3.3 0 .9-.3 1.6-.3.8 0 1.3.3 2.2.3 1.2 0 2.2-.9 2.2-2.1 0-2.7-3.6-4.4-6-4.4z'/%3E"
    "%3C/svg%3E"
)


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
<meta name="theme-color" content="#2d5a3d">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{FAVICON_SVG}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
{extra_head}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{base}index.html">{icon("paw", "brand-icon")}<span>{esc(SITE_TITLE)}</span></a>
    <nav class="site-nav">
      {nav_html}
    </nav>
  </div>
</header>
<main id="main">
{body_html}
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      {icon("paw", "brand-icon")}<strong>{esc(SITE_TITLE)}</strong>
      <p>100 species, editorially reviewed and citation-checked. A public field guide to animal and bird behavior.</p>
    </div>
    <div class="footer-links">
      <span class="footer-heading">Explore</span>
      <a href="{base}animals/index.html">Animals</a>
      <a href="{base}birds/index.html">Birds</a>
      <a href="{base}glossary/index.html">Glossary</a>
      <a href="{base}quizzes/index.html">Quizzes</a>
    </div>
    <div class="footer-links">
      <span class="footer-heading">Project</span>
      <a href="{base}about/index.html">About</a>
      <a href="{REPO_URL}">{icon("github")}Source on GitHub</a>
    </div>
  </div>
</footer>
<button id="back-to-top" class="back-to-top" hidden aria-label="Back to top">{icon("arrow-up")}</button>
<script src="{base}assets/site.js"></script>
</body>
</html>
"""


def image_credit_html(image):
    if not image:
        return ""
    return (
        '<p class="img-credit">'
        f'Photo: {esc(image["artist"])} '
        f'(<a href="{esc(image["pageUrl"])}">{esc(image["license"])}</a>, via Wikimedia Commons)'
        "</p>"
    )


def card_html(base, rec, depth_prefix=""):
    href = f"{base}{rec['category']}s/{rec['slug']}/index.html"
    img = rec.get("image")
    media_html = (
        f'<div class="card-media"><img src="{esc(img["thumbUrl"])}" alt="{esc(rec["commonName"])}" loading="lazy" decoding="async"></div>'
        if img else ""
    )
    return f"""<a class="card" href="{href}">
  {media_html}
  <div class="card-body">
  <div class="card-top">
    {category_badge(rec['category'])}
    <span class="card-num">{rec['number']:03d}</span>
  </div>
  <h3>{esc(rec['commonName'])}</h3>
  <p class="sci">{inline_md('*' + rec['scientificName'] + '*') if not rec['scientificName'].startswith('*') else inline_md(rec['scientificName'])}</p>
  <p class="hook">{esc(rec['hook'])}</p>
  <p class="teaser">{esc(rec['teaser'])}</p>
  <span class="card-cta">Read the book {icon('chevron-right')}</span>
  </div>
</a>"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def load_image_credits():
    path = ROOT / "image-credits.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_species():
    master = parse_master_list()
    image_credits = load_image_credits()
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
                "image": image_credits.get(folder.name),
            })
    species.sort(key=lambda r: r["number"])
    return species


def render_species_page(rec):
    base = "../../"
    toc_items = "\n".join(
        f'<li><a href="#{s["id"]}">'
        + (f'<span class="toc-num">{s["num"]}</span>' if s["num"] else "")
        + f'{esc(s["title"])}</a></li>'
        for s in rec["sections"]
    )
    minutes = reading_minutes(rec["sections"])
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

    img = rec.get("image")
    hero_media_html = (
        f'''<div class="species-hero-media">
          <img src="{esc(img["thumbUrl"])}" alt="{esc(rec['commonName'])}" loading="eager" decoding="async">
          {image_credit_html(img)}
        </div>'''
        if img else ""
    )

    body = f"""
<header class="species-hero cat-{rec['category']}">
  <div class="wrap species-hero-grid">
    <div class="species-hero-text">
    <nav class="breadcrumb">
      <a href="{base}index.html">Home</a>{icon('chevron-right')}<a href="{base}{rec['category']}s/index.html">{rec['category'].capitalize()}s</a>{icon('chevron-right')}<span>{esc(rec['commonName'])}</span>
    </nav>
    <div class="species-hero-top">
      {category_badge(rec['category'])}
      <span class="card-num">No. {rec['number']:03d}</span>
      <span class="reading-time">{icon('clock')}{minutes} min read</span>
    </div>
    <h1>{esc(rec['bookTitle'])}</h1>
    <p class="sci">{sci_html}</p>
    <p class="hook">{esc(rec['hook'])}</p>
    </div>
    {hero_media_html}
  </div>
</header>

<div class="wrap species-page">
  <div class="species-layout">
    <aside class="toc">
      <h2>Contents</h2>
      <ul>{toc_items}</ul>
      <ul class="toc-jump">
        <li><a href="#glossary">{icon('tag')}Glossary</a></li>
        <li><a href="#quiz">{icon('quiz')}Quiz</a></li>
        <li><a href="#references">{icon('book')}References</a></li>
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
                <span class="quiz-opt-letter">{letter}</span><span>{inline_md(text)}</span>
              </label>'''
            for letter, text in sorted(q["options"].items())
        )
        q_html.append(f'''<fieldset class="quiz-question" data-qnum="{q['num']}">
          <legend><span class="quiz-qnum">{q['num']}</span>{inline_md(q['stem'])}</legend>
          {opts}
          <p class="quiz-feedback" hidden></p>
        </fieldset>''')
    answers_json = json.dumps(rec["answers"])
    total = len(rec["questions"])
    return f'''<form class="quiz-widget" id="{widget_id}" data-answers='{answers_json}'>
      <div class="quiz-progress"><div class="quiz-progress-bar" style="width:0%"></div></div>
      <p class="quiz-progress-label"><span class="quiz-answered">0</span> of {total} answered</p>
      {"".join(q_html)}
      <div class="quiz-controls">
        <button type="submit" class="btn">{icon('quiz')}Check answers</button>
        <span class="quiz-score" hidden></span>
      </div>
    </form>'''


def render_category_index(species, category, base):
    label = "Animals" if category == "animal" else "Birds"
    lo, hi = (1, 50) if category == "animal" else (51, 100)
    items = [r for r in species if r["category"] == category]
    cards = "\n".join(card_html(base, r) for r in items)
    body = f"""
<header class="page-banner cat-{category}">
  <div class="wrap">
    <span class="kicker">{icon(CATEGORY_META[category]['icon'])}Catalog {lo:03d}–{hi:03d}</span>
    <h1>{label}</h1>
    <p class="lede">{len(items)} species, ordered by catalog number — each with a full book, glossary, and quiz.</p>
  </div>
</header>
<div class="wrap">
  <div class="card-grid">{cards}</div>
</div>
"""
    return page_shell(base, f"{label} — {SITE_TITLE}", f"Index of all {len(items)} {label.lower()} covered in {SITE_TITLE}.", body, active=label)


def render_home(species, base):
    featured = species[:3] + [r for r in species if r["category"] == "bird"][:3]
    cards = "\n".join(card_html(base, r) for r in featured)
    body = f"""
<div class="hero">
  <div class="hero-blob hero-blob-1"></div>
  <div class="hero-blob hero-blob-2"></div>
  <div class="wrap">
    <span class="kicker">{icon('book')}A public field guide</span>
    <h1>{esc(SITE_TITLE)}</h1>
    <p class="tagline">{esc(SITE_TAGLINE)}</p>
    <div class="search-box">
      {icon('search', 'search-icon')}
      <input type="search" id="site-search" placeholder="Search by species, scientific name, or behavior…" autocomplete="off">
      <div id="search-results" class="search-results" hidden></div>
    </div>
    <div class="hero-stats">
      <div><strong>50</strong><span>{icon('paw')}Animals</span></div>
      <div><strong>50</strong><span>{icon('feather')}Birds</span></div>
      <div><strong>100</strong><span>{icon('quiz')}Verified quizzes</span></div>
      <div><strong>1,485</strong><span>{icon('tag')}Glossary terms</span></div>
    </div>
  </div>
</div>
<div class="wrap">
  <span class="kicker">Explore the collection</span>
  <h2>Featured species</h2>
  <div class="card-grid">{cards}</div>
  <p class="browse-links">
    <a class="btn" href="{base}animals/index.html">Browse all animals {icon('chevron-right')}</a>
    <a class="btn btn-outline" href="{base}birds/index.html">Browse all birds {icon('chevron-right')}</a>
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
<header class="page-banner">
  <div class="wrap">
    <span class="kicker">{icon('tag')}Cross-referenced</span>
    <h1>Master Glossary</h1>
    <p class="lede">{len(all_terms)} behavioral and biological terms across all 100 books, alphabetized with links back to their source species.</p>
    <div class="search-box glossary-filter">
      {icon('search', 'search-icon')}
      <input type="search" id="glossary-filter" placeholder="Filter terms…" autocomplete="off">
    </div>
  </div>
</header>
<div class="wrap">
  <nav class="alpha-nav">{letters_nav}</nav>
  <div id="glossary-content">
  {"".join(sections)}
  </div>
  <p id="glossary-empty" class="lede" hidden>No terms match your filter.</p>
</div>
"""
    return page_shell(base, f"Master Glossary — {SITE_TITLE}", "Every glossary term across all 100 ethology books, alphabetized.", body, active="Glossary")


def render_quiz_index(species, base):
    items = "\n".join(
        f'<a class="quiz-index-item cat-{r["category"]}" href="{base}{r["category"]}s/{r["slug"]}/index.html#quiz">'
        f'{category_badge(r["category"])}'
        f'<span class="card-num">{r["number"]:03d}</span>'
        f'<strong>{esc(r["commonName"])}</strong>'
        f'<span class="sci">{inline_md("*" + r["scientificName"] + "*")}</span>'
        f'<span class="quiz-index-cta">{icon("quiz")}10 questions</span>'
        "</a>"
        for r in species
    )
    body = f"""
<header class="page-banner">
  <div class="wrap">
    <span class="kicker">{icon('quiz')}Test yourself</span>
    <h1>Quiz Index</h1>
    <p class="lede">All 100 quizzes, 10 questions each. Pick a species to take its quiz on its book page.</p>
  </div>
</header>
<div class="wrap">
  <div class="quiz-index-grid">{items}</div>
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
<header class="page-banner">
  <div class="wrap">
    <span class="kicker">{icon('book')}The project</span>
    <h1>About This Project</h1>
  </div>
</header>
<div class="wrap about-page">
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
  --bg:#fbf8f2; --bg-alt:#f2ece0; --bg-raised:#ffffff; --text:#211f1a; --text-muted:#655f52;
  --accent:#2d5a3d; --accent-dark:#1c3d29; --accent-soft:#e4ede5;
  --bird:#2f5d78; --bird-soft:#e2edf3;
  --border:#e3dbc9; --myth:#a1502b; --reality:#1c6b45;
  --shadow:0 1px 2px rgba(30,25,15,.04); --shadow-lg:0 16px 40px -12px rgba(30,25,15,.18);
  --max:1120px; --radius:14px; --radius-sm:8px;
  --font-display: "Fraunces", Georgia, serif;
  --font-body: "Source Serif 4", Georgia, "Iowan Old Style", serif;
  --font-ui: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#15170f; --bg-alt:#1d2016; --bg-raised:#20231a; --text:#eee9da; --text-muted:#a9a48f;
    --accent:#7cc99a; --accent-dark:#a6dfbc; --accent-soft:#233028;
    --bird:#7fb8d9; --bird-soft:#1c2a33;
    --border:#33362a; --myth:#e0916a; --reality:#7cc99a;
    --shadow:0 1px 2px rgba(0,0,0,.3); --shadow-lg:0 20px 50px -12px rgba(0,0,0,.55);
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-body);line-height:1.7;font-size:18px;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--max);margin:0 auto;padding:0 28px}
a{color:var(--accent-dark);text-decoration-thickness:1px}
a:hover{color:var(--accent)}
.icon{width:1em;height:1em;vertical-align:-0.15em;flex-shrink:0}
.skip-link{position:absolute;left:-999px;top:0;background:var(--accent);color:#fff;padding:8px 16px;z-index:100;border-radius:0 0 8px 0}
.skip-link:focus{left:0}

/* Header */
.site-header{background:color-mix(in srgb, var(--bg) 88%, transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:30}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;padding:14px 28px;flex-wrap:wrap;gap:14px}
.brand{font-family:var(--font-display);font-weight:600;font-size:1.25rem;text-decoration:none;color:var(--text);display:flex;align-items:center;gap:8px;letter-spacing:-0.01em}
.brand-icon{width:22px;height:22px;color:var(--accent)}
.site-nav{display:flex;gap:22px;font-family:var(--font-ui);font-size:0.92rem}
.site-nav a{text-decoration:none;color:var(--text-muted);font-weight:500;position:relative;padding:4px 0}
.site-nav a::after{content:"";position:absolute;left:0;right:0;bottom:-2px;height:2px;background:var(--accent);transform:scaleX(0);transition:transform .15s ease}
.site-nav a:hover{color:var(--text)}
.site-nav a:hover::after,.site-nav a.active::after{transform:scaleX(1)}
.site-nav a.active{color:var(--accent-dark);font-weight:600}

main{min-height:60vh}
h1,h2,h3,h4{font-family:var(--font-display);color:var(--text);line-height:1.2;letter-spacing:-0.01em;font-weight:600}
h1{font-size:2.6rem;margin:.3em 0 .3em}
h2{font-size:1.6rem;margin-top:2.2em;padding-bottom:.4em;border-bottom:1px solid var(--border)}
h3{font-size:1.2rem;margin-top:1.6em}
.lede{color:var(--text-muted);font-family:var(--font-ui);font-size:1.05rem;max-width:65ch}
.kicker{display:inline-flex;align-items:center;gap:7px;font-family:var(--font-ui);font-size:.78rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--accent-dark);background:var(--accent-soft);padding:5px 12px 5px 10px;border-radius:20px;margin-bottom:14px}

/* Hero (home) */
.hero{position:relative;padding:76px 0 52px;border-bottom:1px solid var(--border);overflow:hidden;background:linear-gradient(180deg,var(--bg-alt),var(--bg) 75%)}
.hero-blob{position:absolute;border-radius:50%;filter:blur(60px);opacity:.35;z-index:0}
.hero-blob-1{width:420px;height:420px;background:var(--accent);top:-180px;right:-120px}
.hero-blob-2{width:320px;height:320px;background:var(--bird);bottom:-160px;left:-100px;opacity:.22}
.hero .wrap{position:relative;z-index:1}
.hero h1{font-size:3.2rem;margin:.15em 0 .2em;max-width:14ch}
.tagline{font-family:var(--font-ui);color:var(--text-muted);font-size:1.2rem;max-width:640px;margin:0}
.hero-stats{display:flex;gap:36px;margin-top:34px;font-family:var(--font-ui);flex-wrap:wrap}
.hero-stats div{display:flex;flex-direction:column;gap:2px}
.hero-stats strong{font-size:1.7rem;color:var(--accent-dark);font-family:var(--font-display)}
.hero-stats span{display:flex;align-items:center;gap:5px;color:var(--text-muted);font-size:.82rem;text-transform:uppercase;letter-spacing:.05em}

/* Search */
.search-box{position:relative;max-width:540px;margin-top:28px;display:flex;align-items:center}
.search-icon{position:absolute;left:16px;color:var(--text-muted);pointer-events:none}
#site-search,#glossary-filter{width:100%;padding:14px 16px 14px 42px;font-size:1rem;border:1px solid var(--border);border-radius:var(--radius);font-family:var(--font-ui);background:var(--bg-raised);color:var(--text);box-shadow:var(--shadow)}
#site-search:focus,#glossary-filter:focus{outline:2px solid var(--accent);outline-offset:1px}
.search-results{position:absolute;top:calc(100% + 6px);left:0;right:0;background:var(--bg-raised);border:1px solid var(--border);border-radius:var(--radius);max-height:360px;overflow:auto;z-index:20;box-shadow:var(--shadow-lg)}
.search-results a{display:block;padding:11px 16px;text-decoration:none;color:var(--text);border-bottom:1px solid var(--border);font-family:var(--font-ui);font-size:.92rem}
.search-results a:last-child{border-bottom:none}
.search-results a:hover{background:var(--accent-soft)}
.search-results .sr-empty{padding:14px 16px;color:var(--text-muted);font-family:var(--font-ui)}

/* Cards */
.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px;margin:28px 0}
.card{display:flex;flex-direction:column;background:var(--bg-raised);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;text-decoration:none;color:var(--text);transition:transform .15s ease, box-shadow .15s ease, border-color .15s ease}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg);border-color:transparent}
.card:hover .card-media img{transform:scale(1.05)}
.card-media{aspect-ratio:4/3;overflow:hidden;background:var(--bg-alt)}
.card-media img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s ease}
.card-body{padding:18px 22px 20px;display:flex;flex-direction:column;flex:1}
.card-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.cat-badge{display:inline-flex;align-items:center;gap:5px;font-family:var(--font-ui);font-size:.72rem;font-weight:600;padding:3px 9px;border-radius:20px}
.cat-badge.cat-animal{background:var(--accent-soft);color:var(--accent-dark)}
.cat-badge.cat-bird{background:var(--bird-soft);color:var(--bird)}
.card-num{font-family:var(--font-ui);font-size:.75rem;color:var(--text-muted);font-weight:600}
.card h3{margin:0 0 3px;font-size:1.25rem}
.card .sci{font-style:italic;color:var(--text-muted);font-size:.9rem;margin:0 0 8px;font-family:var(--font-ui)}
.card .hook{font-family:var(--font-ui);font-size:.82rem;font-weight:600;color:var(--accent-dark);margin:0 0 10px}
.card .teaser{font-size:.92rem;color:var(--text-muted);margin:0;line-height:1.55;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.card-cta{margin-top:14px;padding-top:12px;border-top:1px solid var(--border);font-family:var(--font-ui);font-size:.82rem;font-weight:600;color:var(--accent-dark);display:flex;align-items:center;gap:4px}

/* Buttons */
.btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-ui);font-weight:600;background:var(--accent);color:#fff;padding:12px 20px;border-radius:var(--radius-sm);text-decoration:none;border:none;font-size:.95rem;cursor:pointer;transition:background .15s ease, transform .1s ease}
.btn:hover{background:var(--accent-dark);color:#fff;transform:translateY(-1px)}
.btn-outline{background:transparent;color:var(--accent-dark);border:1px solid var(--border)}
.btn-outline:hover{background:var(--accent-soft);color:var(--accent-dark)}
.browse-links{display:flex;gap:14px;margin:32px 0 56px;flex-wrap:wrap}

/* Page banners (category/glossary/quiz/about) */
.page-banner{background:linear-gradient(180deg,var(--bg-alt),var(--bg));border-bottom:1px solid var(--border);padding:48px 0 36px}
.page-banner.cat-bird{background:linear-gradient(180deg,var(--bird-soft),var(--bg))}
.page-banner h1{margin-top:0}

/* Species hero */
.species-hero{background:linear-gradient(160deg,var(--accent-soft),var(--bg) 65%);border-bottom:1px solid var(--border);padding:28px 0 32px}
.species-hero.cat-bird{background:linear-gradient(160deg,var(--bird-soft),var(--bg) 65%)}
.breadcrumb{font-family:var(--font-ui);font-size:.82rem;color:var(--text-muted);margin:0 0 18px;display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.breadcrumb a{color:var(--text-muted);text-decoration:none}
.breadcrumb a:hover{color:var(--accent-dark)}
.breadcrumb .icon{width:14px;height:14px;opacity:.6}
.breadcrumb span{color:var(--text)}
.species-hero-top{display:flex;align-items:center;gap:12px;margin-bottom:14px;flex-wrap:wrap}
.reading-time{display:inline-flex;align-items:center;gap:5px;font-family:var(--font-ui);font-size:.78rem;color:var(--text-muted)}
.species-hero h1{font-size:2.4rem;margin:0 0 8px;max-width:22ch}
.species-hero .sci{font-style:italic;font-size:1.15rem;color:var(--text-muted);font-family:var(--font-ui);margin:0 0 6px}
.species-hero .hook{font-family:var(--font-ui);color:var(--accent-dark);font-weight:600;margin:0}
.species-hero-grid{display:grid;grid-template-columns:1fr 340px;gap:40px;align-items:center}
.species-hero-media img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--radius);box-shadow:var(--shadow-lg);display:block}
.img-credit{font-family:var(--font-ui);font-size:.72rem;color:var(--text-muted);margin:8px 2px 0}
.img-credit a{color:var(--text-muted)}
.img-credit a:hover{color:var(--accent-dark)}

/* Species layout / TOC */
.species-layout{display:grid;grid-template-columns:250px 1fr;gap:44px;margin:36px 0 70px;align-items:start}
.toc{position:sticky;top:88px;font-family:var(--font-ui);font-size:.87rem;background:var(--bg-raised);border:1px solid var(--border);border-radius:var(--radius);padding:18px 18px 14px;max-height:calc(100vh - 110px);overflow-y:auto}
.toc h2{font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;border:none;margin:0 0 10px;color:var(--text-muted);font-family:var(--font-ui);font-weight:700}
.toc ul{list-style:none;padding:0;margin:0 0 14px}
.toc li{margin-bottom:2px}
.toc a{text-decoration:none;color:var(--text-muted);display:flex;align-items:center;gap:8px;padding:5px 8px;border-radius:6px;line-height:1.3}
.toc a:hover{color:var(--text);background:var(--bg-alt)}
.toc a.active{color:var(--accent-dark);background:var(--accent-soft);font-weight:600}
.toc-num{font-size:.72rem;color:var(--text-muted);min-width:1.2em}
.toc-jump{border-top:1px solid var(--border);padding-top:10px}
.toc-jump a{gap:8px}
.toc-jump .icon{width:15px;height:15px;opacity:.7}

/* Book body */
.book-body p{margin:0 0 1.05em}
.book-body section{scroll-margin-top:90px}
.myth-block{background:var(--bg-raised);border:1px solid var(--border);border-left:3px solid var(--myth);border-radius:var(--radius-sm);padding:16px 20px;margin:18px 0}
.myth-block .myth{color:var(--text);display:flex;gap:8px;align-items:flex-start}
.myth-block .reality{color:var(--text);margin:10px 0 0;display:flex;gap:8px;align-items:flex-start;padding-top:10px;border-top:1px dashed var(--border)}
.myth-block .icon{margin-top:.2em;flex-shrink:0}
.myth-block .myth .icon{color:var(--myth)}
.myth-block .reality .icon{color:var(--reality)}
.tag{font-family:var(--font-ui);font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700;margin-right:2px}
.tag-myth{color:var(--myth)}
.tag-reality{color:var(--reality)}
pre{background:var(--bg-alt);border-radius:var(--radius-sm);padding:14px;overflow:auto;white-space:pre-wrap;font-family:var(--font-ui);font-size:.9rem}

/* Glossary */
.glossary-list{margin:0}
.gloss-entry{margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid var(--border)}
.gloss-entry dt{font-weight:700;font-family:var(--font-ui);display:inline;color:var(--accent-dark)}
.gloss-entry dd{margin:3px 0 0;display:block}
.source-link{font-family:var(--font-ui);font-size:.8rem;color:var(--text-muted)}
.glossary-filter{margin-top:22px;max-width:420px}
#glossary-content section{scroll-margin-top:130px}

.badge{display:inline-block;font-family:var(--font-ui);font-size:.68rem;font-weight:700;background:#e8b84b;color:#3a2c00;padding:2px 9px;border-radius:20px;margin-left:6px;vertical-align:middle}

/* Quiz */
.quiz-widget{margin-top:12px}
.quiz-progress{height:6px;border-radius:4px;background:var(--bg-alt);overflow:hidden;margin-bottom:6px}
.quiz-progress-bar{height:100%;background:var(--accent);border-radius:4px;transition:width .2s ease}
.quiz-progress-label{font-family:var(--font-ui);font-size:.8rem;color:var(--text-muted);margin:0 0 18px}
.quiz-question{border:1px solid var(--border);border-radius:var(--radius);padding:18px 20px;margin-bottom:16px;background:var(--bg-raised);transition:border-color .15s ease}
.quiz-question legend{font-family:var(--font-ui);font-weight:600;padding:0 6px;display:flex;align-items:center;gap:10px}
.quiz-qnum{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:var(--accent-soft);color:var(--accent-dark);font-size:.78rem;font-weight:700;flex-shrink:0}
.quiz-opt{display:flex;align-items:center;gap:10px;font-family:var(--font-ui);padding:9px 10px;cursor:pointer;border-radius:8px;margin-top:2px}
.quiz-opt:hover{background:var(--bg-alt)}
.quiz-opt input{margin:0;accent-color:var(--accent);width:16px;height:16px;flex-shrink:0}
.quiz-opt-letter{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:6px;border:1px solid var(--border);font-size:.72rem;font-weight:700;color:var(--text-muted);flex-shrink:0}
.quiz-question.correct{border-color:var(--reality)}
.quiz-question.incorrect{border-color:var(--myth)}
.quiz-feedback{font-family:var(--font-ui);font-size:.85rem;margin:10px 0 0;font-weight:600}
.quiz-question.correct .quiz-feedback{color:var(--reality)}
.quiz-question.incorrect .quiz-feedback{color:var(--myth)}
.quiz-controls{display:flex;align-items:center;gap:16px;margin-top:8px}
.quiz-score{font-family:var(--font-ui);font-weight:700;font-size:1.05rem;color:var(--accent-dark)}

/* Alpha nav */
.alpha-nav{display:flex;flex-wrap:wrap;gap:7px;font-family:var(--font-ui);margin:8px 0 24px;position:sticky;top:78px;background:var(--bg);padding:10px 0;z-index:5}
.alpha-nav a{text-decoration:none;border:1px solid var(--border);border-radius:8px;padding:4px 11px;font-size:.85rem;font-weight:600;color:var(--text-muted);background:var(--bg-raised)}
.alpha-nav a:hover{color:var(--accent-dark);border-color:var(--accent)}

/* Quiz index grid */
.quiz-index-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin:28px 0 56px}
.quiz-index-item{display:flex;flex-direction:column;gap:4px;text-decoration:none;font-family:var(--font-ui);color:var(--text);background:var(--bg-raised);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;transition:transform .15s ease, box-shadow .15s ease}
.quiz-index-item:hover{transform:translateY(-2px);box-shadow:var(--shadow-lg)}
.quiz-index-item .cat-badge{align-self:flex-start;margin-bottom:2px}
.quiz-index-item strong{font-size:1rem}
.quiz-index-item .sci{font-style:italic;color:var(--text-muted);font-size:.85rem}
.quiz-index-item .quiz-index-cta{margin-top:8px;padding-top:8px;border-top:1px solid var(--border);font-size:.8rem;color:var(--accent-dark);font-weight:600;display:flex;align-items:center;gap:6px}

.about-page{padding-bottom:60px}
.about-page li{margin-bottom:6px}
.about-page h2{font-size:1.35rem}

/* Footer */
.site-footer{border-top:1px solid var(--border);margin-top:60px;padding:44px 0 32px;font-family:var(--font-ui);font-size:.88rem;color:var(--text-muted);background:var(--bg-alt)}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:36px}
.footer-brand{display:flex;flex-direction:column;gap:8px}
.footer-brand strong{font-family:var(--font-display);font-size:1.1rem;color:var(--text);display:flex;align-items:center;gap:8px}
.footer-brand .brand-icon{color:var(--accent)}
.footer-brand p{margin:0;max-width:38ch}
.footer-links{display:flex;flex-direction:column;gap:9px}
.footer-heading{font-weight:700;color:var(--text);text-transform:uppercase;font-size:.75rem;letter-spacing:.06em;margin-bottom:2px}
.footer-links a{color:var(--text-muted);text-decoration:none;display:flex;align-items:center;gap:6px}
.footer-links a:hover{color:var(--accent-dark)}

/* Back to top */
.back-to-top{position:fixed;right:24px;bottom:24px;width:44px;height:44px;border-radius:50%;background:var(--accent);color:#fff;border:none;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:var(--shadow-lg);opacity:0;transform:translateY(10px);transition:opacity .2s ease, transform .2s ease;z-index:25}
.back-to-top.visible{opacity:1;transform:translateY(0)}
.back-to-top:hover{background:var(--accent-dark)}

@media (max-width: 900px){
  .species-layout{grid-template-columns:1fr}
  .toc{position:static;max-height:none}
  .footer-grid{grid-template-columns:1fr;gap:24px}
  .hero h1{font-size:2.4rem}
  h1{font-size:2.1rem}
  .species-hero-grid{grid-template-columns:1fr;gap:20px}
  .species-hero-media{order:-1}
  .species-hero-media img{aspect-ratio:16/9}
}
@media (max-width: 620px){
  body{font-size:16.5px}
  .site-nav{gap:12px;font-size:.85rem}
  .hero{padding:52px 0 36px}
  .hero h1{font-size:1.9rem}
  .card-grid{grid-template-columns:1fr}
}
"""

JS = """
(function(){
  // Quiz widgets: live progress + scored check
  var quizzes = document.querySelectorAll('.quiz-widget');
  quizzes.forEach(function(form){
    var answers = JSON.parse(form.dataset.answers || '{}');
    var questions = form.querySelectorAll('.quiz-question');
    var bar = form.querySelector('.quiz-progress-bar');
    var answeredEl = form.querySelector('.quiz-answered');

    function updateProgress(){
      var answered = form.querySelectorAll('input[type=radio]:checked').length;
      if(bar){ bar.style.width = Math.round((answered / questions.length) * 100) + '%'; }
      if(answeredEl){ answeredEl.textContent = answered; }
    }
    form.addEventListener('change', updateProgress);

    form.addEventListener('submit', function(e){
      e.preventDefault();
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
      var first = form.querySelector('.quiz-question.incorrect, .quiz-question.correct');
      if(first){ first.scrollIntoView({behavior:'smooth', block:'center'}); }
    });
  });

  // Home / glossary search
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

  // Glossary filter
  var glossaryFilter = document.getElementById('glossary-filter');
  if(glossaryFilter){
    var entries = document.querySelectorAll('#glossary-content .gloss-entry');
    var sections = document.querySelectorAll('#glossary-content section');
    var alphaNav = document.querySelector('.alpha-nav');
    var emptyMsg = document.getElementById('glossary-empty');
    glossaryFilter.addEventListener('input', function(){
      var q = glossaryFilter.value.trim().toLowerCase();
      var anyVisible = false;
      sections.forEach(function(sec){
        var sectionHasMatch = false;
        sec.querySelectorAll('.gloss-entry').forEach(function(entry){
          var text = entry.textContent.toLowerCase();
          var match = !q || text.indexOf(q) !== -1;
          entry.hidden = !match;
          if(match){ sectionHasMatch = true; anyVisible = true; }
        });
        sec.hidden = !sectionHasMatch;
      });
      if(alphaNav){ alphaNav.hidden = q.length > 0; }
      if(emptyMsg){ emptyMsg.hidden = anyVisible; }
    });
  }

  // Active section highlighting in the species-page table of contents
  var toc = document.querySelector('.toc');
  if(toc){
    var tocLinks = toc.querySelectorAll('a[href^="#"]');
    var linkFor = {};
    tocLinks.forEach(function(a){ linkFor[a.getAttribute('href').slice(1)] = a; });
    var sections = document.querySelectorAll('.book-body section[id]');
    if('IntersectionObserver' in window && sections.length){
      var current = null;
      var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            if(current) current.classList.remove('active');
            current = linkFor[entry.target.id];
            if(current) current.classList.add('active');
          }
        });
      }, {rootMargin: '-15% 0px -70% 0px', threshold: 0});
      sections.forEach(function(s){ observer.observe(s); });
    }
  }

  // Back-to-top button
  var backToTop = document.getElementById('back-to-top');
  if(backToTop){
    window.addEventListener('scroll', function(){
      backToTop.classList.toggle('visible', window.scrollY > 600);
      backToTop.hidden = false;
    }, {passive:true});
    backToTop.addEventListener('click', function(){
      window.scrollTo({top:0, behavior:'smooth'});
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
