# French e-invoicing reform — approved platforms (PA)

Checked 24 Sept 2026. Tags: [OFF] official, [THIRD] third-party.

- Calendar: every company must be able to **receive** e-invoices since Sept 2026; SMEs must **issue** them from Sept 2027. [OFF]
- Official list of approved platforms (PA, formerly PDP): https://www.impots.gouv.fr/je-consulte-la-liste-des-plateformes-agreees — page updated 22 Sept 2026; the main file lists 149 operators meeting all conditions including interoperability tests; a second file lists 14 operators awaiting interoperability tests. [OFF] **VOLATILE — re-check the list and its update date.**
- ERP vendors and the PA they rely on (per the official list and vendor pages, 24 Sept 2026):

| ERP | Vendor itself a PA? | Route |
|---|---|---|
| Odoo | Yes — ODOO listed (15 Apr 2026) | native |
| Sage (100, X3) | Yes — SAGE listed (22 Dec 2025) | native, included up to a monthly invoice cap, then pay-per-use (sage.com) |
| Cegid XRP Flex | Yes — CEGID listed (18 Dec 2025) | native, included |
| SAP (incl. Business One) | SAP SE listed (15 Jan 2026) | Business One via SAP DRC Cloud Edition (subscription); feature described as under development in an SAP Community post [OFF, excerpt only] |
| Microsoft Dynamics 365 Business Central | No | "E-Reporting FR" extension sends documents via the E-Document framework to a PA or the public portal |
| Divalto infinity | No | PA service through Docoon (Docoon listed 15 Dec 2025) |
| Sylob | No | partnership with a PA; Esker (listed 11 Dec 2025) named in a 2023 Esker/Forterro release |
| EBP | No | native integration with Shine (listed 21 May 2026) |

What to check in any ERP project: the invoicing flow end to end (issue, receive, statuses, e-reporting) on the target version, with the chosen PA, and who pays per-invoice fees above included volumes.
