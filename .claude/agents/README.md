# Starter setup: one project, small team

## What this is
A tech lead + 2 ICs (one generalist, one backend specialist) for a single project. 

## Setup

1. Copy these three `.md` files into your project's `.claude/agents/` directory:
   ```
   cp tech-lead.md ic-generalist.md ic-specialist-backend.md /path/to/project/.claude/agents/
   ```

2. Enable agent teams for the session:
   ```
   export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
   claude
   ```

3. Pre-approve common permissions (file edits, bash in project dir) in your Claude Code settings so teammates don't stall on prompts that bubble up to you.

4. Kick it off by talking to the main session as if it's the tech lead — or explicitly:
   ```
   Spawn a teammate using the tech-lead agent type to own [project/goal].
   ```
   The tech lead will then spawn ICs itself, referencing `ic-generalist` or `ic-specialist-backend` by name as tasks come up.

## How to interact day to day

- Talk to the tech lead, not the ICs. Give it goals, not implementation steps.
- Check `/tasks` (or your task list view) periodically instead of asking for status — it's more accurate than a summary.
- If a teammate stalls (check the agent panel), the tech lead should notice and respawn — if it doesn't within a reasonable window, nudge it directly.

## When to expand

- Add a `pm` role instead of overloading tech-lead with product decisions, once you notice the lead making product calls it shouldn't.
- Add more IC specialties (frontend, infra, test) as tasks pile up in one lane.
- Only add the second top-level lead + mutual-restart layer once you're running multiple projects in parallel and the single-lead check-in load gets heavy — it's not worth the complexity for one project.

## Costs to watch
Each teammate is a full Claude instance with its own context window. A 3-agent team (lead + 2 ICs) running for a day is meaningfully more token spend than one Claude Code session — worth watching usage for the first week before deciding whether to scale wider.
