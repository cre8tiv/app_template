import { StarterHome } from "@/components/starter-home";
import { hasSupabaseEnv } from "@/lib/supabase/env";

export default function Home() {
  return <StarterHome hasSupabaseEnv={hasSupabaseEnv()} />;
}
