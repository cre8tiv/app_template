---
name: pr-review
description: Stack-specific PR/diff review for this Next.js + Supabase + Tailwind starter template. Use when the user asks to review a PR, review a branch, or review the current diff in this repo — complements the general-purpose code-review skill with checks specific to this template's conventions (Supabase client boundaries, auth guards, UI primitive reuse, RLS). Also use before opening a PR to sanity-check changes.
---

# PR review for this template

Review the diff (working tree, a branch vs `main`, or a given PR number) against both general correctness and this template's stack-specific conventions. See [[app-conventions]] for the conventions themselves — this skill is the review checklist derived from them.

## 1. Run the gate commands first

Before reviewing code, confirm the change actually passes what CI and the pre-push hook (`.husky/pre-push`) enforce:

```bash
npm run lint
npm run typecheck
npm run format:check
npm run test
npm run build
```

If any fail, that's the top finding — report it before anything stylistic. Don't hand-wave "should pass CI"; run the commands.

## 2. Stack-specific checklist

Walk the diff against these, in addition to normal correctness/simplification review:

**Supabase client boundaries**

- `@/lib/supabase/client` (browser) only imported from files with `"use client"`.
- `@/lib/supabase/server` (async `createClient`) only used in Server Components, Server Actions, or Route Handlers, and always `await`ed.
- `lib/supabase/middleware.ts` (`updateSession`) is not called anywhere except `proxy.ts`.

**Env var handling**

- Any new code that needs Supabase either goes through `hasSupabaseEnv()` for a friendly degraded state, or accepts that `getSupabaseConfig()`/`createClient()` will throw when unconfigured — flag it if a page/action skips this and would crash ungracefully instead of redirecting or messaging.
- New required env vars are added to `.env.example` and to the `env:` block in `.github/workflows/ci.yml`.

**Auth & route protection**

- A new page meant to require a session checks `supabase.auth.getUser()` server-side and `redirect("/login")` — don't rely on `proxy.ts`/middleware alone to gate access (it only refreshes the session cookie, it doesn't block routes).
- New Server Actions that mutate auth or user data are colocated in an `actions.ts` next to the page, marked `"use server"`, and call `revalidatePath(...)` before `redirect(...)` where state visibly changes.

**UI consistency**

- New buttons/inputs/labels/cards use `components/ui/*` (extending with a variant if needed) rather than new one-off Tailwind class strings duplicating existing primitives.
- Class merging goes through `cn()` from `lib/cn.ts`, not manual template-literal concatenation.

**Local Supabase config**

- Ports in `supabase/config.toml` stay as `env(SUPABASE_*_PORT)` references, not hardcoded numbers — a hardcoded port reintroduces the multi-instance collision the current setup avoids.
- Any `supabase` CLI invocation added to scripts/docs goes through `npm run supabase -- <command>` (or the `supabase:*` scripts), not a bare `supabase` call — bare calls skip `scripts/supabase.mjs` and will fail to parse config unless every `SUPABASE_*_PORT` var happens to already be set.

**Database changes**

- Any change under `supabase/` (migrations, schema) — hand off to the `supabase-postgres-best-practices` skill for the schema/RLS-level review; this skill only flags that such a review is needed, it doesn't replace it.
- New tables have RLS enabled and policies scoped to the right role, not left open by default.

**Tests**

- New non-trivial components/pages/actions have a colocated `*.test.tsx`/`*.test.ts` (see `components/starter-home.test.tsx` for the pattern).

## 3. Report

Use the same severity-ordered format as the general `code-review` skill: most severe first, concrete failure scenario per finding, and call out anything from the gate-command run as the highest-priority item if it failed.
