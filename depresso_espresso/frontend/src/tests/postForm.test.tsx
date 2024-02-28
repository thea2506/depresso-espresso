import { describe, expect, test } from "vitest";
import { render, screen } from "@testing-library/react";
import { Button } from "../components/Button";

describe("Accordion test", () => {
  test("should show title all the time", () => {
    render(
      <Button
        title="Testing"
        buttonType="text"
      >
        <p>Content</p>
      </Button>
    );

    expect(screen.getByText(/Testing/i)).toBeDefined();
  });
});
