# Nordic Light Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle all pages of nayyarsan.github.io from dark-mode terminal aesthetic to Nordic Light (light mode, teal primary, Geist font, 1280px layout).

**Architecture:** Single `style.css` owns all tokens and component styles — all pages reference it. `blog.html` also needs structural HTML changes for the bento grid. `index.html` needs two CTA buttons added. All other HTML files need only a font import swap.

**Tech Stack:** Plain HTML, CSS custom properties, Google Fonts (Geist + JetBrains Mono), Playwright MCP for verification.

---

## File Map

| File | Change type |
|---|---|
| `style.css` | Full rewrite of tokens + all component styles |
| `index.html` | Add two CTA buttons to hero section |
| `blog.html` | Restructure main content for bento grid + filter tabs + archived logs |
| `about.html` | Font import swap only |
| `404.html` | Font import swap only |
| `blog/*.html` (10 files) | Font import swap only |

---

## Task 1: Update Font Imports Across All HTML Files

**Files:**
- Modify: `index.html`, `blog.html`, `about.html`, `404.html`, `blog/*.html`

- [ ] **Step 1: Replace the font import string in all HTML files**

Run this from the repo root in PowerShell:

```powershell
Get-ChildItem -Path . -Filter "*.html" -Recurse |
  Where-Object { $_.Name -notlike "stitch_*" } |
  ForEach-Object {
    $content = (Get-Content $_.FullName) -replace `
      'family=JetBrains\+Mono:wght@400;700&family=Inter:wght@400;500&display=swap', `
      'family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap'
    Set-Content -Path $_.FullName -Value $content
  }
```

- [ ] **Step 2: Verify the replacement**

```powershell
Select-String -Path "*.html", "blog/*.html" -Pattern "Inter" | Select-Object Path, Line
```

Expected: no output (zero matches). If any remain, fix manually.

- [ ] **Step 3: Verify Geist is present**

```powershell
Select-String -Path "index.html" -Pattern "Geist"
```

Expected: one line showing the new font URL.

- [ ] **Step 4: Commit**

```bash
git add index.html blog.html about.html 404.html blog/
git commit -m "chore: swap Inter for Geist in all HTML font imports"
```

---

## Task 2: Replace CSS Tokens in style.css

**Files:**
- Modify: `style.css` lines 1–15 (the `:root` block)

- [ ] **Step 1: Replace the entire `:root` block**

Replace lines 1–15 of `style.css` (the `/* ── Tokens */` section through the closing `}`) with:

```css
/* ── Tokens ─────────────────────────────────────────── */
:root {
  --bg:                  #faf8ff;
  --surface:             #ffffff;
  --surface-card:        #ffffff;
  --surface-hover:       #f2f3ff;
  --surface-container:   #eaedff;
  --text:                #131b2e;
  --muted:               #3e484d;
  --outline:             #6e797e;
  --outline-variant:     #bdc8ce;
  --accent:              #00647c;
  --accent-container:    #007f9d;
  --secondary-container: #d0e1fb;
  --inverse-surface:     #283044;
  --font-mono:           'JetBrains Mono', monospace;
  --font-body:           'Geist', sans-serif;
  --max-w:               1280px;
  --margin-desktop:      64px;
  --margin-mobile:       16px;
  --gutter:              24px;
  --radius:              4px;
  --radius-lg:           8px;
}
```

- [ ] **Step 2: Commit**

```bash
git add style.css
git commit -m "feat: replace dark-mode tokens with Nordic Light design tokens"
```

---

## Task 3: Update Reset, Body, Nav, and Layout CSS

**Files:**
- Modify: `style.css` — Reset, Body, Nav, Layout sections

- [ ] **Step 1: Replace the Reset section**

Replace the `/* ── Reset */` block with:

```css
/* ── Reset ───────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  font-size: 1rem;
  line-height: 1.7;
  padding-top: 64px;
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
```

- [ ] **Step 2: Replace the Nav section**

Replace the entire `/* ── Nav */` block (including the `@keyframes blink` animation) with:

