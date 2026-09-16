---
name: init-app
description: One-time customization pass for a freshly cloned copy of this Next.js + Supabase starter template — renames the app, remaps local Supabase ports if they collide, and updates the README. Use the first time an agent (Claude, Codex, or otherwise) works in a copy of this template where package.json's name is still the placeholder "app_template", or when the user asks to "initialize", "set up", or "customize" this template for a new app.
---

# Initialize this template for a new app

This template ships with placeholder identity (`app_template`) so it can be cloned repeatedly. This skill runs once per clone to turn it into a specific app.

## 0. Check whether this has already run

Read `package.json`. If `name` is no longer `"app_template"` (or a placeholder like `"app-template"`), initialization already happened — tell the user and ask whether they want to re-run specific steps (e.g. just the port remap) rather than redoing everything blind.

## 1. Ask the user for the app identity

Ask (one question, or a couple if needed):

- **App name** — a human-readable name (e.g. "Acme Invoicing"). Derive an npm-safe slug from it: lowercase, spaces/underscores → hyphens, strip anything not `[a-z0-9-]`.
- **Short one-line description**, if they want one in the README. Optional — skip if they don't have one yet, don't block on it.

Don't ask about things you can decide yourself (port numbers, file names) — only ask what's genuinely the user's call.

## 2. Rename the app

- `package.json`: set `"name"` to the slug.
- `supabase/config.toml`: set `project_id = "<slug>"` (line 1). This is what namespaces the local Supabase Docker containers — leaving it as `app-template` is what causes container-name collisions when someone runs two clones of this template side by side, which is the exact problem the env-var port mapping in this file already solves for ports.
- `README.md`: replace the `# App Template` title with the app name, and the one-line description under it with the user's description (or leave the existing generic sentence if they didn't give one). Also update the Mailpit URL in the "Included" list to use the configured `SUPABASE_MAILPIT_PORT` (default `54324`) instead of a hardcoded port — e.g. `http://127.0.0.1:${SUPABASE_MAILPIT_PORT}`. Leave the rest of the README (setup steps, scripts, quality gates) as-is — it's still accurate.

## 3. Check for local Supabase port collisions

Default ports (from `scripts/supabase.mjs`): `SUPABASE_API_PORT=54321`, `SUPABASE_DB_PORT=54322`, `SUPABASE_DB_SHADOW_PORT=54320`, `SUPABASE_STUDIO_PORT=54323`, `SUPABASE_MAILPIT_PORT=54324`.

Check each with PowerShell, e.g.:

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 54321 -InformationLevel Quiet
```

or `Get-NetTCPConnection -LocalPort 54321 -ErrorAction SilentlyContinue`. This matters most when another clone of this template (or another app) is already running its own local Supabase stack.

If any port is taken:

- Pick a free replacement (e.g. bump by 10, re-check, repeat until free). Each candidate must be distinct from **every** configured Supabase port and from all replacements already selected for other colliding ports in this pass — not just not actively listening. Re-check and increment until a globally unused port is found.
- Create `.env.local` from `.env.example` if it doesn't exist yet.
- Uncomment and set the colliding `SUPABASE_*_PORT` var(s) in `.env.local` to the new value(s).
- If `SUPABASE_API_PORT` changed, also update `NEXT_PUBLIC_SUPABASE_URL` in `.env.local` to match (`http://127.0.0.1:<new port>`).

If nothing is taken, leave `.env.local` untouched (or don't create it) — the defaults in `scripts/supabase.mjs` already cover the no-collision case.

## 4. Report and hand back

Summarize what changed (renamed to `<slug>`, README updated, ports remapped or left default). Don't `git add`/`git commit` automatically — show the diff and let the user review and commit it themselves, since renaming and port remaps are the kind of change they'll want to glance at first.

Point them at [[app-conventions]] for ongoing feature work — this skill only handles one-time identity/config setup, not app features.
