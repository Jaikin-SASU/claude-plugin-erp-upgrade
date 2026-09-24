---
name: review-odoo-integrator-quote
description: Review a quote or proposal from an Odoo integrator (implementation or migration to Odoo 19/20) from the buyer's side — Odoo-specific traps (licences and user counting, first-year discount, plan vs custom modules, upgrade service vs custom code porting, OCA dependencies, deprecated API integrations, Studio) on top of general contract checks. Use when the user shares an Odoo integrator's quote ("devis intégrateur Odoo", "proposition migration Odoo 20") or asks whether an Odoo quote is complete or fair.
---

# Review an Odoo integrator's quote

**Language:** answer in the user's language. Quote the document in its original language.

## Workflow
1. Read the whole document (extract text from PDF/DOCX). Identify: scope (apps, processes), version targeted, edition, hosting, licences, pricing model, schedule, acceptance, warranty, ownership, exit.
2. Walk the **Odoo-specific checklist** below, then the general contract points (price cap, ownership in the client's name, acceptance by written report, warranty, reversibility, exit cost). If the `software-buyer-france` plugin is installed, its `review-quote-contract` skill covers the general points in depth.
3. If the `prix-logiciel` MCP tools are available, position the amount with `position_quote` (project type `erp`) and cite sources.
4. Output: verdict, red flags by severity (blocking / major / minor) with the quote and section, missing items, questions for the integrator (see `../odoo-20-migration-readiness/references/integrator-questions.md` for migrations).

## Odoo-specific checklist
- **Licences**: users counted from real data; Light Users (employees without user account) counted; plan consistent with the scope (API, Studio or custom code → Custom); prices at dated list price; **first-year discount not presented as the recurring price**; licences shown separately from the integrator's fees (licences are paid to Odoo).
- **Hosting vs method**: "Standard" is both a plan name and a way of working ("standard Odoo, no custom module") — the quote must say which it means. Custom modules require Odoo.sh or on-premise, or covered modules on Online.
- **Migration quotes**: Odoo's upgrade service upgrades the database of standard modules (and Studio while subscribed); it does **not** port custom or uncovered partner modules. The quote must price the custom-code port per module, including the ir.access security rewrite and OWL 3 for Odoo 20.
- **OCA / third-party modules**: listed, with their availability for the target version; fallback if not ported.
- **Integrations**: listed; any XML-RPC/JSON-RPC integration planned to move to JSON-2 (deprecated APIs; `db` service removed in 20).
- **Studio**: what is done in Studio vs in code, and how it is maintained across upgrades.
- **Test cycles**: number of test databases, test scripts per process, business testers, rehearsal, rollback.
- **Data migration**: scope of history, cleaning responsibility, dry runs.
- **Training and change**: processes that change with the version (see odoo-20-facts §5).
- **Partner claims**: a partner grade or certification claimed in the quote should be verifiable on Odoo's public partner directory (https://www.odoo.com/partners); do not assume it.
- **Code ownership**: custom modules in the client's repository, licence compatible with the client's use (LGPL/OPL implications explained).

## Principles
- Every Odoo fact cited must come from `../odoo-20-migration-readiness/references/odoo-20-facts.md` or a live check with URL and date.
- Unknown third-party costs are "to be confirmed", never 0 €.
- Not legal advice; recommend legal review for large contracts.
