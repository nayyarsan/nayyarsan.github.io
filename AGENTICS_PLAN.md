# Agentics Plan — nayyarsan.github.io

Add [GitHub Agentic Workflows](https://github.com/githubnext/agentics) to the personal portfolio and blog.

## Prerequisites

```bash
gh extension install github/gh-aw
```

## Workflows to Add

- [ ] **Link Checker** — auto-finds and fixes broken blog and portfolio links daily
  ```bash
  gh aw add-wizard githubnext/agentics/link-checker
  ```

- [ ] **Markdown Linter** — keeps markdown blog posts consistent and well-formed
  ```bash
  gh aw add-wizard githubnext/agentics/markdown-linter
  ```

- [ ] **Documentation Unbloat** — simplifies verbose blog posts; reduces verbosity while maintaining clarity
  ```bash
  gh aw add-wizard githubnext/agentics/unbloat-docs
  ```

- [ ] **Multi-Device Docs Tester** — validates site layout across mobile, tablet, and desktop viewports
  ```bash
  gh aw add-wizard githubnext/agentics/daily-multi-device-docs-tester
  ```

- [ ] **Daily Accessibility Review** — reviews the site for accessibility issues automatically
  ```bash
  gh aw add-wizard githubnext/agentics/daily-accessibility-review
  ```

- [ ] **Issue Triage** — auto-labels incoming issues and PRs
  ```bash
  gh aw add-wizard githubnext/agentics/issue-triage
  ```

## Keep Workflows Updated

```bash
gh aw upgrade
gh aw update
```
