# Odoo — vendor facts and traps

Checked 24 Sept 2026. Deep Odoo 20 facts with sources: `${CLAUDE_PLUGIN_ROOT}/skills/odoo-20-upgrade/references/odoo-20-facts.md`. Re-check volatile items live (pricing, upgrade targets, OCA branches).

## Editions, plans and hosting
- Editions: Community (open source, LGPL) and Enterprise (subscription).
- Enterprise plans: **Standard** and **Custom**. "Access to data via the external API is only available on Custom Odoo pricing plans." Studio is listed in the Custom plan. — https://www.odoo.com/documentation/20.0/developer/reference/external_api.html · https://www.odoo.com/pricing
- Hosting: Odoo Online (SaaS), Odoo.sh (PaaS with Git repositories for custom modules), on-premise.
- Custom modules: Odoo.sh or on-premise; on Odoo Online they must be "Covered" (maintenance fee per 100 lines of code, Enterprise agreement v13 of 24 Sept 2026).
- "Standard" is both a plan name and a way of working ("standard Odoo, no custom module"): documents must say which one they mean.

## Prices (VOLATILE — EUR per user per month, yearly billing, checked 24 Sept 2026)
- Standard 24.90 € (19.90 € first-year discount).
- Custom 44.90 € (35.90 € first-year discount) — up about 20 % from 37.40 € observed on 23 Sept 2026.
- Light User (employee record without user account, agreement v13): "at 7,90 €" via an Odoo advisor — to confirm.
- Renewal indexation "up to 7% per year". First-year discounts are not the recurring price. — https://www.odoo.com/fr_FR/pricing

## Versions and support
- One major version per year (autumn); standard support 3 years; +25 % fee risk for databases older than the 3 latest versions; Odoo Online forces an upgrade every 2 years. Details and sources in odoo-20-facts.md §1.
- Enterprise: official upgrade service (upgrade.odoo.com) for standard modules and Studio; custom and uncovered partner modules are **not** ported by it. Community: OCA OpenUpgrade.

## Customisation model
- Python modules (ORM) + XML views + OWL front-end; Studio for low-code. Custom code must be ported at each major version (Odoo 20: ir.access security rewrite, OWL 3…).
- OCA (Odoo Community Association) modules: free, community-maintained, ported to each version on the community's schedule.

## France
- Odoo is registered as an approved e-invoicing platform (PA) in France. — https://www.odoo.com/blog/odoo-news-5/odoo-an-approved-platform-pa-registered-in-france-for-electronic-invoicing-2193

## Quote traps
- Licences at the first-year discount; Light Users not counted; Standard plan quoted while the scope needs API, Studio or custom code (Custom plan).
- "Custom modules will be migrated automatically by Odoo's upgrade service" — false for custom and uncovered partner modules.
- OCA dependencies without a target-version branch; integrations on deprecated XML-RPC/JSON-RPC; custom code kept in the integrator's private repository.
- Partner grade claims: verify on https://www.odoo.com/partners.
