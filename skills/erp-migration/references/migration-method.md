# ERP migration method (any vendor)

## 1. Decide
- [ ] Why migrate now: end of support, compliance (e.g. French e-invoicing), features, cost, vendor change.
- [ ] Cost of staying: extended support fees, security exposure, compliance gaps.
- [ ] Target and path: direct jump vs intermediate versions; vendor's supported upgrade paths.
- [ ] Business window from the calendar.

## 2. Inventory
- [ ] Modules/apps in use and by whom; users by type.
- [ ] Customisations: code, extensions, scripts, reports, workflows, low-code/studio changes — with owner and documentation.
- [ ] Integrations: every system in and out, protocol, frequency, owner.
- [ ] Data volumes and quality; history depth.

## 3. Customisations
- [ ] For each: keep, replace by standard, rebuild, or drop — decided with the business owner.
- [ ] Vendor's customisation model on the target (e.g. extensions only, no base-code change) and its upgrade impact.
- [ ] Port effort estimated per item, capped price.

## 4. Data
- [ ] Scope of history; archive strategy; legal retention.
- [ ] Mapping and transformation rules documented; master data cleaned before migration.
- [ ] Dry runs (≥ 2) with reconciliation: record counts, totals (receivables, payables, stock value, GL balances).

## 5. Integrations
- [ ] Each integration re-tested on the target; deprecated APIs replaced; credentials rotated.

## 6. Compliance (France)
- [ ] E-invoicing: reception obligation since Sept 2026, issuance for SMEs Sept 2027 — invoicing flow tested end to end with the approved platform (PA).
- [ ] FEC export, VAT, payroll (if in scope) validated with the accountant.

## 7. Testing
- [ ] Unit/automated tests of customisations; functional test scripts per process written by process owners; user acceptance with a written report (PV); performance test on production-size data.

## 8. Cut-over
- [ ] Runbook with timings, owners, go/no-go criteria; rehearsal; opening balances; rollback tested; communication plan.

## 9. Run
- [ ] Hypercare 2–4 weeks with daily triage; first month-end closing assisted; post-migration review.
