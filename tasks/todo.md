# Plugin n° 2 — « ERP Upgrade & Fit-Gap Advisor (for Odoo) » — PLAN À VALIDER

Rédigé le 24/09/2026 (jour de sortie d'Odoo 20). Soumission prévue APRÈS l'acceptation du plugin n° 1.

## Pourquoi
- Être trouvé par les recherches « Odoo » de l'annuaire Claude (Code + Cowork) ; public = entreprises qui préparent une migration ou une implémentation Odoo.
- Fenêtre de tir : Odoo 20 sort aujourd'hui, la 17 sort du support standard, upgrade.odoo.com n'ouvre pas encore la cible 20, l'OCA n'a aucune branche 20.0. Les gens vont chercher « que faut-il faire ? ».
- Backlink : 2e lien claude.com → www.jaikin.eu (gain SEO marginal, même domaine référent) ; l'intérêt principal est la visibilité.

## Contraintes
- « Odoo » interdit dans le NOM du plugin (marque tierce) ; autorisé dans la description. Aucune revendication de statut auprès de l’éditeur.
- Uniquement des faits publics : docs officielles, notes de version, code **Community** 20.0, OCA. **Rien tiré du dépôt Enterprise** (accès Learning Partner).
- Chaque fait Odoo 20 porte : URL, date de relevé (24/09/2026), niveau de certitude (officiel 20 / code 20 / officiel 19 / tiers). Les faits volatils (cible 20 ouverte sur upgrade.odoo.com, branches OCA 20.0) sont RE-VÉRIFIÉS en direct par le skill.
- Aucun prix Jaikin, aucun nom de client (même garde-fou check-content.sh que le plugin n° 1).

## Contenu

### Skills (anglais, réponses dans la langue de l'utilisateur)
1. **`odoo-20-upgrade`** — LA checklist approfondie, en 8 blocs :
   1. *Décider* : support (17 hors support standard en sept. 2026 ; +25 % du prix annualisé pour une base hors des 3 dernières versions, ~6 mois après la sortie ; Online : upgrade obligatoire tous les 2 ans), 19 maintenant ou 20 plus tard selon le profil.
   2. *Inventaire* : version, hébergement (Online / Odoo.sh / on-prem), modules standard / OCA / maison / Studio, intégrations (XML-RPC et JSON-RPC dépréciés, service `db` retiré en 20, JSON-2 seulement sur l'offre Custom), rapports, actions automatisées.
   3. *Prérequis techniques* : Python ≥ 3.12, PostgreSQL ≥ 16, Ubuntu 24.04 / Fedora 42 pour les paquets.
   4. *Code personnalisé* : `ir.model.access` + `ir.rule` → `ir.access` (réécriture de la sécurité de CHAQUE module), OWL 3 (22 ruptures, couche de compatibilité temporaire), nouvelle signature de `read_group`, suppression des valeurs de suivi, `_table_query`, champs binaires, modules fusionnés (`base_vat`, `stock_picking_batch`, wishlist…) → `depends` à corriger, icônes Font Awesome → Material Symbols ; restes 17/18 pour les vieilles bases (`attrs`, `tree`, `_sql_constraints`, `type='json'`) ; outil `odoo-bin upgrade_code` (« best-effort »).
   5. *Changements fonctionnels par application* : Field Service → Planning ; paie (work entries supprimées) ; compta (écritures bancaires issues des transactions, groupes de comptes → comptes parents, statuts de paiement renommés, notes de frais → factures fournisseur) ; stock et fabrication ; ventes ; PdV ; projet ; IA sur crédits IAP.
   6. *Licences* : contrat Enterprise v13 du 24/09 → **Light User** (fiches employé sans utilisateur = facturables), nouvelle définition de « User », modules maison sur Online obligatoirement « Covered ».
   7. *OCA et tiers* : aucune branche 20.0 au 24/09 ; OpenUpgrade 19 encore incomplet un an après → prévoir des mois ; vérifier chaque dépendance en direct.
   8. *Exécution* : base de test sur upgrade.odoo.com (cible 20 pas encore ouverte au 24/09), gel du code, filestore, neutralisation, tests (EDI/API, actions automatisées, exports, modèles de mail), répétition la veille, retour arrière, recette par procès-verbal.
   Sortie : un rapport « feu tricolore » par bloc, les bloquants, un plan en phases, et les questions à poser à l'intégrateur.
2. **`fit-gap`** — une matrice exigence par exigence (standard, configuration, Studio, OCA ou développement), en tenant compte des contraintes de l'offre : sur Standard, pas de modules maison ni d'API ; Custom est obligatoire pour Studio, l'API et le code maison.
3. **`erp-cost`** — licences au tarif public daté, dont Light User et la remise de 1re année signalée comme telle ; hébergement Online / Odoo.sh / sur site ; implémentation et migration via le serveur `prix-logiciel` du plugin n° 1 ; jamais « 0 € ».
4. **`review-erp-quote`** — les pièges propres à Odoo :
   - modules maison sur une offre qui ne les accepte pas ;
   - décompte des utilisateurs et des Light Users ;
   - remise de 1re année présentée comme le prix normal ;
   - migration du code maison non comprise dans l'upgrade Odoo ;
   - dépendances OCA non portées ;
   - intégrations sur XML-RPC déprécié ;
   - grade de partenaire à vérifier sur odoo.com/partners.

### Scripts locaux fournis avec le skill de migration (Python, bibliothèque standard seulement, lecture seule)
- **`scan_addons.py <dossier>`** — analyse statique des modules maison, SANS accès à la base : `ir.model.access.csv` / `ir.rule`, motifs OWL 2 (`useState`, `t-esc`, `onWillUpdateProps`, `this.props`…), appels `read_group` à l'ancienne, `_sql_constraints`, `attrs=`/`states=`, `<tree`, `type='json'`, `mail.tracking.value`, `fa-` dans les vues et rapports, `depends` vers les modules retirés ou fusionnés, `odoo.define`. Sortie JSON + score d'effort par module.
- **`inventory_instance.py`** — inventaire en lecture seule d'une instance via sa clé d'API : JSON-2 en 19 et plus, XML-RPC avant. Il liste la version, les modules installés classés (Odoo, OCA, tiers, maison), les personnalisations Studio (champs `x_`), les actions automatisées et serveur, et les utilisateurs d'API. La clé est lue dans une variable d'environnement, jamais affichée ni stockée.
- Pas de nouveau serveur MCP distant : le plugin réutilise `prix-logiciel` (mcp.jaikin.eu).

### Commandes
`/erp-upgrade-fit-gap:odoo-20-upgrade`, `/erp-upgrade-fit-gap:fit-gap`, `/erp-upgrade-fit-gap:erp-cost`, `/erp-upgrade-fit-gap:review-erp-quote`

## Étapes
- [x] 0. Validation de ce plan par Victor (nom, périmètre des scripts, calendrier) — validé par Victor le 24/09 : nom « ERP Upgrade & Fit-Gap », inventaire d'instance inclus
- [x] 1. Faits sourcés : `skills/odoo-20-upgrade/references/odoo-20-facts.md` (URL, citation, niveau de certitude)
- [x] 2. Skills + références (rédigés par Claude), commandes, README EN/FR, PRIVACY, LICENSE MIT
- [x] 3. Scripts `scan_addons.py` / `inventory_instance.py` en TDD (cursor-agent), avec des modules de test fictifs (un module 18 avec `ir.model.access.csv`, OWL 2, `read_group` à l'ancienne, `depends: stock_picking_batch`) — 21 tests
- [x] 4. Évaluations : un module piégé (le scan doit tout trouver), un devis d'intégrateur piégé, un cahier des charges pour le fit-gap — devis piégé 9/10 → checklist complétée : saut de versions cumulatif ; scan réel sur des modules 19 : effort regroupé par fichier
- [x] 5. check-content OK + `claude plugin validate` OK + installation locale
- [ ] 6. Dépôt public Jaikin-SASU/claude-plugin-erp-upgrade (accord explicite de Victor)
- [ ] 7. Soumission par Victor APRÈS l'acceptation du plugin n° 1
- [ ] 8. Rafraîchissement programmé : revérifier les faits volatils (upgrade.odoo.com, OCA 20.0, grille tarifaire) vers le 24/10 et le 24/12

## Points à trancher
1. ~~Nom : « ERP Upgrade & Fit-Gap Advisor » (recommandé) ou « ERP Migration Advisor » ?~~ → tranché : « ERP Upgrade & Fit-Gap »
2. ~~`inventory_instance.py` (connexion à la base du client avec clé d'API) : dans la v1, ou seulement le scan de code (zéro accès) ?~~ → tranché : inventaire d'instance inclus en v1

