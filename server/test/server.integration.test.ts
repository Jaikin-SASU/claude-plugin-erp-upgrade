import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { describe, expect, it } from "vitest";
import factsJson from "../src/data/erp-facts.json";
import type { ErpFacts } from "../src/lib/types.js";
import { buildServer } from "../src/server.js";

const data = factsJson as ErpFacts;

const TOOL_NAMES = [
  "list_vendors",
  "vendor_facts",
  "einvoicing_status",
  "support_deadlines",
  "odoo_20_changes",
  "sources_and_method",
] as const;

describe("buildServer integration", () => {
  it("lists 6 tools with title and readOnlyHint, each callable", async () => {
    const server = buildServer(data);
    const client = new Client({ name: "test", version: "1.0.0" });
    const [clientTransport, serverTransport] =
      InMemoryTransport.createLinkedPair();
    await Promise.all([
      server.connect(serverTransport),
      client.connect(clientTransport),
    ]);

    const listed = await client.listTools();
    expect(listed.tools).toHaveLength(6);
    const names = listed.tools.map((t) => t.name).sort();
    expect(names).toEqual([...TOOL_NAMES].sort());
    for (const tool of listed.tools) {
      expect(tool.title).toBeTruthy();
      expect(tool.annotations?.readOnlyHint).toBe(true);
    }

    const argsByName: Record<(typeof TOOL_NAMES)[number], Record<string, unknown>> = {
      list_vendors: {},
      vendor_facts: { vendor: "odoo", topic: "pricing" },
      einvoicing_status: { vendor: "sage" },
      support_deadlines: { vendor: "bc" },
      odoo_20_changes: { area: "api" },
      sources_and_method: {},
    };

    for (const name of TOOL_NAMES) {
      const res = await client.callTool({
        name,
        arguments: argsByName[name],
      });
      const text = (res.content as { type: string; text: string }[])
        .filter((c) => c.type === "text")
        .map((c) => c.text)
        .join("\n");
      expect(text.length).toBeGreaterThan(20);
      expect(text).toMatch(
        new RegExp(`source: .+ · checked ${data.checked_on}`),
      );
    }

    await client.close();
    await server.close();
  });
});
