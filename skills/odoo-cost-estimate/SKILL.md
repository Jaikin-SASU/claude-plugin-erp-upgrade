---
name: odoo-cost-estimate
description: Estimate the total cost of an Odoo project or of running Odoo — licences (Standard, Custom, Light Users, first-year discount), hosting (Odoo Online, Odoo.sh, on-premise), implementation, migration and maintenance — over 5 years, with dated list prices and sourced market references. Use when the user asks "how much does Odoo cost?", "combien coûte Odoo pour 20 utilisateurs ?", "Odoo licence price", "budget for an Odoo implementation or migration", or compares Odoo with another ERP.
---

# Odoo total cost estimate

**Language:** answer in the user's language.

## Workflow
1. Collect: number of internal users (who creates or edits data), number of employees without user account (Light Users), apps needed, plan implied (see odoo-fit-gap `plan-constraints.md`: API, Studio or custom code → Custom), hosting, custom developments, data migration, integrations, current version if it is a migration.
2. **Licences**: check current prices on https://www.odoo.com/pricing if web access is available; otherwise use the dated values in `../odoo-fit-gap/references/plan-constraints.md` and say "as of 24 Sept 2026". Compute year 1 (with first-year discount, flagged as such) and years 2–5 at list price. Mention renewal indexation "up to 7 %/year" as a risk, not a forecast. Light Users: price via an Odoo advisor — show it as "to confirm" with the published "from" price.
3. **Hosting**: Online (included), Odoo.sh (priced separately — check the Odoo.sh pricing page), on-premise (servers, backups, operations: list items, never 0 €).
4. **Implementation or migration**: if the `prix-logiciel` MCP tools are available, call `price_statistics` and `private_market_prices` for `erp` and `search_public_contracts` with keywords "Odoo" to show comparable contracts; state the caveats (public amounts are often multi-year ceilings). Cross-check with an effort table (framing, configuration per app, Studio, custom modules S/M/L, data migration, integrations, training, acceptance, project management 15–20 %) × a market day rate from `daily_rates`.
5. **Maintenance**: optional support contract; upgrade porting of custom code at each major version (every DEV line costs again).
6. Output.

## Output format
```
## 5-year cost
| | Year 1 | Years 2–5 (per year) | 5-year total |
| Licences (users × price) | | | |
| Light Users | | | |
| Hosting | | | |
| Implementation / migration (one-off) | | | |
| Maintenance / upgrades | | | |
| Total | | | |

## Assumptions (dated prices, users, plan, hosting)
## Market references (sources, dates, caveats)
## What would change the cost most
```

## Principles
- Prices always with their check date; unknown items "to confirm", never 0 €.
- Never present the first-year discount as the recurring price.
- A discount belonging to Odoo (negotiated) is mentioned without a figure.
