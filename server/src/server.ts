import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import {
  GITHUB_REPO,
  READ_ONLY_ANNOTATIONS,
  SITE_URL,
  type ErpFacts,
} from "./lib/types.js";
import { sourceLine, urlsFromFacts } from "./lib/helpers.js";
import { listVendors } from "./tools/list-vendors.js";
import { vendorFacts } from "./tools/vendor-facts.js";
import { einvoicingStatus } from "./tools/einvoicing-status.js";
import { supportDeadlines } from "./tools/support-deadlines.js";
import { odoo20Changes } from "./tools/odoo-20-changes.js";
import { sourcesAndMethod } from "./tools/sources-and-method.js";

function textResult(payload: unknown, urls: string[], checkedOn: string) {
  return {
    content: [
      {
        type: "text" as const,
        text: `${JSON.stringify(payload)}\n${sourceLine(urls, checkedOn)}`,
      },
    ],
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function collectUrls(payload: unknown): string[] {
  if (!isRecord(payload)) return [GITHUB_REPO];

  if ("available_vendor_ids" in payload) {
    return [GITHUB_REPO];
  }

  if ("repository" in payload && "site" in payload) {
    return [GITHUB_REPO, SITE_URL];
  }

  if ("vendors" in payload && Array.isArray(payload.vendors)) {
    const urls: string[] = [];
    for (const row of payload.vendors) {
      if (!isRecord(row) || !Array.isArray(row.facts)) continue;
      urls.push(...urlsFromFacts(row.facts as { source_url: string }[]));
    }
    if (
      isRecord(payload.einvoicing_france) &&
      typeof payload.einvoicing_france.source_url === "string"
    ) {
      urls.push(payload.einvoicing_france.source_url);
    }
    if ("fact_count" in (payload.vendors[0] ?? {})) {
      return [GITHUB_REPO];
    }
    return urls.length > 0 ? urls : [GITHUB_REPO];
  }

  if ("facts" in payload && Array.isArray(payload.facts)) {
    return urlsFromFacts(payload.facts as { source_url: string }[]);
  }

  if ("changes" in payload && Array.isArray(payload.changes)) {
    return urlsFromFacts(payload.changes as { source_url: string }[]);
  }

  return [GITHUB_REPO];
}

export function buildServer(data: ErpFacts): McpServer {
  const server = new McpServer({
    name: "erp-facts",
    version: "0.2.0",
  });
  const checkedOn = data.checked_on;

  server.registerTool(
    "list_vendors",
    {
      title: "List vendors",
      description:
        "List ERP vendors with id, name, fact count and available topics.",
      inputSchema: {},
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async () => {
      const payload = listVendors(data);
      return textResult(payload, collectUrls(payload), checkedOn);
    },
  );

  server.registerTool(
    "vendor_facts",
    {
      title: "Vendor facts",
      description:
        "Return sourced facts for one ERP vendor (id or name; aliases: bc/business central/dynamics, sap b1/sap, sage 100/sage x3). Optional topic filter. Max 15 facts.",
      inputSchema: {
        vendor: z
          .string()
          .describe("Vendor id or name (case/accent-insensitive; aliases accepted)"),
        topic: z
          .string()
          .optional()
          .describe("Optional topic filter, e.g. pricing, einvoicing"),
      },
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async (args) => {
      const payload = vendorFacts(data, args);
      return textResult(payload, collectUrls(payload), checkedOn);
    },
  );

  server.registerTool(
    "einvoicing_status",
    {
      title: "E-invoicing status",
      description:
        "French e-invoicing (PA) status per vendor plus the national einvoicing_france block. Optional vendor filter.",
      inputSchema: {
        vendor: z
          .string()
          .optional()
          .describe("Optional vendor id or name"),
      },
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async (args) => {
      const payload = einvoicingStatus(data, args);
      return textResult(payload, collectUrls(payload), checkedOn);
    },
  );

  server.registerTool(
    "support_deadlines",
    {
      title: "Support deadlines",
      description:
        "Support / maintenance end dates per ERP vendor. Optional vendor filter. Max 15 facts.",
      inputSchema: {
        vendor: z
          .string()
          .optional()
          .describe("Optional vendor id or name"),
      },
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async (args) => {
      const payload = supportDeadlines(data, args);
      return textResult(payload, collectUrls(payload), checkedOn);
    },
  );

  server.registerTool(
    "odoo_20_changes",
    {
      title: "Odoo 20 changes",
      description:
        "Breaking and notable changes in Odoo 20. Optional area filter (requirements, security, frontend, orm, modules, api, functional, ecosystem). Max 15.",
      inputSchema: {
        area: z
          .string()
          .optional()
          .describe("Optional area filter"),
      },
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async (args) => {
      const payload = odoo20Changes(data, args);
      return textResult(payload, collectUrls(payload), checkedOn);
    },
  );

  server.registerTool(
    "sources_and_method",
    {
      title: "Sources and method",
      description:
        "Dataset checked_on date, certainty levels, volatility rule, GitHub repository and JAIKIN site.",
      inputSchema: {},
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async () => {
      const payload = sourcesAndMethod(data);
      return textResult(payload, collectUrls(payload), checkedOn);
    },
  );

  return server;
}
