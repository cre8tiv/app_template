# App Template

A starter template built with Next.js, TypeScript, Tailwind CSS, and Supabase.

## Included

- Next.js App Router
- TypeScript
- Tailwind CSS
- ESLint
- Prettier
- Vitest + Testing Library
- Supabase client helpers for browser, server, and proxy usage
- Local Supabase configuration in `/supabase`, with Mailpit catching auth emails at http://127.0.0.1:54324
- Email/password auth example (`/login`, `/protected`, `app/auth/callback`)
- Reusable UI primitives in `components/ui` (Button, Input, Label, Card)
- GitHub Actions CI (lint, typecheck, format check, test, build) required on `main` via branch protection
- Husky pre-push hook running lint, typecheck, and test before every push
- `.claude/skills/app-conventions` and `.claude/skills/pr-review` documenting this template's conventions and a stack-specific PR review checklist for Claude Code

## Local setup

1. Install dependencies:

   ```bash
   npm install
   ```

2. Copy the example environment file:

   ```bash
   cp .env.example .env.local
   ```

3. Start the Next.js dev server:

   ```bash
   npm run dev
   ```

## Run Supabase locally

Supabase local development uses Docker via the Supabase CLI.

### Windows (Scoop)

```powershell
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase
```

### Start and stop the local stack

```bash
npm run supabase:start
npm run supabase:status
npm run supabase:stop
```

After the stack starts, update `.env.local` with the URL and anon key for your project.

### Overriding local ports

`supabase/config.toml` reads its ports from environment variables instead of hardcoding them, so multiple instances of this template (or unrelated local services) can run side by side without `Bind for 0.0.0.0:PORT failed: port is already allocated` errors. `npm run supabase:*` runs the CLI through `scripts/supabase.mjs`, which supplies default ports and loads any overrides from `.env.local` first.

To change a port, uncomment and edit the relevant line in `.env.local` (see `.env.example`):

```
SUPABASE_API_PORT=54321
SUPABASE_DB_PORT=54322
SUPABASE_DB_SHADOW_PORT=54320
SUPABASE_STUDIO_PORT=54323
SUPABASE_MAILPIT_PORT=54324
```

If you change `SUPABASE_API_PORT`, update `NEXT_PUBLIC_SUPABASE_URL` to match. Always use `npm run supabase:start` / `:status` / `:stop` (or `npm run supabase -- <command>` for anything else) rather than calling `supabase` directly — every subcommand needs the same port env vars, not just `start`, or config parsing fails.

### Viewing emails sent by Supabase (Mailpit)

The local stack catches every email Supabase Auth would send (signup confirmations, password resets, magic links, email changes) instead of delivering it. View them at [http://127.0.0.1:54324](http://127.0.0.1:54324) while the stack is running — no inbox or real SMTP server needed.

## Auth example

`/login` demonstrates the Supabase email/password flow using server actions (`app/login/actions.ts`), and `/protected` demonstrates a page that redirects to `/login` when there's no session. `app/auth/callback/route.ts` handles the redirect used by email confirmation / OAuth code exchange. Use these as the starting point for real auth flows.

## UI primitives

`components/ui` has small, typed Tailwind components (`Button`, `Input`, `Label`, `Card`) used throughout the template. Prefer extending these over writing new one-off styled elements.

## Quality gates

- `.husky/pre-push` runs `lint`, `typecheck`, and `test` before every `git push` (installed automatically by `npm install` via the `prepare` script).
- `.github/workflows/ci.yml` runs `lint`, `typecheck`, `format:check`, `test`, and `build` on every push and PR, using placeholder Supabase env vars.
- The `main` branch requires the CI `build` job to pass before a PR can merge (GitHub branch protection, no admin bypass).

## Scripts

- `npm run dev` - start the Next.js dev server
- `npm run build` - create a production build
- `npm run start` - run the production server
- `npm run lint` - run ESLint
- `npm run typecheck` - generate route types and run `tsc --noEmit`
- `npm run format` - format files with Prettier
- `npm run format:check` - verify Prettier formatting
- `npm run test` - run tests once
- `npm run test:watch` - run tests in watch mode
- `npm run supabase:start` - start local Supabase services
- `npm run supabase:status` - inspect the local Supabase stack
- `npm run supabase:stop` - stop local Supabase services
