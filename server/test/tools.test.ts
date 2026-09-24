import { describe, expect, it } from "vitest";
import factsJson from "../src/data/erp-facts.json";
import type { ErpFacts, Fact, Vendor } from "../src/lib/types.js";
import { MAX_FACTS, GITHUB_REPO, SITE_URL, VOLATILE_RULE } from "../src/lib/types.js";
import { listVendors } from "../src/tools/list-vendors.js";
import { vendorFacts } from "../src/tools/vendor-facts.js";
import { einvoicingStatus } from "../src/tools/einvoicing-status.js";
import { supportDeadlines } from "../src/tools/support-deadlines.js";
import { odoo20Changes } from "../src/tools/odoo-20-changes.js";
import { sourcesAndMethod } from "../src/tools/sources-and-method.js";

const data = factsJson as ErpFacts;

function oversizedVendor(id: string, n: number): Vendor {
  const facts: Fact[] = Array.from({ length: n }, (_, i) => ({
    topic: i % 2 === 0 ? "pricing" : "migration",
    statement: `fact-${i}`,
    source_url: `https://example.com/${i}`,
    certainty: "official",
    volatile: i === 0,
  }));
  return { id, name: id, facts };
}

function withExtraVendor(vendor: Vendor): ErpFacts {
  return { ...data, vendors: [...data.vendors, vendor] };
}

describe("list_vendors", () => {
  it("returns id, name, fact count and topics", () => {
    const result = listVendors(data);
    expect(result.vendors.length).toBe(data.vendors.length);
    const odoo = result.vendors.find((v) => v.id === "odoo");
    expect(odoo).toMatchObject({
      id: "odoo",
      name: "Odoo (Community / Enterprise)",
      fact_count: data.vendors.find((v) => v.id === "odoo")!.facts.length,
    });
    expect(odoo?.topics).toContain("pricing");
    expect(odoo?.topics).toContain("einvoicing");
  });
});

describe("vendor_facts", () => {
  it("returns facts for a known vendor by id", () => {
    const result = vendorFacts(data, { vendor: "odoo" });
    expect("facts" in result).toBe(true);
    if ("facts" in result) {
      expect(result.vendor_id).toBe("odoo");
      expect(result.facts.length).toBeGreaterThan(0);
      expect(result.facts[0]).toHaveProperty("statement");
      expect(result.facts[0]).toHaveProperty("source_url");
      expect(result.facts[0]).toHaveProperty("certainty");
    }
  });

  it("resolves aliases case/accent-insensitively", () => {
    expect(vendorFacts(data, { vendor: "BC" })).toMatchObject({
      vendor_id: "business-central",
    });
    expect(vendorFacts(data, { vendor: "Business Central" })).toMatchObject({
      vendor_id: "business-central",
    });
    expect(vendorFacts(data, { vendor: "dynamics" })).toMatchObject({
      vendor_id: "business-central",
    });
    expect(vendorFacts(data, { vendor: "SAP B1" })).toMatchObject({
      vendor_id: "sap-business-one",
    });
    expect(vendorFacts(data, { vendor: "sap" })).toMatchObject({
      vendor_id: "sap-business-one",
    });
    expect(vendorFacts(data, { vendor: "Sage 100" })).toMatchObject({
      vendor_id: "sage",
    });
    expect(vendorFacts(data, { vendor: "Sage X3" })).toMatchObject({
      vendor_id: "sage",
    });
    expect(vendorFacts(data, { vendor: "Odoo" })).toMatchObject({
      vendor_id: "odoo",
    });
  });

  it("returns a soft message for unknown vendor with available ids", () => {
    const result = vendorFacts(data, { vendor: "acumatica" });
    expect(result).toMatchObject({
      message: expect.stringMatching(
        /no sourced facts for acumatica; verify on the vendor's official pages/,
      ),
      available_vendor_ids: expect.arrayContaining(["odoo", "sage"]),
    });
    expect(result).not.toHaveProperty("error");
  });

  it("filters by topic", () => {
    const result = vendorFacts(data, { vendor: "odoo", topic: "pricing" });
    if ("facts" in result) {
      expect(result.facts.length).toBeGreaterThan(0);
      expect(result.facts.every((f) => f.statement.length > 0)).toBe(true);
      const raw = data.vendors.find((v) => v.id === "odoo")!.facts.filter(
        (f) => f.topic === "pricing",
      );
      expect(result.facts.length).toBe(raw.length);
      expect(result.facts.some((f) => f.volatile === true && f.note === "re-check live")).toBe(
        true,
      );
    }
  });

  it("caps at 15 facts", () => {
    const oversized = withExtraVendor(oversizedVendor("huge", 40));
    const result = vendorFacts(oversized, { vendor: "huge" });
    if ("facts" in result) {
      expect(result.facts.length).toBe(MAX_FACTS);
    }
  });
});

