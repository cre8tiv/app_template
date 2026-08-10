#!/usr/bin/env node
// Wrapper around the Supabase CLI that guarantees the port env vars
// referenced by supabase/config.toml (via env(...)) are always set, loading
// overrides from .env.local first. Without this, `supabase <any command>`
// fails to parse the config whenever one of those vars is missing.
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const repoRoot = path.resolve(fileURLToPath(import.meta.url), "../..");

const DEFAULT_PORTS = {
  SUPABASE_API_PORT: "54321",
  SUPABASE_DB_PORT: "54322",
  SUPABASE_DB_SHADOW_PORT: "54320",
  SUPABASE_STUDIO_PORT: "54323",
  SUPABASE_MAILPIT_PORT: "54324",
};

function loadEnvLocal() {
  const envPath = path.join(repoRoot, ".env.local");
  if (!existsSync(envPath)) return;

  for (const line of readFileSync(envPath, "utf8").split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;

    const eq = trimmed.indexOf("=");
    if (eq === -1) continue;

    const key = trimmed.slice(0, eq).trim();
    const value = trimmed
      .slice(eq + 1)
      .trim()
      .replace(/^['"]|['"]$/g, "");

    if (process.env[key] === undefined) {
      process.env[key] = value;
    }
  }
}

loadEnvLocal();

for (const [key, value] of Object.entries(DEFAULT_PORTS)) {
  if (process.env[key] === undefined) {
    process.env[key] = value;
  }
}

const result = spawnSync("supabase", process.argv.slice(2), {
  stdio: "inherit",
  env: process.env,
  shell: true,
});

process.exit(result.status ?? 1);
