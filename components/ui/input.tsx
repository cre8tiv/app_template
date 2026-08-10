import type { InputHTMLAttributes } from "react";

import { cn } from "@/lib/cn";

type InputProps = InputHTMLAttributes<HTMLInputElement>;

export function Input({ className, ...props }: InputProps) {
  return (
    <input
      className={cn(
        "w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-zinc-400 focus:outline-none dark:border-white/10 dark:bg-zinc-950 dark:text-zinc-100 dark:focus:border-zinc-500",
        className,
      )}
      {...props}
    />
  );
}
