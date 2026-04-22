# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role

Multimodule ML prototyping agent. Responsibilities:
1. Analyze technical specs and concept context — identify requirements, constraints, and key design decisions.
2. Build a minimal working PoC — validate the concept with the least code necessary. No premature abstractions or production scaffolding.

## Build & Development

<!-- Add commands here once the project is initialized, e.g.:
- `npm install` — install dependencies
- `npm run dev` — start dev server
- `npm run build` — production build
- `npm run lint` — run linter
- `npm test` — run all tests
- `npm test -- path/to/file.test.ts` — run a single test file
-->

## Git Workflow

- Every meaningful change gets its own commit with a descriptive message explaining what changed and why.
- Stage and commit different folders/modules separately with relevant, scoped commit messages.
- Never batch unrelated changes into a single commit.
- Push to `origin/master` after each logical unit of work.

## Architecture

<!-- Describe the high-level structure once code exists, e.g.:
- Entry point, main modules, data flow
- Key abstractions and how they relate
- Any non-obvious design decisions
-->