```css
/* ── Nav ─────────────────────────────────────────────── */
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 56px;
  background: rgba(250,248,255,0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--outline-variant);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.nav__inner {
  width: 100%;
  max-width: var(--max-w);
  padding: 0 var(--margin-desktop);
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav__brand {
  font-family: var(--font-mono);
  font-size: 0.9rem;
  color: var(--accent);
  font-weight: 700;
  margin-right: auto;
}

.nav__link {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--muted);
  transition: color 0.15s;
  text-decoration: none;
}

.nav__link:hover { color: var(--accent); text-decoration: none; }

.nav__link.active {
  color: var(--accent);
  border-bottom: 2px solid var(--accent);
  padding-bottom: 4px;
  position: relative;
}
```

- [ ] **Step 3: Replace the Layout section**

Replace the `/* ── Layout */` block with:

```css
/* ── Layout ──────────────────────────────────────────── */
.container {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 3rem var(--margin-desktop);
}
```

- [ ] **Step 4: Replace the Section heading**

Replace the `/* ── Section heading */` block with:

```css
/* ── Section heading ─────────────────────────────────── */
.section-heading {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--accent);
  margin-bottom: 1.5rem;
}
```

- [ ] **Step 5: Commit**

```bash
git add style.css
git commit -m "feat: update nav, body, layout to Nordic Light"
```

---

## Task 4: Update Hero CSS + Add CTA Buttons to index.html

**Files:**
- Modify: `style.css` — Hero section
- Modify: `index.html` — hero section HTML

- [ ] **Step 1: Replace the Hero CSS block**

Replace the `/* ── Hero */` section in `style.css` with:

```css
/* ── Hero ────────────────────────────────────────────── */
.hero {
  margin-bottom: 3rem;
}

.hero__prompt {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--accent);
  margin-bottom: 0.5rem;
}

.hero__name {
  font-family: var(--font-body);
  font-size: 2.5rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text);
  margin-bottom: 0.75rem;
}

.hero__bio {
  color: var(--muted);
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
}

.hero__cta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  background: var(--accent);
  color: #ffffff;
  padding: 8px 24px;
  border-radius: var(--radius);
  transition: background 0.15s;
  text-decoration: none;
}

.btn-primary:hover {
  background: var(--accent-container);
  text-decoration: none;
  color: #ffffff;
}

.btn-ghost {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  background: transparent;
  color: var(--text);
  padding: 8px 24px;
  border-radius: var(--radius);
  border: 1px solid var(--outline-variant);
  transition: border-color 0.15s, color 0.15s;
  text-decoration: none;
}

.btn-ghost:hover {
  border-color: var(--accent);
  color: var(--accent);
  text-decoration: none;
}
```

- [ ] **Step 2: Add CTA buttons to `index.html` hero section**

In `index.html`, find this block:

```html
    <p class="hero__bio">AI &amp; Enterprise Dev &middot; Los Angeles &mdash; Building AI-powered tools and developer experiences.</p>
  </section>
```

Replace with:

```html
    <p class="hero__bio">AI &amp; Enterprise Dev &middot; Los Angeles &mdash; Building AI-powered tools and developer experiences.</p>
    <div class="hero__cta">
      <a class="btn-primary" href="about.html">Contact Me</a>
      <a class="btn-ghost" href="#">View Resume</a>
    </div>
  </section>
```

- [ ] **Step 3: Commit**

```bash
git add style.css index.html
git commit -m "feat: update hero styles and add CTA buttons"
```

---

## Task 5: Update Project Card CSS

**Files:**
- Modify: `style.css` — Project cards section

- [ ] **Step 1: Replace the entire Project cards section**

Replace the `/* ── Project cards */` block with:

