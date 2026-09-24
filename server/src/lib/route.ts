import {
  GITHUB_REPO,
  MCP_URL,
  SITE_URL,
} from "./types.js";

export const HOME = `erp-facts — read-only sourced ERP facts MCP
Repo: ${GITHUB_REPO}
Privacy: ${GITHUB_REPO}/blob/main/PRIVACY.md
Site: ${SITE_URL}
MCP endpoint: /mcp
`;

const PRIVACY_URL = `${GITHUB_REPO}/blob/main/PRIVACY.md`;

const LANDING_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>erp-facts — MCP server</title>
</head>
<body>
<main>
<h1>erp-facts — MCP server</h1>
<section lang="en">
<p>This is a read-only MCP server of sourced, dated ERP facts (Odoo, Business Central, Sage, SAP Business One, Divalto, Cegid, Sylob, EBP).</p>
<p>Configure the MCP address as <code>${MCP_URL}</code>.</p>
<p>It stores no conversation data.</p>
</section>
<section lang="fr">
<p>Ceci est un serveur MCP en lecture seule de faits ERP sourcés et datés (Odoo, Business Central, Sage, SAP Business One, Divalto, Cegid, Sylob, EBP).</p>
<p>L'adresse à configurer est <code>${MCP_URL}</code>.</p>
<p>Il ne stocke aucune donnée de conversation.</p>
</section>
<p><a href="${GITHUB_REPO}">GitHub repository</a> · <a href="${PRIVACY_URL}">PRIVACY.md</a> · <a href="${SITE_URL}">Maintained by JAIKIN</a></p>
</main>
</body>
</html>
`;

export type RouteDecision =
  | { kind: "static"; response: Response }
  | { kind: "mcp" };

function acceptsEventStream(accept: string | null): boolean {
  return (accept ?? "").toLowerCase().includes("text/event-stream");
}

function landingResponse(): Response {
  return new Response(LANDING_HTML, {
    status: 200,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "x-content-type-options": "nosniff",
      "cache-control": "no-store",
      vary: "Accept",
    },
  });
}

function homeResponse(): Response {
  return new Response(HOME, {
    status: 200,
    headers: { "content-type": "text/plain; charset=utf-8" },
  });
}

/**
 * Decide whether to serve a static response or delegate to the MCP handler.
 * Browser GET /mcp (Accept without text/event-stream) gets an HTML landing page.
 */
export function decideRoute(request: Request): RouteDecision {
  const url = new URL(request.url);

  if (request.method === "GET" && url.pathname === "/") {
    return { kind: "static", response: homeResponse() };
  }

  if (
    request.method === "GET" &&
    url.pathname === "/mcp" &&
    !acceptsEventStream(request.headers.get("accept"))
  ) {
    return { kind: "static", response: landingResponse() };
  }

  return { kind: "mcp" };
}
