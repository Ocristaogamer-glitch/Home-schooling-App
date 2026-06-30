# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A homeschooling app for kids focused on creativity, autonomy, and project-based
learning (not quizzes/rote memorization). It is built to run **entirely on an
Android phone via Pydroid 3**, so the whole app is a single self-contained
`main.py` using the standard-library **Tkinter** GUI — no external/compiled
dependencies.

## Running

- Target runtime is **Pydroid 3** on Android: open `main.py` and press Play.
- On desktop: `python3 main.py` (requires a Tk-capable Python; the headless CI
  container here has no `tkinter`, so the GUI cannot launch — validate with
  `python3 -m py_compile main.py` and test data logic in isolation instead).
- No build step, no package manager, no test framework. The only dependency is
  the Python standard library (`tkinter`, `json`, `os`, `datetime`).

## Architecture (`main.py`)

Single file, one `App(tk.Tk)` root with a persistent bottom nav bar switching
between three screens stacked in a shared container:

- `HubScreen` — "Missões": list of creative project cards; advance status
  (`A fazer → Fazendo → Concluida`) or mark done; add custom missions via
  `MissionDialog` (a `Toplevel` form).
- `PortfolioScreen` — student writes/saves "conquistas", optionally tied to a
  mission; entries are listed newest-first and deletable.
- `ParentScreen` — read-only report: overall progress bar, per-area
  completion, counts, recent portfolio entries, editable student name.

Cross-cutting pieces:

- **Persistence:** all state lives in one dict (`aluno`, `missoes`,
  `portfolio`) saved to `homeschool_data.json` next to the script.
  `load_data()` auto-creates the file, seeds `DEFAULT_MISSIONS` on first run,
  and tolerates a missing/corrupt JSON file (falls back to defaults rather than
  crashing). Every mutation calls `App.persist()` then re-renders the screen.
- **Screens** subclass `tk.Frame`, expose a `refresh()` that rebuilds their
  content from `app.data`; `App.show(key)` calls `refresh()` on display so data
  edits propagate across screens.
- **`Scrollable`** is the reusable scroll container (Canvas + inner frame). It
  supports finger-drag panning via `scan_mark`/`scan_dragto` plus mouse wheel,
  which is the touch-scroll mechanism on Pydroid. When adding child widgets to
  a scroll area, call `bind_touch(widget)` on them so drags over content still
  scroll.

## Conventions

- Keep everything in `main.py` and stdlib-only — adding compiled/external
  deps breaks the one-tap Pydroid workflow.
- UI is a fixed dark palette defined as module constants at the top
  (`BG`, `CARD`, `PRIMARY`, area/status color maps); large fonts and big
  padded `big_button(...)` controls for touch.
- User-facing strings are Portuguese (pt-BR) and intentionally avoid accented
  characters in code literals to dodge Pydroid encoding quirks.
- Status values and their order live in `STATUS_FLOW`; mission categories and
  their colors in `AREA_COLORS`. Reuse these rather than hardcoding.

## Git workflow

- Default branch `main`; current work on `claude/claude-md-docs-8kudj5`.
- Don't push to `main` or open PRs without explicit instruction.