```css
/* ── Project cards ───────────────────────────────────── */
.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--gutter);
  margin-bottom: 3rem;
}

.card {
  background: var(--surface-card);
  border: 1px solid var(--outline-variant);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: border-color 0.15s;
}

.card:hover {
  border-color: var(--accent);
  background: var(--surface-card);
  box-shadow: none;
}

.card__name {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
}

.card__desc {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--muted);
  flex: 1;
}

.card__status {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.05em;
}

.card__status--deployed { color: var(--accent); }
.card__status--private  { color: var(--muted); }

.card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.25rem;
}

.tag {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  color: var(--muted);
  background: var(--surface-container);
  padding: 2px 8px;
  border-radius: var(--radius);
}

.btn {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #ffffff;
  background: var(--accent);
  border: none;
  padding: 4px 12px;
  border-radius: var(--radius);
  transition: background 0.15s;
  text-decoration: none;
}

.btn:hover {
  background: var(--accent-container);
  text-decoration: none;
  color: #ffffff;
}

.badge-private {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--muted);
  background: var(--surface-container);
  border: 1px solid var(--outline-variant);
  padding: 3px 10px;
  border-radius: var(--radius);
}
```

- [ ] **Step 2: Commit**

```bash
git add style.css
git commit -m "feat: update project card styles to Nordic Light"
```

---

## Task 6: Add Blog CSS + Restructure blog.html

**Files:**
- Modify: `style.css` — replace Blog list section, add bento + filter + archived logs CSS
- Modify: `blog.html` — restructure `<main>` content

- [ ] **Step 1: Replace the Blog list CSS section**

Replace the `/* ── Blog list */` block in `style.css` with the following (this is a full replacement, adding all blog-related component styles):

```css
/* ── Blog header ─────────────────────────────────────── */
.blog-header {
  margin-bottom: 2rem;
}

.blog-header__title {
  font-family: var(--font-body);
  font-size: 2rem;
  font-weight: 600;
  color: var(--text);
  margin-top: 0.25rem;
  margin-bottom: 0.5rem;
}

.blog-header__subtitle {
  font-family: var(--font-body);
  font-size: 1rem;
  color: var(--muted);
}

/* ── Filter tabs ─────────────────────────────────────── */
.filter-tabs {
  display: flex;
  gap: 2rem;
  border-bottom: 1px solid var(--outline-variant);
  margin-bottom: 2rem;
  overflow-x: auto;
}

.filter-tab {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--muted);
  padding-bottom: 0.75rem;
  white-space: nowrap;
  cursor: default;
  border: none;
  background: none;
  transition: color 0.15s;
}

.filter-tab:hover { color: var(--text); }

.filter-tab--active {
  color: var(--accent);
  border-bottom: 2px solid var(--accent);
}

/* ── Bento grid ──────────────────────────────────────── */
.post-bento {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--gutter);
  margin-bottom: 2rem;
}

.post-bento--featured {
  grid-column: span 8;
  background: var(--surface-card);
  border: 1px solid var(--outline-variant);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition: border-color 0.15s;
  text-decoration: none;
}

.post-bento--featured:hover { border-color: var(--accent); text-decoration: none; }

.post-bento--secondary {
  grid-column: span 4;
  background: var(--surface-card);
  border: 1px solid var(--outline-variant);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition: border-color 0.15s;
  text-decoration: none;
}

.post-bento--secondary:hover { border-color: var(--accent); text-decoration: none; }

.post-bento__badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  background: var(--accent);
  color: #ffffff;
  padding: 3px 12px;
  border-radius: 9999px;
  width: fit-content;
}

.post-bento__meta {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--muted);
}

.post-bento__title {
  font-family: var(--font-body);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
  line-height: 1.3;
  transition: color 0.15s;
}

.post-bento--secondary .post-bento__title {
  font-size: 1.125rem;
}

.post-bento--featured:hover .post-bento__title,
.post-bento--secondary:hover .post-bento__title { color: var(--accent); }

.post-bento__excerpt {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--muted);
  flex: 1;
}

.post-bento__tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: auto;
}

/* ── Archived logs ───────────────────────────────────── */
.archived-logs__label {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--outline);
  margin-top: 40px;
  margin-bottom: 0;
  display: block;
}

.archived-logs__list {
  list-style: none;
}

.archived-log-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid var(--outline-variant);
  transition: background 0.15s, padding 0.15s, margin 0.15s;
}

.archived-log-row:hover {
  background: var(--surface-hover);
  padding-left: 8px;
  padding-right: 8px;
  margin-left: -8px;
  margin-right: -8px;
}

.archived-log-row__left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  min-width: 0;
}

.archived-log-row__date {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--muted);
  width: 6rem;
  flex-shrink: 0;
}

.archived-log-row__title {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text);
  text-decoration: none;
  transition: color 0.15s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.archived-log-row:hover .archived-log-row__title { color: var(--accent); }

.archived-log-row__right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
  margin-left: 1rem;
}

.archived-log-row__arrow {
  color: var(--outline);
  font-size: 0.875rem;
  transition: color 0.15s, transform 0.15s;
  display: inline-block;
}

.archived-log-row:hover .archived-log-row__arrow {
  color: var(--accent);
  transform: translateX(2px);
}
```

