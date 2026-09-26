# ERP Upgrade & Fit-Gap Advisor (Claude plugin)

**Choose, plan, cost and upgrade an ERP with sourced facts, not guesses.** For French SMEs and mid-size companies evaluating or running Odoo, Microsoft Dynamics 365 Business Central, Sage 100 / X3, SAP Business One, Divalto, Cegid, Sylob or EBP — with a deep **Odoo 20 upgrade** module built on Odoo 20 release day (24 Sept 2026).

Every vendor fact carries its URL, check date and certainty level (official / third-party / not found). Nothing is invented: unknowns become questions for the vendor.

*Independent plugin, not affiliated with or endorsed by any ERP vendor. Product names are trademarks of their owners.*

[Français plus bas](#français)

## Skills

Invoke as `/erp-upgrade-fit-gap:<skill>` or just describe your need — skills trigger on their own.

| Skill | You get |
|---|---|
| `choose-erp` | Standard ERP, vertical or custom? A weighted shortlist of 2–4 ERPs from your profile, sourced vendor facts, and a demo script of 5 real scenarios to impose on every vendor |
| `fit-gap` | Requirement-by-requirement matrix: standard, configuration, low-code, add-on, development or outside the ERP — with edition, plan, hosting and upgrade consequences |
| `erp-migration` | Migration plan for a version upgrade or an ERP-to-ERP move: readiness by block, data migration and reconciliation, cut-over runbook, rollback, hypercare |
| `erp-cost` | 5-year total cost per candidate on the same scope: licences by user type (only vendor-published prices, dated), hosting, implementation, integrations, upgrades |
| `review-erp-quote` | Red flags in an integrator's quote: licence counting, scope vs fit-gap, customisation and upgrade exposure, data migration, testing, cut-over, e-invoicing |
| `odoo-20-upgrade` | Deep Odoo 20 readiness in 8 blocks + read-only scanners (below) |

### Vendor references (checked 24 Sept 2026)
`references/vendors/`: Odoo, Business Central, Sage, SAP Business One, Divalto, Cegid, Sylob, EBP, and the **French e-invoicing approved-platform (PA) status of each ERP** from the official impots.gouv.fr list. Examples of what they settle: Business Central France list price 69.30 € (Essentials), SAP Business One 10.0 mainstream maintenance until 31 Dec 2028, Sage 100 V16-or-earlier contracts not renewed after 30 Nov 2026, Divalto 10.x maintenance table, which vendors are themselves a PA.

### Odoo 20 module
- 17.0 leaves standard support; +25 % fee risk for databases outside the three latest versions; Python ≥ 3.12 and PostgreSQL ≥ 16.
- `ir.model.access` + `ir.rule` merged into `ir.access` (every custom module's security to rewrite), OWL 3, new `read_group`, merged modules, XML-RPC/JSON-RPC deprecated.
- Field Service discontinued (→ Planning), payroll work entries removed, bank entries must come from bank transactions; Light User licence; Custom plan list price up about 20 % on 24 Sept 2026.
- **Read-only scripts** (Python ≥ 3.9, standard library only):
  - `scan_addons.py <addons-folder>` — static scan of custom modules, no database access, effort points per module.
  - `inventory_instance.py --url … --db …` — read-only inventory through an API key typed at a hidden prompt or piped with `--api-key-stdin` (never read from shell variables, printed or stored; hard-coded whitelist of read methods).

## MCP server `erp-facts`
The plugin connects to a read-only MCP server, **https://erp-mcp.jaikin.eu/mcp** (no account needed), that serves the same sourced vendor facts so they can be updated without reinstalling: `list_vendors`, `vendor_facts`, `support_deadlines`, `einvoicing_status`, `odoo_20_changes`, `sources_and_method`. Registry name: `eu.jaikin/erp-facts`.

## Price data
Cost and quote skills use the read-only `prix-logiciel` MCP server (French public procurement contracts and verified private-market figures), shared with the [Software Buyer France](https://github.com/Jaikin-SASU/claude-plugin-software-buyer) plugin.

## Further reading (JAIKIN, in French)
- Odoo 20: what changes and who should upgrade — [Odoo 20 : les nouveautés](https://www.jaikin.eu/blog/odoo-20-nouveautes)
- Planning an Odoo upgrade — [Migration Odoo](https://www.jaikin.eu/migration-odoo)
- Moving an SME to a new ERP — [Migration ERP PME](https://www.jaikin.eu/migration-erp-pme)
- Odoo licence and project costs — [Prix Odoo](https://www.jaikin.eu/odoo-prix)
- Odoo and French e-invoicing — [Odoo et facture électronique](https://www.jaikin.eu/odoo-facture-electronique)
- Comparing ERPs for manufacturers — [Meilleur ERP pour PME industrielle](https://www.jaikin.eu/blog/meilleur-erp-pme-industrielle-2026) · [Odoo vs Sage](https://www.jaikin.eu/odoo-vs-sage)

## Install
```
/plugin marketplace add Jaikin-SASU/claude-plugin-erp-upgrade
/plugin install erp-upgrade-fit-gap@jaikin-erp
```
Once listed in the community marketplace: `/plugin marketplace add anthropics/claude-plugins-community` then `/plugin install erp-upgrade-fit-gap@claude-community`.

## Privacy
See [PRIVACY.md](PRIVACY.md). Scripts run on your machine; your API key and data never leave it except towards your own ERP instance.

## Maintainer
Built and maintained by [JAIKIN](https://www.jaikin.eu/), Strasbourg (France). Vendor facts are re-checked periodically; issues and pull requests welcome.

---

## Français

**Choisir, planifier, chiffrer et faire évoluer un ERP avec des faits sourcés.** Pour les PME et ETI qui évaluent ou utilisent Odoo, Microsoft Dynamics 365 Business Central, Sage 100 / X3, SAP Business One, Divalto, Cegid, Sylob ou EBP, avec un module approfondi de **migration vers Odoo 20**.

- `choose-erp` : ERP standard, vertical ou sur mesure ? Liste courte pondérée et scénarios de démonstration.
- `fit-gap` : matrice exigence par exigence (standard, paramétrage, low-code, module complémentaire, développement).
- `erp-migration` : plan de migration (montée de version ou changement d'ERP), reprise des données, bascule, retour arrière.
- `erp-cost` : coût complet sur 5 ans, prix éditeurs datés uniquement s'ils sont publiés.
- `review-erp-quote` : relecture d'un devis d'intégrateur ERP.
- `odoo-20-upgrade` : préparation à Odoo 20 en 8 blocs et scripts d'analyse en lecture seule.
- Statut « plateforme agréée » (facturation électronique) de chaque ERP, d'après la liste officielle.

Plugin indépendant, non affilié aux éditeurs cités. Conçu et maintenu par [JAIKIN](https://www.jaikin.eu/), Strasbourg.
