# ERP selection criteria (weights are defaults — adapt them)

| # | Criterion | Default weight | What to check |
|---|---|---|---|
| 1 | Core process coverage | 25 | Fit-gap on the 10 processes that make the company's margin (standard vs configuration vs development) |
| 2 | Sector fit | 10 | Vertical features (e.g. manufacturing: routings, MRP, traceability, quality; distribution: WMS, pricing; projects: time and cost) and local references in the same sector |
| 3 | Total cost over 5 years | 15 | Licences by user type, hosting, implementation, integrations, upgrades, internal time |
| 4 | Upgrade policy and customisation model | 10 | Release cadence, mandatory SaaS updates, how customisations are built (extensions vs code changes) and survive upgrades |
| 5 | Deployment options | 5 | Vendor SaaS, partner cloud, on-premise; data location; exit (data export) |
| 6 | Integration capabilities | 10 | Documented APIs, plan restrictions on API access, connectors to the company's tools |
| 7 | France compliance | 10 | E-invoicing (approved platform or partner), FEC, payroll localisation if needed, accounting standards |
| 8 | Partner ecosystem | 10 | Integrators available near the company, their size, certifications (verified on the vendor's public partner directory), references |
| 9 | Usability and adoption | 5 | Demo on real scenarios by future users |

## Family decision
- **Standard ERP**: most processes are common practice; accept adapting habits.
- **Standard + vertical add-on**: a sector-specific layer from the vendor's ecosystem.
- **Sector ERP**: the sector's rules dominate (e.g. regulated traceability, complex configure-to-order).
- **Custom software**: the core process is the differentiator and would require heavy development on any ERP; often combined with a standard accounting package.

## Demo script rules
Five scenarios from the company's real week (e.g. "quote with options → order → purchase of components → production → partial delivery → invoice → payment"), with the company's data, performed by the vendor live, scored by future users.
