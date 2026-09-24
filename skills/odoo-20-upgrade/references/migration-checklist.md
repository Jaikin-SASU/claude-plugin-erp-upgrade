# Odoo 20 migration checklist (detailed)

Each item: what to check → why (fact in odoo-20-facts.md §) → what to do. Tick 🟢 / 🟠 / 🔴.

## 1. Decide
- [ ] Current version and its support status (§1). 17 → leaves standard support in Sept 2026; 16 and older → already outside standard support; upgrade targets are limited to supported versions (plus the last unsupported one for 6 months).
- [ ] Cost of staying (§1): +25 % of the annualised subscription possible for databases outside the 3 latest versions, not earlier than 6 months after a release; extended support fees on Odoo.sh / on-premise; Online forces an upgrade every 2 years.
- [ ] Choose the path:
  - **On 17 or older, business-critical, many OCA modules** → upgrade to **19 now** (mature, OCA ported), plan 20 in 12–18 months.
  - **On 18/19, little custom code, Enterprise standard modules** → **20 later**, once 20 is a target on upgrade.odoo.com and a test cycle is clean.
  - **New features of 20 needed** (AI agents, new accounting flows) and little custom code → **20 directly**, after test cycles.
  - **Heavy custom code or Studio + OCA dependencies** → do not target 20 before the OCA dependencies exist for 20.0; budget the ir.access and OWL 3 port.
- [ ] Version jump: upgrading from 16/17/18 directly to 20 is allowed, but the code and process changes of **every skipped version add up** (e.g. 17 → 20 accumulates the 18.x, 19.x and 20 changes: `_sql_constraints`, `jsonrpc` routes, JSON-2, then ir.access and OWL 3). Size the port and the training for the whole jump, not for "20" alone.
- [ ] Business window: no go-live during closing, inventory count, payroll run or seasonal peak.

## 2. Inventory
- [ ] Edition and hosting; for Online: custom modules must be covered (§6).
- [ ] Installed modules by origin (Odoo / OCA / third-party / custom) — `inventory_instance.py`.
- [ ] Studio: custom fields (`x_`), views, reports, automations — Studio customisations are included in the upgrade only while Studio is installed and subscribed (§2).
- [ ] Automated actions and server actions with code — must be tested after upgrade (§2).
- [ ] Integrations: list every system calling Odoo (EDI, e-shop, BI, bank, scripts). Any use of XML-RPC/JSON-RPC → plan JSON-2; the `db` service no longer exists in 20; external API requires the Custom plan (§4).
- [ ] Custom reports (QWeb/PDF) and email templates — icon classes, report engine changes (§4).
- [ ] Data volumes: database size, filestore size, number of years of history.

## 3. Technical prerequisites
- [ ] On-premise: Python ≥ 3.12, PostgreSQL ≥ 16, OS Ubuntu 24.04 or Fedora 42 for packages (§1, §3). Plan the PostgreSQL major upgrade separately (dump/restore or pg_upgrade) and test it.
- [ ] Odoo.sh: staging branch available for the upgrade; custom module repositories ready for a 20.0 branch.
- [ ] Network for on-premise upgrade requests: port 443 and TCP 32768–60999 outbound (§2).
- [ ] Backups: full dump + filestore, restore tested before starting.

