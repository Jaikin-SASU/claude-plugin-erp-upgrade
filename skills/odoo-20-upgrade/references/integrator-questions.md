# Questions for your Odoo integrator (migration)

Format: **Question** — ✅ good answer · 🚩 red flag

1. **Does your price include porting our custom modules, or only Odoo's database upgrade?** — ✅ explicit: database upgrade by Odoo + code port by us, both priced · 🚩 "the upgrade is included in your subscription" (it does not cover custom code).
2. **How many custom modules, and how will you handle the new ir.access security model?** — ✅ module list with effort per module · 🚩 unaware of ir.access.
3. **Which of our OCA / third-party modules exist for 20.0 today, and what if one does not?** — ✅ per-module status and a fallback · 🚩 "they'll be ready".
4. **How many test-database cycles do you plan, and who tests what?** — ✅ several cycles, test scripts per process, business testers named · 🚩 one test then production.
5. **Which processes change for us in 20 (accounting, stock, payroll, field service…) and how will you train users?** — ✅ list tied to our apps · 🚩 "it's the same, just newer".
6. **Which integrations call Odoo, and are they on XML-RPC/JSON-RPC?** — ✅ inventory and JSON-2 plan · 🚩 no inventory.
7. **Why 20 now rather than 19?** — ✅ reasoned by our dependencies and features · 🚩 "always take the latest".
8. **What is the go-live date and why that date?** — ✅ outside closing and peaks, with rehearsal · 🚩 a date with no rehearsal.
9. **What is the rollback plan?** — ✅ tested restore, go/no-go criteria · 🚩 none.
10. **Is the price capped?** — ✅ fixed price per lot, capped · 🚩 time and materials "depending on surprises".
11. **Who owns the migrated code and in which repository?** — ✅ our repository, from day one · 🚩 integrator's private repository.
12. **How many licences will we pay after the upgrade (Users, Light Users) and on which plan?** — ✅ counted from our data, dated list prices · 🚩 first-year discount presented as the price.
13. **What happens to our Studio customisations?** — ✅ checked in test database, Studio subscription kept during upgrade · 🚩 unaware.
14. **Hypercare: how long, who, what response time?** — ✅ named people, 2–4 weeks · 🚩 "open a ticket".