- [ ] **Step 2: Replace `blog.html` `<main>` content**

In `blog.html`, replace everything between `<main class="container">` and `</main>` with:

```html
<main class="container">

  <div class="blog-header">
    <p class="section-heading">&gt; ls blog/</p>
    <h1 class="blog-header__title">ls blog/</h1>
    <p class="blog-header__subtitle">Exploring the intersections of distributed systems, developer experience, and the subtle art of clean documentation.</p>
  </div>

  <div class="filter-tabs">
    <button class="filter-tab filter-tab--active">ALL_ENTRIES</button>
    <button class="filter-tab">TECHNICAL_GUIDES</button>
    <button class="filter-tab">AI_RESEARCH</button>
    <button class="filter-tab">SIDE_PROJECTS</button>
  </div>

  <div class="post-bento">
    <article class="post-bento--featured">
      <span class="post-bento__badge">FEATURED</span>
      <p class="post-bento__meta">2026-05-23 &nbsp;&middot;&nbsp; 3 MIN READ</p>
      <a class="post-bento__title" href="blog/repos-2026-05-23.html">Repos to Watch — Week of May 23, 2026</a>
      <p class="post-bento__excerpt">3 AI/SDLC repos worth your attention this week — filtered from GitHub Trending, HN, and Reddit.</p>
      <div class="post-bento__tags">
        <span class="tag">repos</span>
      </div>
    </article>

    <article class="post-bento--secondary">
      <p class="post-bento__meta">2026-03-22</p>
      <a class="post-bento__title" href="blog/md-export-pro.html">Markdown the Way You Actually Want It</a>
      <p class="post-bento__excerpt">Building a VS Code extension that previews, renders Mermaid, and exports to DOCX and HTML with theme control.</p>
      <div class="post-bento__tags">
        <span class="tag">TypeScript</span>
      </div>
    </article>
  </div>

  <span class="archived-logs__label">ARCHIVED_LOGS</span>
  <ul class="archived-logs__list">

    <li>
      <div class="archived-log-row">
        <div class="archived-log-row__left">
          <span class="archived-log-row__date">2026-03-21</span>
          <a class="archived-log-row__title" href="blog/jarvis.html">Running a Private AI on a Raspberry Pi 5</a>
        </div>
        <div class="archived-log-row__right">
          <span class="tag">Python</span>
          <span class="archived-log-row__arrow">→</span>
        </div>
      </div>
    </li>

    <li>
      <div class="archived-log-row">
        <div class="archived-log-row__left">
          <span class="archived-log-row__date">2026-03-20</span>
          <a class="archived-log-row__title" href="blog/reflexloop.html">Building Agents That Improve Themselves</a>
        </div>
        <div class="archived-log-row__right">
          <span class="tag">Python</span>
          <span class="archived-log-row__arrow">→</span>
        </div>
      </div>
    </li>

    <li>
      <div class="archived-log-row">
        <div class="archived-log-row__left">
          <span class="archived-log-row__date">2026-03-19</span>
          <a class="archived-log-row__title" href="blog/business-requirements-agent.html">Extending VS Code with the Copilot SDK</a>
        </div>
        <div class="archived-log-row__right">
          <span class="tag">TypeScript</span>
          <span class="archived-log-row__arrow">→</span>
        </div>
      </div>
    </li>

    <li>
      <div class="archived-log-row">
        <div class="archived-log-row__left">
          <span class="archived-log-row__date">2026-03-18</span>
          <a class="archived-log-row__title" href="blog/mynewsletters.html">Automating My Weekly AI Reading</a>
        </div>
        <div class="archived-log-row__right">
          <span class="tag">Python</span>
          <span class="archived-log-row__arrow">→</span>
        </div>
      </div>
    </li>

    <li>
      <div class="archived-log-row">
        <div class="archived-log-row__left">
          <span class="archived-log-row__date">2026-03-17</span>
          <a class="archived-log-row__title" href="blog/discoveryandresearch.html">Finding the Best AI Repos Before Everyone Else</a>
        </div>
        <div class="archived-log-row__right">
          <span class="tag">Python</span>
          <span class="archived-log-row__arrow">→</span>
        </div>
      </div>
    </li>

    <li>
      <div class="archived-log-row">
        <div class="archived-log-row__left">
          <span class="archived-log-row__date">2026-03-16</span>
          <a class="archived-log-row__title" href="blog/mybudgetapp.html">Cross-Platform Finance with Flutter + Firebase</a>
        </div>
        <div class="archived-log-row__right">
          <span class="tag">Dart</span>
          <span class="archived-log-row__arrow">→</span>
        </div>
      </div>
    </li>

    <li>
      <div class="archived-log-row">
        <div class="archived-log-row__left">
          <span class="archived-log-row__date">2026-03-15</span>
          <a class="archived-log-row__title" href="blog/sight-word-quest.html">Building a PWA for My Daughter</a>
        </div>
        <div class="archived-log-row__right">
          <span class="tag">JavaScript</span>
          <span class="archived-log-row__arrow">→</span>
        </div>
      </div>
    </li>

  </ul>

</main>
```

