import Link from "next/link";

import { Card } from "@/components/ui/card";

type StarterHomeProps = {
  hasSupabaseEnv: boolean;
};

const steps = [
  {
    title: "Configure environment variables",
    description:
      "Copy .env.example to .env.local and fill in your Supabase project URL and anon key.",
  },
  {
    title: "Run Supabase locally",
    description:
      "Install the Supabase CLI, make sure Docker is running, then use npm run supabase:start.",
  },
  {
    title: "Start building",
    description:
      "Use the browser and server Supabase helpers in lib/supabase for auth, data access, and SSR flows.",
  },
];

const commands = [
  "npm run dev",
  "npm run lint",
  "npm run format:check",
  "npm run test",
  "npm run supabase:start",
];

export function StarterHome({ hasSupabaseEnv }: StarterHomeProps) {
  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col gap-12 px-6 py-16">
      <Card className="rounded-3xl p-8">
        <div className="flex flex-wrap items-center gap-3">
          <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-sm font-medium text-emerald-700 dark:text-emerald-300">
            Next.js + Tailwind + Supabase
          </span>
          <span className="rounded-full bg-zinc-900 px-3 py-1 text-sm font-medium text-white dark:bg-zinc-100 dark:text-zinc-900">
            TypeScript ready
          </span>
        </div>
        <div className="mt-6 flex flex-col gap-4">
          <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-balance">
            Starter template for shipping a Supabase-backed Next.js app fast.
          </h1>
          <p className="max-w-2xl text-lg text-zinc-600 dark:text-zinc-300">
            This scaffold includes App Router, Tailwind CSS, linting, Prettier,
            Vitest, and Supabase helpers for browser, server, and middleware
            usage.
          </p>
        </div>
        <div
          className={`mt-6 rounded-2xl border px-4 py-3 text-sm ${
            hasSupabaseEnv
              ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-800 dark:text-emerald-200"
              : "border-amber-500/30 bg-amber-500/10 text-amber-800 dark:text-amber-200"
          }`}
        >
          {hasSupabaseEnv
            ? "Supabase environment variables are configured."
            : "Supabase environment variables are not configured yet. Copy .env.example to .env.local to get started."}
        </div>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            href="/login"
            className="rounded-xl bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-700 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-300"
          >
            View auth example
          </Link>
          <Link
            href="/protected"
            className="rounded-xl border border-black/10 bg-white px-4 py-2 text-sm font-medium text-zinc-900 hover:bg-zinc-50 dark:border-white/10 dark:bg-zinc-950 dark:text-zinc-100 dark:hover:bg-zinc-900"
          >
            View protected page example
          </Link>
        </div>
      </Card>

      <section className="grid gap-4 md:grid-cols-3">
        {steps.map((step) => (
          <Card key={step.title}>
            <h2 className="text-lg font-semibold">{step.title}</h2>
            <p className="mt-3 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
              {step.description}
            </p>
          </Card>
        ))}
      </section>

      <Card className="bg-zinc-50 dark:bg-zinc-900">
        <h2 className="text-lg font-semibold">Useful commands</h2>
        <ul className="mt-4 grid gap-3 sm:grid-cols-2">
          {commands.map((command) => (
            <li
              key={command}
              className="rounded-xl bg-white px-4 py-3 font-mono text-sm dark:bg-zinc-950"
            >
              {command}
            </li>
          ))}
        </ul>
      </Card>
    </main>
  );
}
