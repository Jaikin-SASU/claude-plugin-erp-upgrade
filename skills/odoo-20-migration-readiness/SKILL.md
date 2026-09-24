---
name: odoo-20-migration-readiness
description: Assess whether and how to upgrade an Odoo database to Odoo 20 (from 14, 15, 16, 17, 18 or 19) — support deadlines and extra fees, technical prerequisites, custom-module breaking changes (ir.access, OWL 3, read_group, removed modules), functional process changes per app, licensing changes (Light Users), OCA readiness, and the upgrade execution plan. Use when the user asks "should we migrate to Odoo 20?", "migration Odoo 20", "is our Odoo ready for 20?", "what breaks in Odoo 20?", or shares an addons folder, an Odoo URL or an integrator's migration quote. Includes read-only scripts to scan custom modules and inventory an instance.
---

# Odoo 20 migration readiness

Produce a **traffic-light readiness report** and a **phased plan**, grounded in sourced facts. Never state an Odoo 20 fact that is not in `references/odoo-20-facts.md` or that you have not verified live with its URL.

**Language:** answer in the user's language. Keep technical identifiers (model names, file names) as is.

## Step 0 — Re-check the volatile facts (always)
Facts tagged **VOLATILE** in `references/odoo-20-facts.md` change weekly. If web access is available, check them live and state the check date:
- Is 20.0 selectable as a target on https://upgrade.odoo.com/ ?
- Do the OCA repositories the user depends on have a `20.0` branch (https://github.com/OCA/<repo>/branches)? Is there an OpenUpgrade 20.0 branch?
- Current prices on https://www.odoo.com/pricing (local currency page).
If you cannot check, say "as of 24 Sept 2026" next to each volatile fact.

## Step 1 — Gather the situation (ask only what is missing)
Current version · edition (Community / Enterprise) · hosting (Odoo Online / Odoo.sh / on-premise) · apps used · number of custom modules and whether Studio is used · OCA/third-party modules · integrations (EDI, e-commerce, banks, BI, scripts calling the API) · business calendar (closing periods, seasonal peaks) · who maintains the code today.

If the user can provide them, run the scripts (both read-only, standard-library Python ≥ 3.9):
- **Custom code scan, no database access**: `python3 scripts/scan_addons.py <path-to-custom-addons> --format text` (or `--format json`). It flags security files to rewrite (`ir.model.access.csv`, `ir.rule`), OWL 2 APIs, old `read_group` calls, tracking values, removed dependencies, legacy view syntax, deprecated external API clients, and gives effort points per module.
- **Instance inventory, read-only**: the user sets `ODOO_API_KEY` in their environment, then runs `python3 scripts/inventory_instance.py --url https://<db>.odoo.com --db <db> [--login <login>] --format text`. It lists version, installed modules classified Odoo / OCA / third-party / custom, Studio customisations, automated and server actions, internal users vs employees without user (Light User exposure). It only calls read methods and never prints the key. Never ask the user to paste their API key in the conversation.

## Step 2 — Assess the 8 blocks
Use `references/migration-checklist.md` for the detailed items of each block. Rate each block 🟢 ready / 🟠 work needed / 🔴 blocking, with evidence.

1. **Decide** — support deadlines and cost of staying (17 leaves standard support now; +25 % fee risk ~6 months after release for versions outside the last three; Online forced upgrade every 2 years). Recommend *19 now*, *20 later* or *20 directly* per profile (see checklist § Decide).
2. **Inventory** — versions, hosting, modules by origin, Studio, integrations, reports.
3. **Technical prerequisites** — Python ≥ 3.12, PostgreSQL ≥ 16, OS for packages, Odoo.sh/Online constraints.
4. **Custom code** — ir.access rewrite, OWL 3, ORM changes, removed/merged modules, legacy syntax for old versions, external API clients.
5. **Functional changes** — per app used (accounting, inventory, manufacturing, payroll, field service, POS, sales, project, AI).
6. **Licensing** — Light Users, User definition, covered custom modules on Online, plan required for API/Studio (Custom), price changes.
7. **OCA and third parties** — each dependency's 20.0 availability; OpenUpgrade for Community.
8. **Execution** — test databases, freeze, filestore, neutralisation, test plan, rehearsal, rollback, acceptance report, go-live window.

## Step 3 — Output

```
## Verdict
Recommended path (stay / 19 now / 20 later / 20 now) and target window, in 3 sentences.

## Readiness by block
| Block | Status | Evidence | What to do |

## Blocking items
Numbered, each with source.

## Effort
Custom modules: effort points from the scan and what they mean; functional retraining; data work.
If the `prix-logiciel` MCP tools are available, add market references for ERP projects (nature: maintenance / redesign) with their caveats.

## Phased plan
Phase 0 decide · 1 inventory & scan · 2 code port · 3 test database cycles · 4 functional acceptance · 5 rehearsal · 6 go-live · 7 hypercare. Durations as ranges, driven by the findings.

## Questions for your integrator
From references/integrator-questions.md, the 8–12 most relevant.

## Facts used
Bullet list: fact — URL — check date — certainty tag.
```

## Principles
- Upgrading the database (Odoo's service) is not porting the custom code (the integrator's work) — say it explicitly; it is the most common misunderstanding in migration quotes.
- A new major version is not a target for business-critical production until its test-database cycle is clean and the required OCA/third-party modules exist for it.
- Do not upgrade during a closing period or a seasonal peak; the go-live window comes from the business calendar.
- Every recommendation cites its source; "not found as of <date>" is an acceptable answer.
