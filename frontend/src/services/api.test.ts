import { beforeEach, expect, test, vi } from "vitest";

const { get } = vi.hoisted(() => ({ get: vi.fn() }));
vi.mock("axios", () => ({ default: { create: () => ({ get }) } }));
import { apiService } from "./api";

beforeEach(() => get.mockReset());

test("loads compounds and preserves their stable IDs", async () => {
  get.mockResolvedValue({ data: [{ id: "ethene", name: "Ethene", formula: "CH2=CH2" }] });
  const compounds = await apiService.getCompounds("eth");
  expect(get).toHaveBeenCalledWith("/compounds/", { params: { search: "eth" } });
  expect(compounds[0].id).toBe("ethene");
  expect(compounds[0].properties?.name).toBe("Ethene");
});

test("normalizes each compound in a returned path", async () => {
  get.mockResolvedValue({ data: [{ compounds: [{ id: "ethene", name: "Ethene", formula: "CH2=CH2" }], reactions: [], reagents: [], total_steps: 0, teaching_cost: 0 }] });
  const paths = await apiService.findPaths("ethene", "ethanol", 4);
  expect(get).toHaveBeenCalledWith("/paths/", { params: { start: "ethene", end: "ethanol", max_steps: 4 } });
  expect(paths[0].compounds[0].properties?.name).toBe("Ethene");
});
