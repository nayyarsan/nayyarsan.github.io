#!/usr/bin/env python3
"""
Generate a weekly "Repos to Watch" blog post from discoveryandresearch's spotlight.json.

Fetches:  https://raw.githubusercontent.com/nayyarsan/discoveryandresearch/output/data/spotlight.json
Writes:   blog/repos-YYYY-MM-DD.html   (new post)
Updates:  blog.html                    (prepends entry to post list)

Run manually:  python scripts/publish_repos_spotlight.py
Run with file: python scripts/publish_repos_spotlight.py --local path/to/spotlight.json
"""
import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SPOTLIGHT_URL = (
    "https://raw.githubusercontent.com/nayyarsan/discoveryandresearch"
    "/output/data/spotlight.json"
)

REPO_ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_spotlight(local_path: str | None = None) -> dict:
    if local_path:
        return json.loads(Path(local_path).read_text())
    req = urllib.request.Request(SPOTLIGHT_URL, headers={"User-Agent": "nayyarsan-blog/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


LANGUAGE_COLORS = {
    "python":     "#3572A5",
    "typescript": "#3178c6",
    "javascript": "#f1e05a",
}


def _lang_badge(lang: str) -> str:
    color = LANGUAGE_COLORS.get(lang.lower(), "#555")
    return (
        f'<span class="tag" style="border-left:3px solid {color};padding-left:6px">'
        f'{_esc(lang)}</span>'
    )


def _star_delta(delta: int) -> str:
    if delta <= 0:
        return ""
    return f'<span style="color:var(--accent);font-family:var(--font-mono);font-size:0.8rem">+{delta:,} this week</span>'


# ---------------------------------------------------------------------------
# Generate blog post HTML
# ---------------------------------------------------------------------------

POST_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{page_title} — Shyam Jayachandran</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../style.css" />
  <style>
    .repo-card {{
      border: 1px solid #222;
      border-radius: var(--radius);
      padding: 1.25rem 1.5rem;
      margin: 1.5rem 0;
      background: var(--surface-card);
    }}
    .repo-card__name {{
      font-family: var(--font-mono);
      font-size: 1rem;
      font-weight: 700;
      color: var(--accent);
      text-decoration: none;
    }}
    .repo-card__name:hover {{ text-decoration: underline; }}
    .repo-card__meta {{
      display: flex;
      gap: 1rem;
      align-items: center;
      margin: 0.4rem 0 0.75rem;
      flex-wrap: wrap;
    }}
    .repo-card__stars {{
      font-family: var(--font-mono);
      font-size: 0.8rem;
      color: var(--muted);
    }}
    .repo-card__desc {{ margin: 0.5rem 0 0.75rem; }}
    .repo-card__why {{
      border-left: 2px solid var(--accent);
      padding-left: 0.75rem;
      color: var(--text);
      font-size: 0.95rem;
    }}
    .repo-card__action {{
      margin-top: 0.75rem;
      font-size: 0.85rem;
      color: var(--muted);
    }}
    .repo-card__action a {{ color: var(--accent); }}
  </style>
</head>
<body>

<nav class="nav">
  <div class="nav__inner">
    <span class="nav__brand">nayyarsan</span>
    <a class="nav__link" href="../index.html">~/projects</a>
    <a class="nav__link" href="../blog.html">~/blog</a>
    <a class="nav__link" href="../about.html">~/about</a>
  </div>
</nav>

<article class="post">
  <p class="post__breadcrumb">&gt; cd ~/blog/{slug}</p>
  <h1 class="post__title">{h1_title}</h1>
  <p class="post__date">{date_iso}</p>

  <div class="post__body">
    <p>{intro}</p>
{repo_cards}
  </div>

  <div class="post__tags">
{tags}
  </div>

  <p class="post__back"><a href="../blog.html">← back to blog</a></p>
</article>

<script src="../nav.js"></script>
</body>
</html>
"""

REPO_CARD_TEMPLATE = """\
    <div class="repo-card">
      <a class="repo-card__name" href="{url}" target="_blank" rel="noopener">{name}</a>
      <div class="repo-card__meta">
        {lang_badge}
        <span class="repo-card__stars">★ {stars:,}</span>
        {star_delta}
      </div>
      <p class="repo-card__desc">{description}</p>
      <p class="repo-card__why">{why_notable}</p>
      {action_line}
    </div>"""


def _repo_card(repo: dict) -> str:
    lang = repo.get("language", "")
    delta = repo.get("stars_delta", 0)
    reason = repo.get("relevance_reason", "").strip()
    action_line = ""
    if reason:
        action_line = (
            f'<p class="repo-card__action">'
            f'<strong>Why it matters for your stack:</strong> {_esc(reason)}'
            f'</p>'
        )
    return REPO_CARD_TEMPLATE.format(
        url=repo.get("url", "#"),
        name=_esc(repo.get("name", "")),
        lang_badge=_lang_badge(lang) if lang else "",
        stars=repo.get("stars", 0),
        star_delta=_star_delta(delta),
        description=_esc(repo.get("description", "")),
        why_notable=_esc(repo.get("why_notable", "")),
        action_line=action_line,
    )


def _intro(repos: list[dict], week_of: str) -> str:
    count = len(repos)
    languages = sorted({r.get("language", "").capitalize() for r in repos if r.get("language")})
    lang_str = ", ".join(languages) if languages else "various languages"
    return (
        f"Week of {week_of}. {count} repo{'s' if count != 1 else ''} surfaced by the "
        f"discovery pipeline across GitHub Trending, Hacker News, Reddit, and Lobsters. "
        f"All are {lang_str}. Filtered for AI/SDLC relevance, MIT or Apache-2.0 licensed, "
        f"and not seen in a previous spotlight."
    )


def _tags(repos: list[dict]) -> str:
    tag_set = {"repos", "AI", "SDLC"}
    for r in repos:
        lang = r.get("language", "").capitalize()
        if lang:
            tag_set.add(lang)
        for t in r.get("topics", [])[:2]:
            tag_set.add(t)
    return "\n".join(f'    <span class="tag">{_esc(t)}</span>' for t in sorted(tag_set))


def generate_post_html(repos: list[dict], date_iso: str, week_of: str) -> tuple[str, str]:
    """Return (slug, html)."""
    slug = f"repos-{date_iso}"
    page_title = f"Repos to Watch — Week of {week_of}"
    h1_title = page_title
    cards = "\n".join(_repo_card(r) for r in repos)
    html = POST_TEMPLATE.format(
        slug=slug,
        page_title=page_title,
        h1_title=h1_title,
        date_iso=date_iso,
        intro=_intro(repos, week_of),
        repo_cards=cards,
        tags=_tags(repos),
    )
    return slug, html


# ---------------------------------------------------------------------------
# Patch blog.html
# ---------------------------------------------------------------------------

BLOG_LIST_ENTRY = """\
    <li>
      <p class="post-item__date">{date_iso} &nbsp;<span class="tag">repos</span></p>
      <a class="post-item__title" href="blog/{slug}.html">{title}</a>
      <p class="post-item__teaser">{teaser}</p>
    </li>
"""


def patch_blog_index(blog_html_path: Path, slug: str, date_iso: str,
                     week_of: str, repos: list[dict]) -> bool:
    """Prepend a new <li> entry to the post list. Returns True if changed."""
    content = blog_html_path.read_text(encoding="utf-8")

    # Skip if this slug is already listed
    if f'href="blog/{slug}.html"' in content:
        print(f"  blog.html already contains {slug} — skipping patch")
        return False

    title = f"Repos to Watch — Week of {week_of}"
    count = len(repos)
    teaser = (
        f"{count} AI/SDLC repo{'s' if count != 1 else ''} worth your attention this week — "
        f"filtered from GitHub Trending, HN, and Reddit."
    )

    entry = BLOG_LIST_ENTRY.format(
        date_iso=date_iso,
        slug=slug,
        title=_esc(title),
        teaser=_esc(teaser),
    )

    # Insert immediately after <ul class="post-list">
    marker = '<ul class="post-list">'
    if marker not in content:
        print("  WARNING: could not find post-list marker in blog.html", file=sys.stderr)
        return False

    patched = content.replace(marker, marker + "\n" + entry, 1)
    blog_html_path.write_text(patched, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", metavar="PATH",
                        help="Use a local spotlight.json instead of fetching from GitHub")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print generated HTML, do not write files")
    args = parser.parse_args()

    print("Fetching spotlight.json...")
    try:
        data = fetch_spotlight(args.local)
    except Exception as e:
        print(f"ERROR: could not load spotlight.json: {e}", file=sys.stderr)
        sys.exit(1)

    repos = data.get("repos", [])
    if not repos:
        print("spotlight.json contains no repos — nothing to publish.")
        sys.exit(0)

    print(f"  {len(repos)} repos in spotlight")

    # Use today's date as the post date
    today = datetime.now(tz=timezone.utc)
    date_iso = today.strftime("%Y-%m-%d")
    week_of = today.strftime("%b %d, %Y")

    slug, html = generate_post_html(repos, date_iso, week_of)

    if args.dry_run:
        print(f"\n--- {slug}.html ---\n")
        print(html)
        return

    # Write post file
    post_path = REPO_ROOT / "blog" / f"{slug}.html"
    post_path.write_text(html, encoding="utf-8")
    print(f"  Written {post_path}")

    # Patch blog index
    blog_html = REPO_ROOT / "blog.html"
    changed = patch_blog_index(blog_html, slug, date_iso, week_of, repos)
    if changed:
        print(f"  Patched {blog_html}")

    print("Done.")


if __name__ == "__main__":
    main()
