---
name: odoo-fit-gap
description: Build a requirement-by-requirement fit-gap analysis for an Odoo project — which needs are covered by standard apps, by configuration, by Studio, by an OCA module, or require custom development — and the pricing-plan and hosting consequences of each choice. Use when the user shares requirements or a specification and asks "can Odoo do this?", "standard or custom?", "fit-gap Odoo", "which Odoo apps do we need?", or before asking integrators for quotes.
---

# Odoo fit-gap analysis

**Language:** answer in the user's language.

## Workflow
1. Read the requirements (extract text from PDF/DOCX). Number them if they are not.
2. For each requirement, classify the coverage level:
   - **S — Standard**: an Odoo app covers it out of the box. Name the app and the feature.
   - **C — Configuration**: standard, but needs settings, data or rules (routes, approval rules, fiscal positions, reporting views).
   - **ST — Studio**: needs Studio fields, views, automations or reports.
   - **OCA** — covered by a community module; name the repository and check whether it exists for the target version (branch `<version>` on github.com/OCA/<repo>).
   - **DEV — Development**: custom module needed; describe it in one sentence and give a size (S/M/L).
   - **OUT** — should stay outside Odoo (specialised tool + integration), with the reason.
   Mark your confidence (high / to verify). Never claim a feature exists without naming where it is; if unsure, mark "to verify in a demo database".
3. Derive the **plan and hosting consequences** (see `references/plan-constraints.md`): any ST, DEV or external API integration → Custom plan; custom modules → Odoo.sh or on-premise (or covered modules on Online); Community edition → no Enterprise apps, no official upgrade service.
4. Derive the **upgrade exposure**: every DEV and OCA line is code to port at each major version (see odoo-20-migration-readiness).
5. Output the matrix and the synthesis.

## Output format
```
## Synthesis
% of requirements by level (S, C, ST, OCA, DEV, OUT) · apps needed · plan required · hosting implied.

## Fit-gap matrix
| # | Requirement | Level | How (app / setting / module / dev) | Confidence | Notes |

## Custom developments to price
| Dev | Purpose | Size | Upgrade exposure |

## Decisions before quotes
Hosting, plan, master data ownership, integrations to verify (API/import availability).

## To verify in a demo database
Numbered.
```

## Principles
- Prefer standard processes over reproducing current habits: flag requirements that describe a habit rather than a need, and propose the standard alternative.
- One master system per data (customers, products, stock, prices) — flag double-master situations.
- Studio is fast but is still customisation: it ties you to the Custom plan and must be tested at each upgrade.
- An OCA module is free but not maintained on your schedule: check its 20.0 status before relying on it.
