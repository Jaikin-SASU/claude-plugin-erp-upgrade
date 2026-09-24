# Microsoft Dynamics 365 Business Central — vendor facts

Checked 24 Sept 2026. [OFF] official, [THIRD] third-party, [NF] not found.

## Prices (France) [OFF] — https://www.microsoft.com/fr-fr/dynamics-365/products/business-central/pricing
- Essentials 69.30 € excl. VAT per user per month (annual payment); Premium 95.30 €; Team Members 6.90 €. "Contact a partner to buy." Minimums: [NF]. Third-party sites quoting ~85 € for France are wrong. **VOLATILE.**

## Deployment and channel [OFF]
- Online (SaaS) or on-premise (Modern Lifecycle Policy). Sold through partners (CSP) in France.

## Release cycle and support [OFF] — https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/update-rollout-timeline
- Two major updates per year (April and October), minor updates in other months.
- Online: 5-month window to apply a major update, then a 1-month grace period, then enforced update; incompatible extensions "might be automatically uninstalled".
- On-premise: each version supported about 18 months — v26 (2025 wave 1) until 14 Oct 2026; v27 (2025 wave 2) until 6 Apr 2027; v28 (2026 wave 1) until 13 Oct 2027. — https://learn.microsoft.com/en-us/lifecycle/products/dynamics-365-business-central-onpremises-modern-policy

## Customisation [OFF]
- AL extensions; modifying base application code is documented for on-premise only, Microsoft "strongly recommended to create extensions". Online = extensions only.

## Migration [OFF] — https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/migrate-nav
- From NAV: via BC 14; C/AL customisations must be converted to AL or "data from tables with code customizations can't be carried forward". Alternative: BC14 reimplementation tool (no transaction history). From GP: choose the oldest year to migrate.

## France e-invoicing
- Microsoft is not a PA; "E-Reporting FR" extension (UBL/Peppol, Factur-X) via E-Document framework to a PA or PPF. See e-invoicing-france.md.

## Quote traps
- Licences quoted without the user-type split (Essentials vs Premium vs Team Members); extensions not tested against the next two major waves; on-premise quoted without the 18-month support horizon; AppSource apps without their own licence cost; e-invoicing PA and per-invoice fees not included.
