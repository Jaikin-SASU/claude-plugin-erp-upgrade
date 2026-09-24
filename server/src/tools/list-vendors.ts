import type { ErpFacts } from "../lib/types.js";
import { topicsFor } from "../lib/helpers.js";

export function listVendors(data: ErpFacts) {
  return {
    vendors: data.vendors.map((v) => ({
      id: v.id,
      name: v.name,
      fact_count: v.facts.length,
      topics: topicsFor(v),
    })),
  };
}