## 4. Custom code (run scan_addons.py)
- [ ] **Security**: every `ir.model.access.csv` → `ir.access.csv`; every `ir.rule` → domain on the access line; Python references to `ir.model.access` (§4). Blocking for every custom module.
- [ ] **OWL 3**: components using `useState`, `reactive`, `onWillUpdateProps`, `t-esc`, `t-portal`, `useComponent`, `useExternalListener`, `this.props`/`this.env`; legacy `odoo.define` widgets. The compatibility layer is temporary — port, do not rely on it (§4).
- [ ] **ORM**: old `read_group` signature; `_table_query`; `_check_access`/`_check_field_access`; binary fields/base64 handling; `copy` behaviour on names; `mail.tracking.value` reads (§4).
- [ ] **Dependencies**: `depends` on removed/merged modules (`base_vat`, `base_iban`, `stock_picking_batch`, `website_sale_wishlist`, `website_sale_comparison`, `hr_org_chart`, `hr_homeworking`, `delivery_mondialrelay`, `transifex`, `hr_work_entry_holidays`, `l10n_fr_hr_work_entry_holidays`, `industry_fsm*`) (§4).
- [ ] **Legacy syntax** for databases below 18/19: `attrs`/`states`, `<tree>`, `_sql_constraints`, `type='json'` routes, `_cr`/`_uid`/`_context` (§4).
- [ ] Run `odoo-bin upgrade_code` as a first pass, then review every change manually ("best-effort").
- [ ] Unit/integration tests of custom modules run green on 20 before any functional test.

## 5. Functional changes (only for apps in use) (§5)
- [ ] **Accounting**: bank-impacting entries must come from bank transactions (review manual bank entries, imports, integrations); account groups → parent accounts (reports, custom code, BI); payment status renaming (reports, automations, BI filters); expenses become vendor bills; taxes restricted to fiscal positions; asset models → depreciation models.
- [ ] **Inventory/Manufacturing**: return wizard removed; reorder buttons merged; HS codes per variant; flexible consumption; single Produce button; ASAP scheduling default; auto lots/serials at closing.
- [ ] **Payroll/HR**: work entries removed; work entry and time-off types merged; Remote Work merged into Employees. Validate one full payroll cycle in parallel.
- [ ] **Field Service** users: app discontinued, move to Planning; worksheets move from Studio fields to property fields — plan data and process migration.
- [ ] **Sales/Rental/Subscriptions**: lines without product, unified Prices tab.
- [ ] **POS**: closing by global sale, multi-currency; **Project**: profitability report replaced; **Repair**: "Under Repair" status removed.
- [ ] **AI**: features consume IAP credits — budget them.
- [ ] **France**: e-invoicing reception obligation since Sept 2026 — confirm the invoicing flow works end to end on the upgraded test database (PA, directory, SIREN endpoints).
- [ ] Training plan for every changed process; update internal procedures.

## 6. Licensing (§6)
- [ ] Count employees without a user account → Light User licences under agreement v13.
- [ ] Check the plan: API access, Studio and custom code need the Custom plan; Custom price changed on 24 Sept 2026 — quote current list prices with the date.
- [ ] Online with custom modules: coverage fee per 100 lines of code.
- [ ] Renewal indexation up to 7 %/year; first-year discounts are not the recurring price.

## 7. OCA and third parties (§2)
- [ ] For each OCA repository used: does a `20.0` branch exist? Is each module ported ("Migration to version 20.0" issue status)?
- [ ] Community edition: OpenUpgrade 20.0 availability and module coverage.
- [ ] Third-party apps (Odoo Apps Store): vendor's 20.0 version and support commitment.
- [ ] Fallback for each unavailable module: wait, port it ourselves (estimate), replace by standard, or drop.

## 8. Execution (§2)
- [ ] Code freeze from the first test database.
- [ ] Test database cycle ×N: request → merge filestore (on-premise) → run custom-code upgrade → automated tests → functional test scripts per process → log issues → report upgrade-script issues to Odoo support → repeat with a fresh test database.
- [ ] Neutralisation awareness: crons, mails, payments, carriers, bank sync are off on test databases — test them explicitly in a controlled way.
- [ ] Test plan covers: EDI and API integrations, automated/server actions, exports, email templates, reports, access rights per role (ir.access!), month-end closing, payroll run.
- [ ] Acceptance by written report (PV) per process owner.
- [ ] Rehearsal the day before; timed; go/no-go criteria written.
- [ ] Rollback plan: production backup + tested restore; on Odoo.sh the platform reverts a failed upgrade, but business data entered after go-live is not rolled back.
- [ ] Hypercare: 2–4 weeks, named contacts, daily triage.
