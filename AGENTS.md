# Repository Agent Guidance

## Sources of truth

- `.codex/config.toml` registers the available Codex agents, their model routing, and IC worktree isolation.
- `.codex/agents/*.toml` is the authoritative definition of each agent's remit and operating instructions. Update the relevant TOML file when a role changes; do not duplicate role prompts here.
- `CLAUDE.md` contains repository commands, architecture, and verification conventions. Read it before implementing or reviewing code.

## Agent routing

- `tech-lead`: decompose a multi-IC goal, coordinate work, track Jira/PR state, and report status.
- `ic-generalist`: own one well-scoped full-stack, refactoring, or investigation task.
- `ic-specialist-backend`: own backend, API, database, migration, performance, or security work.
- `code-reviewer`: independently review an IC's completed change before integration.

For multi-agent work, the tech lead assigns independent tasks to ICs, routes each completed PR to `code-reviewer`, and merges only after an approving verdict. The ticket moves to Done only after review passes and the PR merges.

## Repository-wide working agreements

- Use PowerShell for terminal commands on this Windows workspace.
- Codex ICs work in their configured isolated worktrees on ticket-named branches, open a PR, and never merge directly to `main`.
- Claude agent teams do not provide automatic worktree isolation. Claude ICs must use separate worktrees for parallel Git mutations, or serialize those mutations.
- Keep task scopes explicit: affected files or area, acceptance criteria, dependencies, and verification expectations.
- Coordinate through Codex collaboration tools and direct agent messages. Jira and PRs are the durable delivery record; a telemetry file is optional, human-facing, and owned by the tech lead alone.

## When to update agent configuration

When adding, removing, renaming, or materially changing an agent, update both `.codex/config.toml` and its `.codex/agents/<agent>.toml` definition. Update this file only if the shared routing, repository-wide workflow, or source-of-truth locations change.
