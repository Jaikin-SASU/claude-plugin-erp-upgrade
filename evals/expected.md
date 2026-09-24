# Critères de réussite

## /erp-upgrade-fit-gap:review-erp-quote evals/fixtures/devis-migration-odoo20-piege.md — doit détecter
1. Le service d'upgrade Odoo ne migre PAS les 9 modules spécifiques (ni les OCA) → portage du code non chiffré (ir.access, OWL 3…).
2. OCA : aucune branche 20.0 au 24/09 → modules OCA non disponibles.
3. upgrade.odoo.com n'offre pas encore la cible 20.0 au 24/09 → date du 05/10 irréaliste.
4. Connecteur XML-RPC : API dépréciée (service db retiré) ; JSON-2 requiert le plan Custom.
5. Licences : 19,90 € = remise 1re année ; Odoo.sh + modules spécifiques = plan Custom (44,90 € au 24/09) ; 60 salariés vs 25 utilisateurs → ~35 Light Users non comptés.
6. Une seule base de test, recette d'une journée par l'intégrateur (pas par le client, pas de PV), pas de répétition ni de retour arrière.
7. Régie non plafonnée pour « travaux supplémentaires » (qui seront l'essentiel).
8. Code hébergé chez l'intégrateur.
9. « Partenaire Gold certifié » : à vérifier sur odoo.com/partners.
10. Changements fonctionnels non mentionnés (formation), 17 → 20 saute la 18 et la 19 : impacts cumulés.

## scan_addons.py tests/fixtures/addons — voir tests unitaires
