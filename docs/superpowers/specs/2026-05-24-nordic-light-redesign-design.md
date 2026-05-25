# Nordic Light Redesign — Design Spec
**Date:** 2026-05-24  
**Scope:** All pages — `index.html`, `blog.html`, `about.html`, `404.html`, `blog/*.html`  
**Approach:** Token-first surgical update to existing `style.css`. No framework. No images.

---

## 1. Design System Tokens

Single source of truth in `style.css` `:root`. All pages reference this one file.

### Colors
| Token | Value | Role |
|---|---|---|
| `--bg` | `#faf8ff` | Page background |
| `--surface` | `#ffffff` | Elevated surface (nav, cards) |
| `--surface-card` | `#ffffff` | Card background |
| `--surface-hover` | `#f2f3ff` | Card / row hover background |
| `--surface-container` | `#eaedff` | Tag / chip background |
| `--text` | `#131b2e` | Primary text |
| `--muted` | `#3e484d` | Secondary / supporting text |
| `--outline` | `#6e797e` | Subtle borders (rows, dividers) |
| `--outline-variant` | `#bdc8ce` | Card borders, input borders |
| `--accent` | `#00647c` | Primary interactive color (links, active nav, buttons) |
| `--accent-container` | `#007f9d` | Primary button hover |
| `--secondary-container` | `#d0e1fb` | WHOAMI badge background |
| `--inverse-surface` | `#283044` | Dark banner (tech stack strip) |

### Typography
| Token | Value |
|---|---|
| `--font-body` | `'Geist', sans-serif` |
| `--font-mono` | `'JetBrains Mono', monospace` |

Google Fonts import: Geist (wght 400–700) + JetBrains Mono (wght 400;700). Inter removed.

### Layout
| Token | Value |
|---|---|
| `--max-w` | `1280px` |
| `--margin-desktop` | `64px` |
| `--margin-mobile` | `16px` |
| `--gutter` | `24px` |
| `--radius` | `4px` |
| `--radius-lg` | `8px` |

---

## 2. Nav

- Fixed top, height `56px`
- Background: `rgba(250,248,255,0.85)` with `backdrop-filter: blur(12px)`
- Bottom border: `1px solid var(--outline-variant)`
- Brand `nayyarsan` in `--accent` JetBrains Mono, `font-weight: 700`
- Nav links in `--muted` Geist, hover → `--accent`
- Active link: `color: --accent`, `border-bottom: 2px solid --accent`, `padding-bottom: 4px`
- Remove blinking cursor animation entirely
- Max-width container: `1280px`, `64px` side padding desktop, `16px` mobile

---

## 3. Index page (`index.html`)

### Hero
- Terminal prompt `> whoami` stays: JetBrains Mono, `0.85rem`, `--accent`
- `hero__name`: Geist, `2.5rem`, weight 600, letter-spacing `-0.02em`, color `--text`
- Bio: Geist, `1.125rem`, color `--muted`
- Two CTA buttons below bio:
  - **Primary "Contact Me":** solid `--accent` bg, white text, `--radius` 4px, `px: 24px py: 8px`
  - **Ghost "View Resume":** transparent bg, `1px solid --outline-variant`, `--text` color, same sizing
  - Both: `font-family: --font-mono`, `font-size: 0.75rem`, `letter-spacing: 0.05em`, uppercase

### Project Cards
- Grid: 3 columns desktop (>1024px), 2 columns tablet (640–1024px), 1 column mobile
- Gap: `var(--gutter)` (24px)
- Card: white bg, `1px solid var(--outline-variant)`, `border-radius: var(--radius-lg)`, `padding: 20px`
- Hover: `border-color: var(--accent)`, no glow/shadow
- `card__name`: Geist, `1rem`, weight 600, `--text`
- `card__desc`: Geist, `0.875rem`, `--muted`
- Tags: `--surface-container` bg, `--muted` text, `--radius` 4px, JetBrains Mono `0.7rem` uppercase
- STATUS DEPLOYED: `--accent` teal. STATUS PRIVATE: `--muted`
- GitHub button (`btn`): solid `--accent` bg, white text, hover → `--accent-container`
- Private badge: `--surface-container` bg, `--muted` text, `1px solid --outline-variant`

---

## 4. Blog page (`blog.html`)

### Header
- `> ls blog/` prompt in teal mono (same as section-heading)
- `h1` "ls blog/" in Geist display, `2rem`, weight 600
- Subtitle line: Geist `1rem`, `--muted`

