# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state of the repository

This repository is in its **initial, pre-implementation state**. As of this writing it contains only:

- `README.md` — a single line with the project title (`Home-schooling-App`)
- `CLAUDE.md` — this file

There is **no source code, build system, dependency manifest, test suite, or tooling configuration yet**. No language or framework has been chosen. Treat the project name as the only signal of intent: a homeschooling application.

Because nothing has been built, there are intentionally **no build / lint / test commands documented here** — there is nothing to run. Do not invent them.

## When you add the first real code

The first substantive change to this repo defines its architecture. When that happens, update this file in the same change so it stays accurate. At minimum, document:

1. **Commands** — how to install dependencies, build, run, lint, and test, including how to run a *single* test once a test runner exists.
2. **Architecture** — the big-picture structure that spans multiple files and isn't obvious from a directory listing (entry points, how the app is wired together, data flow, and any non-obvious conventions).

Keep this file honest: describe only what actually exists in the tree, not aspirations.

## Git workflow conventions

- The default branch is `main`.
- Development for the current task happens on the branch `claude/claude-md-docs-8kudj5`. Do not push directly to `main` without explicit instruction.
- Do not open a pull request unless explicitly asked.
