import { redirect } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { hasSupabaseEnv } from "@/lib/supabase/env";
import { createClient } from "@/lib/supabase/server";

import { signOut } from "../login/actions";

export default async function ProtectedPage() {
  if (!hasSupabaseEnv()) {
    return (
      <main className="mx-auto flex min-h-screen w-full max-w-2xl flex-col justify-center px-6 py-16">
        <Card>
          <h1 className="text-2xl font-semibold">Protected page</h1>
          <p className="mt-3 text-sm text-zinc-600 dark:text-zinc-300">
            Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in
            .env.local to try this example.
          </p>
        </Card>
      </main>
    );
  }

  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login");
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-2xl flex-col justify-center px-6 py-16">
      <Card>
        <h1 className="text-2xl font-semibold">Protected page</h1>
        <p className="mt-3 text-sm text-zinc-600 dark:text-zinc-300">
          This page redirects to <code>/login</code> unless a Supabase session
          is present. Signed in as{" "}
          <span className="font-medium">{user.email}</span>.
        </p>
        <form action={signOut} className="mt-6">
          <Button type="submit" variant="secondary">
            Log out
          </Button>
        </form>
      </Card>
    </main>
  );
}