### Filter Tabs
- Horizontal row, JetBrains Mono, `0.75rem`, uppercase, letter-spacing `0.05em`
- Active tab: `--accent`, `border-bottom: 2px solid --accent`
- Inactive: `--muted`, hover → `--text`
- Purely decorative (no JS filtering yet)
- Labels: ALL_ENTRIES · TECHNICAL_GUIDES · AI_RESEARCH · SIDE_PROJECTS

### Bento Grid (top 2 posts)
- 12-column CSS grid, `gap: var(--gutter)`
- **Featured post** (`.post-bento--featured`): spans 8 cols
  - Card: white bg, `--outline-variant` border, `--radius-lg`, padding `24px`
  - "FEATURED" badge: `--accent` bg, white text, `--radius` full (pill), mono caps
  - Title: Geist `1.5rem` weight 600, hover → `--accent`
  - Date + read time: JetBrains Mono `0.75rem`, `--muted`
  - Excerpt: Geist `0.875rem`, `--muted`
  - Tags at bottom
- **Secondary post** (`.post-bento--secondary`): spans 4 cols
  - Same card style, no badge
  - Title: Geist `1.125rem` weight 600
- On tablet (640–1024px): both cards go full width, stacked
- On mobile: same

### Archived Logs (remaining posts)
- Section label `ARCHIVED_LOGS`: JetBrains Mono, `0.7rem`, `--outline`, uppercase, letter-spacing `0.1em`, `margin-top: 40px`
- Each row: flex, `justify-content: space-between`, `padding: 12px 0`, `border-bottom: 1px solid --outline-variant`
- Left: date in mono `--muted` `w-24`, then title in Geist `--text` weight 500
- Right: tag badge + `→` arrow in `--outline`, hover `→` shifts to `--accent`
- Row hover: `background: --surface-hover`, `title color → --accent`

---

## 5. About page (`about.html`)

- Section headings (`about__heading`): JetBrains Mono, `0.85rem`, `--accent`, uppercase — structure unchanged
- Body text: Geist `0.875rem`, `--muted`
- Skill grid stays 2-col desktop / 1-col mobile
- Bullet `▸` color: `--accent`
- All other layout unchanged

---

## 6. Blog post pages (`blog/*.html`)

- Max-width for post body: `720px` (narrower than container, for readable prose line length)
- `post__title`: Geist, `2rem`, weight 600, letter-spacing `-0.02em`, `--text`
- `post__date`: JetBrains Mono, `0.8rem`, `--muted`
- `post__breadcrumb`: JetBrains Mono, `0.8rem`, `--accent`
- `post__body p`: Geist, `1rem`, `line-height: 1.75`, `--text`
- `post__body h2`: Geist, `1.125rem`, weight 600, `--accent` (not mono)
- `post__body a`: `--accent`, underline on hover
- Tags: same chip style as cards
- Back link: JetBrains Mono, `--accent`

---

## 7. 404 page (`404.html`)

- Token swap only — structure unchanged
- White bg, teal accent, dark text
- Terminal feel preserved (appropriate for an error page)

---

## 8. Verification

After implementation, use Playwright MCP to:
1. Navigate to `index.html` — verify light bg, teal nav, 3-col card grid
2. Navigate to `blog.html` — verify bento top 2, filter tabs, archived log list
3. Navigate to `about.html` — verify Geist body, teal headings
4. Navigate to a `blog/*.html` — verify 720px prose width, Geist body text
5. Navigate to `404.html` — verify light bg, terminal style preserved
6. Check mobile viewport (375px) — cards go 1-col, nav wraps correctly

---

## HTML Changes Required

`style.css` is the primary target, but two HTML files need structural edits:

- **`blog.html`** — wrap top 2 `<li>` items in a 12-col bento grid container; add `.post-bento--featured` and `.post-bento--secondary` classes; wrap remaining posts in an archived-logs section with the `ARCHIVED_LOGS` label and filter tab row above the bento grid.
- **`index.html`** — add the two CTA buttons (Contact Me / View Resume) to the hero section.

All `blog/*.html` and `about.html` and `404.html` need no structural HTML changes — CSS token swap only.

---

## Out of Scope
- Dark mode toggle
- JS for filter tab functionality
- Images / hero photography
- Blog post page structural changes (only style updates)
