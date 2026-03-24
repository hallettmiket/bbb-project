# Agent HTML Output Rules

## Single Portal Page Per Agent
Each subagent must maintain exactly ONE HTML "portal" page that compiles all of its output. Agents must NOT open multiple Chrome tabs — only open their single portal page.

| Agent | Portal Path | Tab Color |
|-------|------------|-----------|
| Blacksmith | `./outputs/blacksmith/portal.html` | Green (#2E7D32) |
| Bookworm | `./outputs/bookworm/portal.html` | Bright Blue (#00AAFF) |
| Artist | `./outputs/artist/gallery.html` | Purple (#6A1B9A) |
| Adversary | `./outputs/adversary/portal.html` | Red (#C62828) |

## Portal Page Requirements
1. **Browser tab title** must include the agent emoji and name, e.g. `<title>⚒ BLACKSMITH — BBB Project</title>`
2. **Colored header bar** at the top using the agent's assigned color (full-width, white text, agent name + emoji)
3. **Content organized by round** — each round gets its own section heading (e.g., "Round 1 — Initial Data Analysis", "Round 2 — GUI & Literature")
4. **New rounds are appended** — do not overwrite previous rounds. The portal is a living document that accumulates all findings.
5. **All sub-documents embedded or linked** — individual reports (audit reports, literature summaries, figures) should be embedded inline or linked from within the portal. Do not open them in separate tabs.
6. **Only one `open -a "Google Chrome"` call per agent invocation** — and it must point to the portal page only.

## Styling
- Use a consistent CSS structure across all portals
- Header bar: full-width, 60px tall, agent color background, white bold text, agent emoji + name
- Round sections: clear heading with round number and title, horizontal rule between rounds
- Figures: embedded inline with `<img>` tags (not opened separately)
- The Artist's gallery.html serves as their portal — same rules apply
