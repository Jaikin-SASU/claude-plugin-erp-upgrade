import {
  MAX_FACTS,
  type ErpFacts,
  type Fact,
  type FormattedFact,
  type Odoo20Change,
  type UnknownVendor,
  type Vendor,
} from "./types.js";

/** Map folded aliases to canonical vendor ids. */
const VENDOR_ALIASES: Record<string, string> = {
  bc: "business-central",
  "business central": "business-central",
  dynamics: "business-central",
  "sap b1": "sap-business-one",
  sap: "sap-business-one",
  "sage 100": "sage",
  "sage x3": "sage",
};

export function fold(text: string): string {
  return text
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .toLowerCase();
}

export function formatFact(
  fact: Pick<Fact, "statement" | "source_url" | "certainty" | "volatile">,
): FormattedFact {
  const base: FormattedFact = {
    statement: fact.statement,
    source_url: fact.source_url,
    certainty: fact.certainty,
  };
  if (fact.volatile) {
    return { ...base, volatile: true, note: "re-check live" };
  }
  return { ...base, volatile: false };
}

export function takeFacts<T>(items: readonly T[]): T[] {
  return items.slice(0, MAX_FACTS);
}

export function vendorIds(data: ErpFacts): string[] {
  return data.vendors.map((v) => v.id);
}

export function unknownVendor(query: string, data: ErpFacts): UnknownVendor {
  return {
    message: `no sourced facts for ${query}; verify on the vendor's official pages`,
    available_vendor_ids: vendorIds(data),
  };
}

export function resolveVendor(
  data: ErpFacts,
  query: string,
): Vendor | undefined {
  const q = fold(query.trim());
  if (!q) return undefined;

  const aliased = VENDOR_ALIASES[q];
  if (aliased) {
    return data.vendors.find((v) => v.id === aliased);
  }

  const byId = data.vendors.find((v) => fold(v.id) === q);
  if (byId) return byId;

  const byNameExact = data.vendors.find((v) => fold(v.name) === q);
  if (byNameExact) return byNameExact;

  return data.vendors.find(
    (v) => fold(v.name).includes(q) || q.includes(fold(v.id)),
  );
}

export function topicsFor(vendor: Vendor): string[] {
  return [...new Set(vendor.facts.map((f) => f.topic))].sort();
}

export function sourceLine(urls: readonly string[], checkedOn: string): string {
  const unique = [...new Set(urls.filter(Boolean))];
  return `source: ${unique.join(" ")} · checked ${checkedOn}`;
}

export function urlsFromFacts(
  facts: readonly { source_url: string }[],
): string[] {
  return [...new Set(facts.map((f) => f.source_url))];
}

export function formatOdooChange(change: Odoo20Change): FormattedFact & {
  area: string;
} {
  return {
    area: change.area,
    ...formatFact(change),
  };
}
