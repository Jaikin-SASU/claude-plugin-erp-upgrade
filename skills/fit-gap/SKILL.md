---
name: fit-gap
description: Build a requirement-by-requirement fit-gap analysis for an ERP project (Odoo, Microsoft Dynamics 365 Business Central, Sage, SAP Business One, Divalto, Cegid…) — which needs are covered by standard features, configuration, low-code, a partner or community add-on, or custom development — and the edition, plan, hosting and upgrade consequences. Use when the user shares requirements and asks "can <ERP> do this?", "standard or custom?", "fit-gap", "which modules do we need?", or before asking integrators for quotes.
argument-hint: <ERP(s) considered and path to the requirements>
---

# ERP fit-gap analysis

If the user passed arguments, they are: $ARGUMENTS

**Language:** answer in the user's language. Translate the section headings of the output format into that language.

## Workflow
1. Read the requirements (extract text from PDF/DOCX); number them if needed. Identify the ERP(s) considered.
2. Read `${CLAUDE_PLUGIN_ROOT}/references/vendors/<vendor>.md` for each ERP (editions, plans, customisation model, add-on ecosystem; see `${CLAUDE_PLUGIN_ROOT}/references/vendors/INDEX.md` for the file of each ERP).
3. Classify each requirement:
   - **S — Standard**: covered out of the box (name the module/feature).
   - **C — Configuration**: standard with settings, data or rules.
   - **LC — Low-code**: vendor low-code tool (e.g. Odoo Studio, Power Platform for Business Central).
   - **ADD — Add-on**: partner or community add-on (e.g. OCA module for Odoo, AppSource app for Business Central); name it and check availability for the target version.
   - **DEV — Development**: custom extension/module; size S/M/L.
   - **OUT — Outside the ERP**: specialised tool + integration, with the reason.
   Mark confidence (high / to verify in a demo). Never claim a feature exists without naming where it is.
4. Derive consequences: edition/plan required (API, low-code and custom code are often restricted to higher plans), hosting implied, upgrade exposure (every DEV and ADD line is re-tested or ported at each major version).
5. Output.

## Output format
```
## Synthesis
% by level · modules needed · edition/plan required · hosting implied · upgrade exposure.
## Fit-gap matrix
| # | Requirement | Level | How | Confidence | Notes |
## Developments and add-ons to price
| Item | Purpose | Size | Upgrade exposure |
## Decisions before quotes
## To verify in a demo
```

## Principles
- Prefer standard processes over reproducing habits; flag habits disguised as needs.
- One master system per data (customers, products, stock, prices).
- Low-code is still customisation: it ties you to a plan and must be tested at each upgrade.
- Community or partner add-ons are not maintained on your schedule: check the target version before relying on them.
- Never attribute a claim to a source you have not opened in this session: a vendor capability that is not in the plugin's references and not verified live is written "to verify in a demo" (or "to confirm with the vendor"), without citing any website.