describe("einvoicing_status", () => {
  it("returns einvoicing facts for all vendors plus france block", () => {
    const result = einvoicingStatus(data, {});
    expect("einvoicing_france" in result).toBe(true);
    if ("vendors" in result) {
      expect(result.vendors.length).toBe(data.vendors.length);
      expect(result.einvoicing_france.note).toBe("re-check live");
      expect(result.vendors.every((v) => v.facts.length >= 1)).toBe(true);
    }
  });

  it("filters to one vendor via alias", () => {
    const result = einvoicingStatus(data, { vendor: "bc" });
    if ("vendors" in result) {
      expect(result.vendors).toHaveLength(1);
      expect(result.vendors[0]?.id).toBe("business-central");
    }
  });

  it("returns soft message for unknown vendor", () => {
    const result = einvoicingStatus(data, { vendor: "netsuite" });
    expect(result).toMatchObject({
      message: expect.stringMatching(/no sourced facts for netsuite/),
      available_vendor_ids: expect.arrayContaining(["odoo"]),
    });
  });

  it("caps vendor facts at 15", () => {
    const many: Fact[] = Array.from({ length: 20 }, (_, i) => ({
      topic: "einvoicing",
      statement: `e-${i}`,
      source_url: `https://example.com/e/${i}`,
      certainty: "official",
    }));
    const oversized = withExtraVendor({
      id: "huge-e",
      name: "Huge E",
      facts: many,
    });
    const result = einvoicingStatus(oversized, { vendor: "huge-e" });
    if ("vendors" in result) {
      expect(result.vendors[0]?.facts.length).toBe(MAX_FACTS);
    }
  });
});

describe("support_deadlines", () => {
  it("returns support_deadlines facts across vendors", () => {
    const result = supportDeadlines(data, {});
    if ("vendors" in result) {
      expect(result.vendors.length).toBeGreaterThan(0);
      expect(
        result.vendors.every((v) => v.facts.every((f) => f.statement)),
      ).toBe(true);
    }
  });

  it("filters by vendor alias", () => {
    const result = supportDeadlines(data, { vendor: "sage x3" });
    if ("vendors" in result) {
      expect(result.vendors).toHaveLength(1);
      expect(result.vendors[0]?.id).toBe("sage");
    }
  });

  it("returns soft message for unknown vendor", () => {
    const result = supportDeadlines(data, { vendor: "oracle" });
    expect(result).toMatchObject({
      message: expect.stringMatching(/no sourced facts for oracle/),
    });
  });

  it("caps at 15 facts total", () => {
    const many: Fact[] = Array.from({ length: 20 }, (_, i) => ({
      topic: "support_deadlines",
      statement: `d-${i}`,
      source_url: `https://example.com/d/${i}`,
      certainty: "official",
    }));
    const oversized = withExtraVendor({
      id: "huge-d",
      name: "Huge D",
      facts: many,
    });
    const result = supportDeadlines(oversized, { vendor: "huge-d" });
    if ("vendors" in result) {
      const total = result.vendors.reduce((n, v) => n + v.facts.length, 0);
      expect(total).toBe(MAX_FACTS);
    }
  });
});

describe("odoo_20_changes", () => {
  it("returns all odoo 20 changes", () => {
    const result = odoo20Changes(data, {});
    expect(result.changes.length).toBe(data.odoo_20_changes.length);
    expect(result.changes[0]).toHaveProperty("area");
    expect(result.changes[0]).toHaveProperty("statement");
  });

  it("filters by area case-insensitively", () => {
    const result = odoo20Changes(data, { area: "ORM" });
    expect(result.changes.length).toBeGreaterThan(0);
    expect(result.changes.every((c) => c.area === "orm")).toBe(true);
  });

  it("caps at 15", () => {
    const many = Array.from({ length: 20 }, (_, i) => ({
      area: "orm",
      statement: `c-${i}`,
      source_url: `https://example.com/c/${i}`,
      certainty: "code" as const,
    }));
    const oversized: ErpFacts = { ...data, odoo_20_changes: many };
    const result = odoo20Changes(oversized, {});
    expect(result.changes.length).toBe(MAX_FACTS);
  });
});

describe("sources_and_method", () => {
  it("returns checked_on, certainty levels, rule, repo and site", () => {
    const result = sourcesAndMethod(data);
    expect(result.checked_on).toBe(data.checked_on);
    expect(result.certainty_levels).toEqual(data.certainty_levels);
    expect(result.rule).toBe(VOLATILE_RULE);
    expect(result.repository).toBe(GITHUB_REPO);
    expect(result.site).toBe(SITE_URL);
  });
});
