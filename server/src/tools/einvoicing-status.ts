import type { ErpFacts, FormattedFact, Vendor } from "../lib/types.js";
import {
  formatFact,
  resolveVendor,
  takeFacts,
  unknownVendor,
} from "../lib/helpers.js";

function einvoicingFacts(vendor: Vendor): FormattedFact[] {
  return takeFacts(
    vendor.facts.filter((f) => f.topic === "einvoicing"),
  ).map(formatFact);
}

export function einvoicingStatus(
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
          facts: einvoicingFacts(vendor),
        },
      ],
      einvoicing_france: formatFact(data.einvoicing_france),
    };
  }

  return {
    vendors: data.vendors.map((v) => ({
      id: v.id,
      name: v.name,
      facts: einvoicingFacts(v),
    })),
    einvoicing_france: formatFact(data.einvoicing_france),
  };
}
