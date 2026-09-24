export interface Fact {
  topic: string;
  statement: string;
  source_url: string;
  certainty: string;
  volatile?: boolean;
}

export interface Vendor {
  id: string;
  name: string;
  facts: Fact[];
}

export interface EinvoicingFrance {
  statement: string;
  source_url: string;
  certainty: string;
  volatile?: boolean;
}

export interface Odoo20Change {
  area: string;
  statement: string;
  source_url: string;
  certainty: string;
  volatile?: boolean;
}

export interface ErpFacts {
  checked_on: string;
  certainty_levels: Record<string, string>;
  vendors: Vendor[];
  einvoicing_france: EinvoicingFrance;
  odoo_20_changes: Odoo20Change[];
}

export interface FormattedFact {
  statement: string;
  source_url: string;
  certainty: string;
  volatile?: boolean;
  note?: string;
}

export interface UnknownVendor {
  message: string;
  available_vendor_ids: string[];
}

export const MAX_FACTS = 15;

export const GITHUB_REPO =
  "https://github.com/Jaikin-SASU/claude-plugin-erp-upgrade";

export const SITE_URL = "https://www.jaikin.eu/";

export const MCP_URL = "https://erp-mcp.jaikin.eu/mcp";

export const VOLATILE_RULE =
  "facts are dated; volatile items must be re-checked live";

export const READ_ONLY_ANNOTATIONS = {
  readOnlyHint: true,
  destructiveHint: false,
  idempotentHint: true,
  openWorldHint: false,
} as const;
