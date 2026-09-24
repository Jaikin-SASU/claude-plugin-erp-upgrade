import { createMcpHandler } from "agents/mcp";
import factsJson from "./data/erp-facts.json";
import type { ErpFacts } from "./lib/types.js";
import { decideRoute } from "./lib/route.js";
import { buildServer } from "./server.js";

const data = factsJson as ErpFacts;

export default {
  async fetch(request: Request, env: unknown, ctx: ExecutionContext): Promise<Response> {
    const decision = decideRoute(request);
    if (decision.kind === "static") {
      return decision.response;
    }

    // Fresh server per request (stateless). createMcpHandler exists on agents/mcp
    // and routes SDK v1 servers through the WorkerTransport lane.
    return createMcpHandler(buildServer(data), { route: "/mcp" })(
      request,
      env,
      ctx,
    );
  },
} satisfies ExportedHandler;
