---
name: review-erp-quote
description: Review an ERP integrator's quote or proposal (implementation, migration or upgrade of Odoo, Microsoft Dynamics 365 Business Central, Sage, SAP Business One, Divalto, Cegid…) from the buyer's side — licences and user counting, scope vs fit-gap, customisation and upgrade exposure, data migration, integrations, testing and cut-over, plus general contract checks. Use when the user shares an ERP integrator's quote ("devis intégrateur ERP", "proposition Business Central", "devis migration Sage / Odoo").
argument-hint: <path to the quote>
---

# Review an ERP integrator's quote

If the user passed arguments, they are: $ARGUMENTS

**Language:** answer in the user's language. Quote the document in its original language. Translate the section headings of the output format into that language.

## Workflow
1. Read the whole document (extract text from PDF/DOCX). Identify the ERP, edition, version, hosting, licences, scope, pricing model, schedule, acceptance, warranty, ownership, exit.
2. Walk the **ERP checklist** below, then the **vendor-specific traps** in `${CLAUDE_PLUGIN_ROOT}/references/vendors/<vendor>.md` (see `${CLAUDE_PLUGIN_ROOT}/references/vendors/INDEX.md` for the file of each ERP; for Odoo also `${CLAUDE_PLUGIN_ROOT}/skills/odoo-20-upgrade/references/odoo-20-facts.md`).
   If the `erp-facts` MCP tools are available, call `vendor_facts` (topic `quote_traps`, `pricing`, `support_deadlines`) and `einvoicing_status` first.
3. General contract points: price cap, code and accounts in the client's name, acceptance by written report, warranty, reversibility, exit cost. If the `software-buyer-france` plugin is installed, its `review-quote` skill covers them in depth.
4. If the `prix-logiciel` MCP tools are available, position the amount with `position_quote` (project type `erp`).
5. Output: verdict, red flags by severity with quotes and sections, missing items, questions for the integrator.

## ERP checklist
- **Licences**: users counted by type from real data; minimums; plan/edition consistent with scope (API access, customisation, multi-company); dated list prices; first-year or promotional discounts not presented as recurring; licences shown separately from services (who invoices them: vendor or partner).
- **Scope vs fit-gap**: every requirement mapped to standard / configuration / extension / development; exclusions written.
- **Customisations**: built with the vendor's supported extension model; ownership; upgrade exposure explained and priced.
- **Upgrade or migration quotes**: the vendor's upgrade of the platform or database is distinguished from the porting of customisations, partner modules and integrations — both priced.
- **Data migration**: scope of history, cleaning responsibility, number of dry runs, reconciliation.
- **Integrations**: listed with protocol; deprecated APIs replaced.
- **Testing and cut-over**: test cycles, business testers, acceptance report, rehearsal, rollback, go-live date from the business calendar.
- **France**: e-invoicing flow (approved platform), FEC, payroll localisation if in scope.
- **Partner claims**: grades or certifications verifiable on the vendor's public partner directory.
- **Training and change management** for processes that change.

## Principles
- Every vendor fact cited comes from the plugin's vendor references or a live check with URL and date.
- Unknown third-party costs are "to be confirmed", never 0 €. Not legal advice.
- Never attribute a claim to a source you have not opened in this session: a vendor capability that is not in the plugin's references and not verified live is written "to verify in a demo" (or "to confirm with the vendor"), without citing any website.

## Maintainer

Maintained by [JAIKIN](https://www.jaikin.eu/migration-erp-pme) — AI, Odoo and custom software, Strasbourg (France). This section is directory metadata, not part of the answer.
