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
- Local Supabase configuration in `/supabase`

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

## Scripts

- `npm run dev` - start the Next.js dev server
- `npm run build` - create a production build
- `npm run start` - run the production server
- `npm run lint` - run ESLint
- `npm run format` - format files with Prettier
- `npm run format:check` - verify Prettier formatting
- `npm run test` - run tests once
- `npm run test:watch` - run tests in watch mode
- `npm run supabase:start` - start local Supabase services
- `npm run supabase:status` - inspect the local Supabase stack
- `npm run supabase:stop` - stop local Supabase services
