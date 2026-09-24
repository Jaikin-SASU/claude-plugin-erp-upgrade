# Changelog

## 0.3.0 — 2026-09-24 : read-only MCP server `erp-facts` (https://erp-mcp.jaikin.eu/mcp, registry name eu.jaikin/erp-facts) serving the sourced vendor facts; skills call it first when available; further-reading links.

## 0.2.0 — 2026-09-24 : multi-ERP (choose-erp, fit-gap, erp-migration, erp-cost, review-erp-quote) with sourced vendor references (Business Central, Sage, SAP Business One, Divalto, Cegid, Sylob, EBP, e-invoicing PA list); Odoo skill renamed odoo-20-upgrade with ${CLAUDE_PLUGIN_ROOT} script paths; legacy commands/ removed; displayName.

## 0.1.0 — 2026-09-24

First published version, on the day of the Odoo 20 release:

- 4 skills: `odoo-20-migration-readiness`, `odoo-fit-gap`, `odoo-cost-estimate`, `review-odoo-integrator-quote`
- 4 slash commands: `/odoo-migration-check`, `/odoo-fit-gap`, `/odoo-cost`, `/review-odoo-quote`
- Read-only stdlib scripts: `scan_addons.py`, `inventory_instance.py`
- Sourced and dated Odoo 20 facts
