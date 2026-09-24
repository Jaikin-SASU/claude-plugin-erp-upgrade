---
name: choose-erp
description: Help a French SME or mid-size company choose an ERP (Odoo, Microsoft Dynamics 365 Business Central, Sage 100 / Sage X3, SAP Business One, Divalto, Cegid, Sylob, EBP…) or decide between a standard ERP and custom software. Builds a weighted shortlist from the company's profile, processes and constraints, with sourced vendor facts (deployment, pricing model, upgrade policy, e-invoicing readiness). Use when the user asks "which ERP should we choose?", "quel ERP pour une PME industrielle ?", "Odoo or Business Central?", "ERP or custom software?".
argument-hint: <company profile: sector, size, sites, current tools, key processes>
---

# Choose an ERP

If the user passed arguments, they are: $ARGUMENTS

**Language:** answer in the user's language. Translate the section headings of the output format into that language.

## Workflow
1. **Profile** (ask only what is missing): sector and business model (distribution, manufacturing to stock / to order / engineer-to-order, projects, services, retail), size (employees, ERP users, companies, sites, countries), current tools and pain points, must-have processes, integrations, hosting constraints, IT team, budget range, deadline and why.
2. **Decide the family first**: standard ERP, standard ERP + vertical add-on, sector ERP, or custom software (when the core process is the company's differentiator and no standard covers it). Say why.
3. **Shortlist 2–4 candidates** with `references/selection-criteria.md`. For each vendor, read `${CLAUDE_PLUGIN_ROOT}/references/vendors/<vendor>.md` when it exists (see `${CLAUDE_PLUGIN_ROOT}/references/vendors/INDEX.md` for the file of each ERP); use only facts found there or verified live with URL and date. Never quote a price that is not published by the vendor; otherwise write "on quote".
4. **Score** each candidate on the weighted criteria; show the weights and let the user change them.
5. **Check e-invoicing readiness** (France): is the ERP's vendor or its chosen partner a registered approved platform (PA)? Verify on the official list on impots.gouv.fr with its update date.
6. **Next steps**: fit-gap on the top 2 (see the fit-gap skill), demo scripts built on the company's real cases, reference calls.

## Output format
```
## Recommendation
Family (standard / vertical / custom) and the 2–3 candidates to evaluate, in 3 sentences.

## Profile summary
## Scoring
| Criterion | Weight | Candidate A | Candidate B | Candidate C |
## Why each candidate (and why not)
## Facts used (vendor — fact — URL — date)
## Demo script: 5 real scenarios to ask every vendor to perform
```

## Principles
- Choose an ERP on the company's core processes demonstrated with its own data, not on feature lists.
- Total cost over 5 years (licences, hosting, implementation, upgrades), not the first-year price.
- Upgrade policy matters as much as features: how often, how disruptive, how customisations survive.
- No vendor is recommended without a fit-gap and a demo on real scenarios.
- Never attribute a claim to a source you have not opened in this session: a vendor capability that is not in the plugin's references and not verified live is written "to verify in a demo" (or "to confirm with the vendor"), without citing any website.
