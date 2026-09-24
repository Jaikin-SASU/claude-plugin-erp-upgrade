# Privacy policy — ERP Upgrade & Fit-Gap Advisor plugin

Last updated: 24 September 2026. Controller: JAIKIN SASU, 24 rue de l'Industrie, 67640 Fegersheim, France — contact: victor@jaikin.eu.

## Skills and documents
Skills run inside your Claude client. Requirements, quotes and other documents you ask Claude to review are not collected by JAIKIN.

## Local scripts
- `scan_addons.py` reads files on your machine only; it makes no network request.
- `inventory_instance.py` connects only to the Odoo instance URL you provide, with the API key read from the `ODOO_API_KEY` environment variable. It calls read-only methods, never prints or stores the key, and sends nothing to JAIKIN or any third party.

## MCP server `prix-logiciel`
The plugin declares the read-only `prix-logiciel` MCP server (https://mcp.jaikin.eu/mcp). It receives only tool arguments (project type, keywords, amounts to position), stores and logs nothing at application level; the hosting provider (Cloudflare) processes technical request metadata for security. Full policy: https://github.com/Jaikin-SASU/claude-plugin-software-buyer/blob/main/PRIVACY.md

## Third-party sharing and retention
None; no application-level retention.

## Your rights
For any question or GDPR request: victor@jaikin.eu.