- [ ] **Step 3: Commit**

```bash
git add style.css blog.html
git commit -m "feat: add bento grid blog layout and Nordic Light blog styles"
```

---

## Task 7: Update Blog Post Page CSS

**Files:**
- Modify: `style.css` — Blog post page section

- [ ] **Step 1: Replace the Blog post page section**

Replace the `/* ── Blog post page */` block with:

```css
/* ── Blog post page ──────────────────────────────────── */
.post {
  padding: 3rem var(--margin-desktop);
  max-width: 720px;
  margin: 0 auto;
}

.post__breadcrumb {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--accent);
  margin-bottom: 1.5rem;
}

.post__title {
  font-family: var(--font-body);
  font-size: 2rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.post__date {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--muted);
  margin-bottom: 2rem;
}

.post__body p {
  margin-bottom: 1.25rem;
  font-family: var(--font-body);
  line-height: 1.75;
}

.post__body h2 {
  font-family: var(--font-body);
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--accent);
  margin: 2rem 0 0.75rem;
}

.post__body a { color: var(--accent); }
.post__body a:hover { text-decoration: underline; }

.post__tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 2rem 0;
}

.post__back {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--accent);
}
```

- [ ] **Step 2: Commit**

```bash
git add style.css
git commit -m "feat: update blog post page styles to Nordic Light"
```

---

## Task 8: Update About, 404, and Responsive CSS

**Files:**
- Modify: `style.css` — About, 404, Responsive sections

- [ ] **Step 1: Replace the About page section**

Replace the `/* ── About page */` block with:

```css
/* ── About page ──────────────────────────────────────── */
.about__section { margin-bottom: 2rem; }

.about__heading {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--accent);
  margin-bottom: 0.75rem;
  text-transform: uppercase;
}

.skill-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 2rem;
}

.skill-grid__label {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--muted);
  margin-bottom: 0.25rem;
}

.skill-grid__items {
  list-style: none;
  font-family: var(--font-body);
  font-size: 0.875rem;
}

.skill-grid__items li::before {
  content: '▸ ';
  color: var(--accent);
}
```

- [ ] **Step 2: Replace the 404 section**

Replace the `/* ── 404 */` block with:

```css
/* ── 404 ─────────────────────────────────────────────── */
.error-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 56px);
  text-align: center;
  gap: 1.5rem;
}

.error-page__code {
  font-family: var(--font-mono);
  font-size: 0.9rem;
  color: var(--accent);
}

.error-page__links {
  display: flex;
  gap: 1rem;
}
```

