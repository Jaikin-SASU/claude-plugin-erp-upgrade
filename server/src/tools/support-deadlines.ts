import type { ErpFacts, FormattedFact, Vendor } from "../lib/types.js";
import {
  formatFact,
  resolveVendor,
  takeFacts,
  unknownVendor,
} from "../lib/helpers.js";
import { MAX_FACTS } from "../lib/types.js";

function deadlineFacts(vendor: Vendor): FormattedFact[] {
  return vendor.facts
    .filter((f) => f.topic === "support_deadlines")
    .map(formatFact);
}

export function supportDeadlines(
  data: ErpFacts,
  args: { vendor?: string },
) {
  if (args.vendor) {
    const vendor = resolveVendor(data, args.vendor);
    if (!vendor) {
      return unknownVendor(args.vendor, data);
    }
    return {
      vendors: [
        {
          id: vendor.id,
          name: vendor.name,
          facts: takeFacts(deadlineFacts(vendor)),
        },
      ],
    };
  }

  const rows: { id: string; name: string; facts: FormattedFact[] }[] = [];
  let remaining = MAX_FACTS;
  for (const vendor of data.vendors) {
    if (remaining <= 0) break;
    const facts = deadlineFacts(vendor);
    if (facts.length === 0) continue;
    const sliced = facts.slice(0, remaining);
    remaining -= sliced.length;
    rows.push({ id: vendor.id, name: vendor.name, facts: sliced });
  }
  return { vendors: rows };
}
