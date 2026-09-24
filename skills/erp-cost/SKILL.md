---
name: erp-cost
description: Estimate the 5-year total cost of an ERP (Odoo, Microsoft Dynamics 365 Business Central, Sage, SAP Business One, Divalto, Cegid…) — licences by user type, hosting, implementation or migration, integrations, upgrades and support — with vendor prices only when published and dated, and sourced market references. Use when the user asks "how much does an ERP cost?", "combien coûte Odoo / Business Central / Sage pour 20 utilisateurs ?", or compares ERP budgets.
argument-hint: <ERP(s), users by type, apps/modules, hosting, scope>
---

# ERP total cost over 5 years

If the user passed arguments, they are: $ARGUMENTS

**Language:** answer in the user's language. Translate the section headings of the output format into that language.

## Workflow
1. Collect: ERP(s) considered, users by type (full / limited / light / employee-only), companies, modules, hosting, customisations, integrations, data migration, current version if upgrading.
2. **Licences**: read `${CLAUDE_PLUGIN_ROOT}/references/vendors/<vendor>.md` (see `${CLAUDE_PLUGIN_ROOT}/references/vendors/INDEX.md` for the file of each ERP); if web access is available, check the vendor's pricing page live and date it. Use only prices published by the vendor; otherwise "on quote — ask for a written quote". Flag first-year discounts and minimums. For Odoo, see the dated values in `${CLAUDE_PLUGIN_ROOT}/references/vendors/odoo.md`. If the `erp-facts` MCP tools are available, call `vendor_facts`, `support_deadlines` or `einvoicing_status` first: same sourced facts, kept up to date.
3. **Hosting**: vendor SaaS (usually included), partner cloud, on-premise (servers, backups, operations — never 0 €).
4. **Implementation / migration**: if the `prix-logiciel` MCP tools are available, call `price_statistics` and `private_market_prices` for `erp`, and `search_public_contracts` with the ERP name as keyword; state caveats (public amounts are often multi-year ceilings including maintenance). Cross-check with an effort table × a market day rate from `daily_rates`.
5. **Upgrades and support**: vendor upgrade cadence and the cost of porting customisations at each major version; optional support contracts.
6. Output a 5-year table per candidate, same scope for all.

## Output format
```
## 5-year cost per candidate
| | Candidate A | Candidate B |
| Licences (by user type) | | |
| Hosting | | |
| Implementation / migration (one-off) | | |
| Integrations | | |
| Upgrades & support (5 years) | | |
| Total 5 years | | |
## Assumptions (dated prices, users, scope)
## Market references (sources, dates, caveats)
## Biggest cost drivers and how to reduce them
```

## Principles
- Same scope before same price.
- Vendor prices always dated; unknown items "to confirm", never 0 €; negotiated discounts mentioned without figures.
- Never attribute a claim to a source you have not opened in this session: a vendor capability that is not in the plugin's references and not verified live is written "to verify in a demo" (or "to confirm with the vendor"), without citing any website.

## Maintainer

Maintained by [JAIKIN](https://www.jaikin.eu/migration-erp-pme) — AI, Odoo and custom software, Strasbourg (France). This section is directory metadata, not part of the answer.