- [ ] **Step 3: Replace the Responsive section**

Replace the `/* ── Responsive */` block with:

```css
/* ── Responsive ──────────────────────────────────────── */
@media (max-width: 1024px) {
  .cards { grid-template-columns: repeat(2, 1fr); }
  .post-bento--featured { grid-column: span 12; }
  .post-bento--secondary { grid-column: span 12; }
}

@media (max-width: 640px) {
  .cards { grid-template-columns: 1fr; }
  .skill-grid { grid-template-columns: 1fr; }
  .container { padding: 3rem var(--margin-mobile); }
  .post { padding: 3rem var(--margin-mobile); }
  .nav__inner { padding: 0 var(--margin-mobile); }
  .filter-tabs { gap: 1rem; }
  .archived-log-row__right { display: none; }
}

@media (max-width: 480px) {
  .nav__inner { flex-wrap: wrap; gap: 0.75rem; padding: 0.5rem var(--margin-mobile); }
  .nav { height: auto; min-height: 56px; }
  body { padding-top: 90px; }
  .nav__brand { width: 100%; }
}
```

- [ ] **Step 4: Commit**

```bash
git add style.css
git commit -m "feat: update about, 404, and responsive styles to Nordic Light"
```

---

## Task 9: Playwright Visual Verification

**Files:** None modified — read-only verification

- [ ] **Step 1: Start a local file server**

```powershell
python -m http.server 8080
```

Leave this running. Open a new terminal for any follow-up commands.

- [ ] **Step 2: Open index.html and take a screenshot**

Use Playwright MCP:
- Navigate to `http://localhost:8080/index.html`
- Take a screenshot

Verify visually:
- Background is light (`#faf8ff`) — not black
- Nav brand `nayyarsan` is teal
- Nav links are muted grey, not neon green
- Project cards: white cards with light border, no glow
- Card names in Geist (rounded sans-serif, not mono)
- 3-column card grid on desktop
- "Contact Me" (solid teal) and "View Resume" (ghost) buttons visible in hero

- [ ] **Step 3: Open blog.html and take a screenshot**

- Navigate to `http://localhost:8080/blog.html`
- Take a screenshot

Verify:
- Filter tabs row (ALL_ENTRIES active in teal)
- Two bento cards at top — large featured (8 col) + smaller secondary (4 col)
- FEATURED badge (teal pill) on the first card
- ARCHIVED_LOGS label below bento
- Row list with dates, titles, arrows

- [ ] **Step 4: Open about.html and take a screenshot**

- Navigate to `http://localhost:8080/about.html`
- Take a screenshot

Verify:
- Section headings `// bio` etc. in teal mono
- Body text in Geist (proportional sans-serif)
- Teal `▸` bullets

- [ ] **Step 5: Open a blog post and take a screenshot**

- Navigate to `http://localhost:8080/blog/reflexloop.html`
- Take a screenshot

Verify:
- Title in Geist, large, dark text
- Body paragraphs in Geist (not mono)
- `h2` headings in teal Geist
- Narrow readable column (720px)

- [ ] **Step 6: Open 404.html and take a screenshot**

- Navigate to `http://localhost:8080/404.html`
- Take a screenshot

Verify:
- Light background (not black)
- Terminal-style error message in teal mono
- Buttons visible

- [ ] **Step 7: Check mobile viewport**

- Resize browser to 375px wide
- Navigate to `http://localhost:8080/index.html`
- Take a screenshot

Verify:
- Cards stack to 1 column
- Nav wraps correctly

- [ ] **Step 8: Fix any visual issues found, then commit**

```bash
git add style.css index.html blog.html
git commit -m "fix: address visual issues found in Playwright review"
```

Skip this step if no issues found.

- [ ] **Step 9: Stop the server**

Press `Ctrl+C` in the terminal running `python -m http.server 8080`.

- [ ] **Step 10: Final commit**

```bash
git add -A
git commit -m "feat: complete Nordic Light redesign — all pages"
```
