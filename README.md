# ERP Upgrade & Fit-Gap Advisor — for Odoo (Claude plugin)

**Plan Odoo projects and upgrades with sourced facts, not guesses.** Built on Odoo 20 release day (24 Sept 2026) from Odoo's official documentation, release notes and the public Community source code — every fact carries its URL, check date and certainty level.

*Not affiliated with or endorsed by Odoo S.A. "Odoo" is a trademark of Odoo S.A.*

[Français plus bas](#français)

## What it does

| Command | Skill | You get |
|---|---|---|
| `/odoo-migration-check` | `odoo-20-migration-readiness` | A traffic-light readiness report in 8 blocks (decide, inventory, prerequisites, custom code, functional changes, licensing, OCA, execution), blocking items, a phased plan, questions for your integrator, and the list of facts used with their sources |
| `/odoo-fit-gap <file>` | `odoo-fit-gap` | A requirement-by-requirement matrix: standard, configuration, Studio, OCA, development or outside Odoo — with plan and hosting consequences |
| `/odoo-cost` | `odoo-cost-estimate` | A 5-year cost: licences (incl. Light Users, first-year discount flagged), hosting, implementation or migration, maintenance |
| `/review-odoo-quote <file>` | `review-odoo-integrator-quote` | Odoo-specific red flags in an integrator's quote, plus general contract checks |

### Read-only helper scripts (Python ≥ 3.9, standard library only)
- `scan_addons.py <addons-folder>` — static scan of your custom modules, **no database access**: security files to rewrite for the new `ir.access` model, OWL 2 APIs, old `read_group` calls, tracking values, dependencies on modules removed or merged in 20, legacy view syntax, deprecated XML-RPC/JSON-RPC clients. Effort points per module.
- `inventory_instance.py --url … --db …` — read-only inventory of an instance through its API key (read from the `ODOO_API_KEY` environment variable, never printed or stored): version, modules by origin (Odoo / OCA / third-party / custom), Studio customisations, automations, internal users vs employees without user (Light User exposure). Only read methods are allowed (hard-coded whitelist).

### Key Odoo 20 facts covered (checked 24 Sept 2026)
- 17.0 leaves standard support; +25 % fee risk for databases outside the three latest versions.
- Python ≥ 3.12 and PostgreSQL ≥ 16.
- `ir.model.access` + `ir.rule` merged into `ir.access`: every custom module's security must be rewritten.
- OWL 3, new `read_group` signature, tracking values removed, several community modules merged.
- XML-RPC/JSON-RPC deprecated, `db` service removed; JSON-2 requires the Custom plan.
- Field Service discontinued (→ Planning), payroll work entries removed, bank entries must come from bank transactions, payment statuses renamed.
- Light User licence (employees without user account) in the Enterprise agreement v13; Custom plan list price up about 20 % on 24 Sept 2026.
- upgrade.odoo.com did not yet offer 20.0 as a target, and OCA had no 20.0 branches, on release day — the skill re-checks these live.

Full list with sources: [`skills/odoo-20-migration-readiness/references/odoo-20-facts.md`](skills/odoo-20-migration-readiness/references/odoo-20-facts.md).

## Price data
Cost and quote skills use the read-only `prix-logiciel` MCP server (French public procurement contracts and verified private-market figures), shared with the [Software Buyer France](https://github.com/Jaikin-SASU/claude-plugin-software-buyer) plugin.

## Install
```
/plugin marketplace add Jaikin-SASU/claude-plugin-erp-upgrade
/plugin install erp-upgrade-fit-gap@jaikin-erp
```

## Privacy
See [PRIVACY.md](PRIVACY.md). Scripts run on your machine; your API key and data never leave it except towards your own Odoo instance.

## Maintainer
Built and maintained by [JAIKIN](https://www.jaikin.eu/), Strasbourg (France). Facts are re-checked periodically; issues and pull requests welcome.

---

## Français

**Préparer un projet ou une migration Odoo avec des faits sourcés.** Conçu le jour de la sortie d'Odoo 20 (24/09/2026) à partir de la documentation officielle, des notes de version et du code Community public.

- `/odoo-migration-check` : état de préparation en 8 blocs, points bloquants, plan en phases, questions à poser à l'intégrateur.
- `/odoo-fit-gap` : matrice exigence par exigence (standard, paramétrage, Studio, OCA, développement).
- `/odoo-cost` : coût sur 5 ans (licences dont Light Users, hébergement, mise en œuvre, maintenance).
- `/review-odoo-quote` : relecture d'un devis d'intégrateur, pièges propres à Odoo.
- Scripts en lecture seule : analyse des modules maison et inventaire d'une instance (clé d'API dans une variable d'environnement, jamais affichée).

Plugin indépendant, non affilié à Odoo S.A. Conçu et maintenu par [JAIKIN](https://www.jaikin.eu/), Strasbourg.
