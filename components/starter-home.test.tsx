import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { StarterHome } from "./starter-home";

describe("StarterHome", () => {
  it("renders setup guidance when Supabase is not configured", () => {
    render(<StarterHome hasSupabaseEnv={false} />);

    expect(
      screen.getByRole("heading", {
        name: /starter template for shipping a supabase-backed next\.js app fast/i,
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        /supabase environment variables are not configured yet/i,
      ),
    ).toBeInTheDocument();
  });
});
