---
name: app-conventions
description: Conventions for scaffolding new features in this Next.js + Tailwind + Supabase starter template. Use whenever adding a new page, route handler, server action, Supabase-backed feature, or UI component in this repo, so new code matches the existing client/server split, UI kit, and auth patterns instead of inventing new ones.
---

# App template conventions

This repo is a Next.js (App Router) + TypeScript + Tailwind CSS v4 + Supabase starter. Follow these conventions when adding to it so new code matches what's already here.

## Supabase clients — pick the right one

Three factories live in `lib/supabase/`, each for a different execution context:

- `lib/supabase/client.ts` (`createClient`) — Client Components only (`"use client"`).
- `lib/supabase/server.ts` (`createClient`, async) — Server Components, Server Actions, Route Handlers. Always `await` it.
- `lib/supabase/middleware.ts` (`updateSession`) — only called from `proxy.ts`. Don't call it elsewhere.

Never import the browser client into server code or vice versa — the import path (`@/lib/supabase/client` vs `@/lib/supabase/server`) is the tell.

Before doing anything Supabase-schema-related (tables, RLS, migrations, indexes, functions), use the `supabase` and `supabase-postgres-best-practices` skills — this file only covers the Next.js-side conventions.

## Env vars

`lib/supabase/env.ts` is the only place that reads `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY`.

- Use `hasSupabaseEnv()` (never throws) to conditionally render UI when Supabase might not be configured yet — see `app/protected/page.tsx` for the pattern.
- Use `getSupabaseConfig()` / the client factories (which throw if env is missing) only where Supabase access is required to proceed.
- If a new required env var is added, add it to `.env.example` and to the `env:` block in `.github/workflows/ci.yml`.

## Auth pattern

`app/login/actions.ts` holds the `"use server"` actions (`login`, `signup`, `signOut`). Follow this pattern for new mutations tied to a page:

- Colocate server actions in an `actions.ts` file next to the `page.tsx` that uses them.
- Guard with `hasSupabaseEnv()` first and `redirect()` with a friendly `?error=` message rather than letting `getSupabaseConfig()` throw.
- Use `revalidatePath("/", "layout")` after auth state changes, then `redirect()`.
- A `<form>` can have multiple submit buttons with different `formAction={serverAction}` values instead of one action per form (see `app/login/page.tsx`).
- Protect a page by checking `supabase.auth.getUser()` in the Server Component and `redirect("/login")` if there's no user (see `app/protected/page.tsx`). Do this per-page, not by trying to centralize it in `proxy.ts` — the middleware only refreshes the session cookie.

## UI primitives

Reusable, typed, Tailwind-only components live in `components/ui/` (`Button`, `Input`, `Label`, `Card`). Each:

- Wraps the native HTML element's attribute type (e.g. `ButtonHTMLAttributes<HTMLButtonElement>`) plus any variant props — no new prop conventions.
- Merges classes with `cn()` from `lib/cn.ts` (a plain filter+join, no dependency) so callers can override styles via `className`.

Reach for these before writing new one-off `className` strings for buttons, inputs, labels, or bordered/padded containers. Extend an existing primitive (e.g. add a variant) rather than creating a parallel one.

## Tests

Vitest + Testing Library + jsdom. Test files sit next to the code they test (`components/starter-home.test.tsx` next to `starter-home.tsx`). New components/pages with non-trivial logic should get a colocated `*.test.tsx`.

## Before considering a change done

Run, in this order: `npm run lint`, `npm run typecheck`, `npm run format:check`, `npm run test`, `npm run build`. CI (`.github/workflows/ci.yml`) runs the same steps with placeholder Supabase env vars, `main` requires the `build` job to pass before merge, and `.husky/pre-push` runs lint/typecheck/test locally before every push — a change that fails one of these locally will fail CI or be blocked from pushing.

Before opening a PR, use [[pr-review]] for a stack-specific review pass.
