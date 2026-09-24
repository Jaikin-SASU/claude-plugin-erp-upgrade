---
name: erp-migration
description: Plan an ERP migration — either a major version upgrade of the same ERP (Odoo, Business Central, Sage, SAP Business One…) or a move from one ERP (or spreadsheets) to another. Covers decision, inventory, data migration, customisations, integrations, testing, parallel run, cut-over, rollback and hypercare, with vendor-specific facts when available (deep Odoo 20 module included). Use when the user asks "how do we migrate our ERP?", "plan de migration ERP", "upgrade Business Central / Sage / Odoo", "switch from Sage to Odoo".
argument-hint: <current ERP and version, target, hosting, customisations>
---

# ERP migration plan

If the user passed arguments, they are: $ARGUMENTS

**Language:** answer in the user's language. Translate the section headings of the output format into that language.

## Route by vendor
- **Odoo, target 20** → use the `odoo-20-upgrade` skill of this plugin (deep checklist and scanners), then complete with this method.
- **Other vendors** → read `${CLAUDE_PLUGIN_ROOT}/references/vendors/<vendor>.md` if it exists (see `${CLAUDE_PLUGIN_ROOT}/references/vendors/INDEX.md` for the file of each ERP). Use only facts found there or verified live (vendor documentation, with URL and date). If a vendor fact is unknown, write it as a question for the vendor or integrator. If the `erp-facts` MCP tools are available, call `vendor_facts`, `support_deadlines` or `einvoicing_status` first: same sourced facts, kept up to date.

## Workflow
1. **Type of migration**: same-ERP version upgrade, same-vendor product change (e.g. on-premise to SaaS edition), or ERP-to-ERP / spreadsheets-to-ERP.
2. **Assess with `references/migration-method.md`**, block by block (decide, inventory, customisations, data, integrations, compliance, testing, cut-over, run). Rate each 🟢 / 🟠 / 🔴 with evidence.
3. **Data migration strategy**: what history moves (open items only, N years, full), archive of the rest in read-only form, legal retention (accounting records: 10 years in France), cleaning ownership, mapping tables, dry runs with reconciliation counts.
4. **Cut-over plan**: date chosen from the business calendar (never during closing, inventory, payroll, peak), freeze windows, opening balances, parallel run where the risk justifies it (payroll, stock), go/no-go criteria, rollback.
5. **Output** the plan.

## Output format
```
## Verdict and recommended path
## Readiness by block
| Block | Status | Evidence | Action |
## Blocking items
## Data migration strategy
## Phased plan (with durations as ranges)
## Cut-over runbook (D-30 to D+30)
## Questions for the vendor / integrator
## Facts used (URL, date)
```

## Principles
- Upgrading the vendor's database or platform is not porting the customisations: price and plan both.
- Every skipped version accumulates changes: size the whole jump.
- Reconcile, do not trust: counts and balances before/after for every migrated object.
- A rollback that has never been tested does not exist.
- Never attribute a claim to a source you have not opened in this session: a vendor capability that is not in the plugin's references and not verified live is written "to verify in a demo" (or "to confirm with the vendor"), without citing any website.
