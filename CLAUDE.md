# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev             # Start Next.js dev server
npm run build            # Production build
npm run start             # Run production server
npm run lint              # ESLint
npm run typecheck          # next typegen && tsc --noEmit
npm run format             # Prettier write
npm run format:check        # Prettier check
npm run test               # Run all tests once (Vitest)
npm run test:watch          # Vitest watch mode
npm run supabase:start      # Start local Supabase stack (requires Docker)
npm run supabase:status     # Inspect local Supabase stack
npm run supabase:stop       # Stop local Supabase stack
```

Run a single test file: `npx vitest run components/starter-home.test.tsx`
Run tests matching a name: `npx vitest run -t "renders setup guidance"`

Local dev requires `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` in `.env.local` — copy `.env.example` and fill in values (from `npm run supabase:start` output, or a hosted Supabase project).

**Enforcement**: `.husky/pre-push` runs lint, typecheck, and test before every `git push`. `.github/workflows/ci.yml` runs lint, typecheck, format:check, test, and build with placeholder Supabase env vars on every push/PR. The `main` branch requires the `build` CI job to pass before merge (branch protection, `enforce_admins: true` — no bypass). Use the `pr-review` skill for a stack-specific review pass before opening a PR.

## Architecture

This is a minimal Next.js (App Router) + TypeScript + Tailwind CSS v4 + Supabase starter template, not yet a full application. Key structural points for extending it:

- **`lib/supabase/`** holds three separate Supabase client factories, each for a different execution context — do not mix them up:
  - `client.ts` — browser client (`createBrowserClient`), for use in Client Components.
  - `server.ts` — server client (`createServerClient`) bound to Next's `cookies()`, for use in Server Components/Actions/Route Handlers. It swallows cookie-set errors because Server Components can't set cookies (silently no-ops when called outside a Server Action/Route Handler).
  - `middleware.ts` — `updateSession()`, used by `proxy.ts` (the Next.js middleware entry point) to refresh the auth session on every matched request and propagate updated cookies onto the response.
  - `env.ts` — single source of truth for reading/validating the two required Supabase env vars. `hasSupabaseEnv()` checks presence without throwing; `getSupabaseConfig()` throws if either var is missing. Use `hasSupabaseEnv()` for conditional UI/logic, `getSupabaseConfig()` when Supabase access is required.
- **`proxy.ts`** is the Next.js middleware file (Next 16 renamed `middleware.ts` to `proxy.ts`; the exported function is `proxy`, not `middleware`). Its `matcher` excludes `_next/static`, `_next/image`, `favicon.ico`, and static image extensions — update this matcher, not a separate `middleware.ts`, if route matching needs to change.
- **`supabase/config.toml`** configures the local Supabase CLI stack (ports, auth settings, storage limits). Local Postgres runs on port 54322, Studio on 54323, API on 54321.
- Path alias `@/*` maps to the repo root (see `tsconfig.json`), e.g. `@/lib/supabase/env`.
- Tests use Vitest + Testing Library + jsdom (`vitest.config.mts`), with `@testing-library/jest-dom` matchers loaded globally via `vitest.setup.ts`. Test files live next to the code they test (e.g. `components/starter-home.test.tsx`).
- Tailwind v4 is configured via `@tailwindcss/postcss` (no separate `tailwind.config.js`); global styles are in `app/globals.css`.
- **`components/ui/`** has typed Tailwind primitives (`Button`, `Input`, `Label`, `Card`) merged via `cn()` (`lib/cn.ts`). Extend these instead of writing new one-off styled elements.
- **Auth example**: `app/login/page.tsx` + `app/login/actions.ts` (server actions `login`/`signup`/`signOut`), `app/auth/callback/route.ts` (OAuth/email-link code exchange), and `app/protected/page.tsx` (redirects to `/login` if `supabase.auth.getUser()` has no user). This is the reference pattern for new Supabase-backed pages — see `.claude/skills/app-conventions/SKILL.md` for the full conventions (which client to use where, action colocation, protecting pages, etc.).
- `vitest.config.mts` aliases `@` to the repo root for Vite/Vitest, since Vite doesn't read `tsconfig.json` paths on its own.
- `npm run typecheck` runs `next typegen` first — `LayoutProps<"/">`/`PageProps<"/login">` (Next's typed-routes ambient types) only exist after a build or `next typegen`/`next dev` has run at least once; a bare `tsc --noEmit` on a clean checkout fails without it.
