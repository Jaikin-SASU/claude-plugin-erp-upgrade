import type { ErpFacts } from "../lib/types.js";
import {
  fold,
  formatFact,
  resolveVendor,
  takeFacts,
  unknownVendor,
} from "../lib/helpers.js";

export function vendorFacts(
  data: ErpFacts,
  args: { vendor: string; topic?: string },
) {
  const vendor = resolveVendor(data, args.vendor);
  if (!vendor) {
    return unknownVendor(args.vendor, data);
  }

  const topicFilter = args.topic ? fold(args.topic) : undefined;
  const selected = topicFilter
    ? vendor.facts.filter((f) => fold(f.topic) === topicFilter)
    : vendor.facts;

  return {
    vendor_id: vendor.id,
    vendor_name: vendor.name,
    facts: takeFacts(selected).map(formatFact),
  };
}
