import { formatName } from "../src/format";

describe("formatName", () => {
  it("joins names with a space", () => {
    expect(formatName("Ada", "Lovelace")).toBe("Ada Lovelace");
  });
});
