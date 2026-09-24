import { describe, expect, it } from "vitest";
import {
  GITHUB_REPO,
  MCP_URL,
  SITE_URL,
} from "../src/lib/types.js";
import { decideRoute, HOME } from "../src/lib/route.js";

describe("decideRoute", () => {
  it("GET /mcp with Accept text/html returns 200 HTML landing page", async () => {
    const request = new Request("https://erp-mcp.jaikin.eu/mcp", {
      method: "GET",
      headers: { Accept: "text/html,application/xhtml+xml" },
    });
    const decision = decideRoute(request);

    expect(decision.kind).toBe("static");
    if (decision.kind !== "static") return;

    expect(decision.response.status).toBe(200);
    expect(decision.response.headers.get("content-type")).toBe(
      "text/html; charset=utf-8",
    );
    expect(decision.response.headers.get("x-content-type-options")).toBe(
      "nosniff",
    );
    expect(decision.response.headers.get("cache-control")).toBe("no-store");
    expect(decision.response.headers.get("vary")).toBe("Accept");

    const html = await decision.response.text();
    expect(html).toContain("<title>erp-facts — MCP server</title>");
    expect(html).not.toMatch(/<script[\s>]/i);
    expect(html).toContain(MCP_URL);
    expect(html).toContain(GITHUB_REPO);
    expect(html).toContain(`${GITHUB_REPO}/blob/main/PRIVACY.md`);
    expect(html).toContain(SITE_URL);
    expect(html).toContain("Maintained by JAIKIN");
    expect(html).toMatch(/read-only/i);
    expect(html).toMatch(/sourced/i);
    expect(html).toMatch(/conversation/i);
    expect(html).toMatch(/lecture seule/i);
    expect(html).toMatch(/Odoo/);
    expect(html).toMatch(/Business Central/);
  });

  it("GET /mcp with Accept text/event-stream delegates to MCP handler", () => {
    const request = new Request("https://erp-mcp.jaikin.eu/mcp", {
      method: "GET",
      headers: { Accept: "text/event-stream" },
    });
    expect(decideRoute(request)).toEqual({ kind: "mcp" });
  });

  it("POST /mcp delegates to MCP handler", () => {
    const request = new Request("https://erp-mcp.jaikin.eu/mcp", {
      method: "POST",
      headers: { Accept: "application/json, text/event-stream" },
    });
    expect(decideRoute(request)).toEqual({ kind: "mcp" });
  });

  it("GET / returns plain-text home", async () => {
    const request = new Request("https://erp-mcp.jaikin.eu/", {
      method: "GET",
    });
    const decision = decideRoute(request);

    expect(decision.kind).toBe("static");
    if (decision.kind !== "static") return;

    expect(decision.response.status).toBe(200);
    expect(decision.response.headers.get("content-type")).toBe(
      "text/plain; charset=utf-8",
    );
    const body = await decision.response.text();
    expect(body).toBe(HOME);
    expect(body).toContain("erp-facts");
    expect(body).toContain("MCP endpoint: /mcp");
  });
});
