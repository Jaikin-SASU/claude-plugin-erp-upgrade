Les contrôles sont terminés : fiche de faits Odoo 20 du plugin, vérifications en direct du 24/09/2026, positionnement prix. Voici la revue.

# Revue du devis ERPNova — migration Odoo 17 → 20 (Transports Lemoine)

## Verdict : ne pas signer en l'état

Le forfait de 6 000 € ne couvre pas le gros du travail : le portage de 9 modules custom, 6 modules OCA et 2 connecteurs. Trois affirmations du devis sont fausses ou invérifiables :
- la migration « automatique » ;
- la mise en production le 5 octobre sur une version sortie le jour du devis ;
- les connecteurs « à l'identique ».

Le budget réel est ouvert : la régie à 850 €/j n'est pas plafonnée. Les licences sont sans doute sous-estimées, de +25 % à ×2,8 selon le plan et les Light Users.

## Points rouges

### Bloquants

**1. Portage du code custom présenté comme « automatique » (§1)**
> « Vos 9 modules spécifiques et vos 6 modules OCA […] seront migrés automatiquement par le service de mise à niveau inclus dans votre abonnement Odoo. »

- Le service Odoo met à niveau la base, les modules standard et Studio. Il ne porte pas les modules custom non couverts ni les modules partenaires ou tiers. Il ne couvre du custom que s'il est sous abonnement de maintenance Odoo, ce que le devis ne dit pas. [OFF-20, [upgrade](https://www.odoo.com/documentation/20.0/administration/upgrade.html)]
- Rien n'est chiffré pour la réécriture des fichiers de sécurité de chaque module (`ir.model.access` et `ir.rule` deviennent `ir.access`), pour OWL 3, ni pour le nouveau `read_group`. Les dépendances supprimées ou fusionnées, comme `stock_picking_batch` désormais dans `stock`, ne sont pas chiffrées non plus. [OFF-20/CODE-20, fiche §4]
- OCA, contrôle en direct le 24/09/2026 à 17:36 UTC : il n'existe pas de branche `20.0` pour `OCA/stock-logistics-workflow` ni pour `OCA/account-financial-tools` (API GitHub, HTTP 404). Le devis ne prévoit aucun repli.
- Ordre de grandeur : 6 000 € font 7,06 j à 850 €, soit environ 0,47 j par module, tests et mise en production compris.

**2. Version 20 « dès maintenant » et mise en production le 05/10/2026 (§1, §3)**
- Le devis est daté du jour de sortie d'Odoo 20. Ce jour-là, upgrade.odoo.com ne proposait que 19.0, 18.0 et 17.0 comme cibles, sans date d'ouverture annoncée pour la 20.0. Cette information est volatile. [fiche §2, https://upgrade.odoo.com/] Ma vérification en direct par `curl` n'a rien trouvé de contraire, mais la page est probablement rendue en JavaScript, donc ce contrôle est faible.
- La « base de test » du §3 ne peut donc pas être produite par le service Odoo à cette date.
- Il reste 6 jours ouvrés entre le 25/09 et le lundi 05/10, sans répétition ni justification de la date.
- Le devis ne justifie pas non plus le choix de la 20 plutôt que de la 19. « Profiter des nouveautés » n'en nomme aucune. Les fonctions IA de la 20 consomment des crédits IAP payants.
- Il y a bien une échéance, mais elle est plus lointaine. La 17 sort du support standard en septembre 2026. Odoo peut facturer +25 % du prix annualisé pour une base hors des 3 dernières versions, au plus tôt vers fin mars 2027. Cela représente environ +1 500 € sur la base du devis. [OFF-20 + DÉDUIT, fiche §1] Le calendrier se compte donc en mois, pas en 11 jours.

**3. Budget non plafonné (§2, §5)**
> « Travaux supplémentaires éventuels facturés en régie à 850 € HT/jour. »

Le forfait exclut l'essentiel du travail (point 1), et la régie n'est ni définie ni plafonnée. Les « surprises » sont donc certaines et sans limite de coût.

### Majeurs

**4. Licences sous-estimées (§2)**
- Le devis compte 19,90 € × 25 = 5 970 €/an. C'est le prix Standard avec remise de première année. Le tarif public récurrent est de 24,90 €.
- Le plan n'est pas nommé. Un connecteur XML-RPC, une synchronisation e-commerce et 9 modules custom relèvent du plan Custom : l'API externe n'est accessible que sur les plans Custom. [OFF-20, fiche §4]
- Les Light Users ne sont pas comptés. Avec 60 salariés pour 25 utilisateurs, jusqu'à 35 fiches employé sans compte pourraient être facturées, si l'app RH est utilisée. [fiche §6]

| Scénario (25 utilisateurs) | €/mois | €/an |
|---|---|---|
| Devis : Standard, remise 1re année (19,90 €) | 497,50 | 5 970 |
| Standard, tarif public (24,90 €) | 622,50 | 7 470 |
| Custom, remise 1re année (35,90 €) | 897,50 | 10 770 |
| Custom, tarif public (44,90 €) | 1 122,50 | 13 470 |
| + Light Users (≤ 35 × 7,90 €, via conseiller, **à confirmer**) | +276,50 | +3 318 |

- Source : https://www.odoo.com/fr_FR/pricing, relevé du 24/09/2026. Le plan Custom valait 37,40 € la veille, soit +20 % le jour de la sortie de la 20.
- La revalorisation annuelle peut aller jusqu'à +7 %.
- Le client est déjà sur Odoo 17 Enterprise. Son plan actuel et son éligibilité à la remise de première année sont à confirmer auprès d'Odoo.

**5. Intégrations « à l'identique » (§1)**
- XML-RPC et JSON-RPC sont dépréciés. Le service `db` est supprimé en 20. Les services `common` et `object` sont annoncés pour retrait en Odoo 22 (automne 2028). Le remplaçant est JSON-2, disponible depuis la 19.0. [OFF-20, [external_api](https://www.odoo.com/documentation/20.0/developer/reference/external_api.html)]
- Le devis ne contient ni inventaire des appels ni plan JSON-2.
- Le connecteur transporteur casse s'il utilise le service `db`. S'il utilise seulement `common` et `object`, il devrait tourner en 20 mais avec un horizon de retrait à 2028 [DÉDUIT].
- Vérifier aussi qu'il ne dépend pas d'un module supprimé, par exemple `delivery_mondialrelay`.

**6. Recette et bascule (§3, §4)**
> « Une journée de tests par nos consultants »

- Une seule base de test, testée par l'intégrateur lui-même.
- Aucun scénario par processus, aucun testeur métier, aucune répétition, aucun plan de retour arrière, aucun procès-verbal de recette.
- Odoo recommande de geler le code, de redemander plusieurs bases de test et de répéter la veille de la mise en production. [OFF-20, [upgrade_custom_db](https://www.odoo.com/documentation/20.0/developer/howtos/upgrade_custom_db.html)]
- Sur Odoo.sh, une mise à niveau de production qui échoue est annulée automatiquement. Cela ne remplace pas un plan de retour arrière métier.

**7. Code chez l'intégrateur (§5)**
> « Code des modules hébergé sur notre GitLab. »

Le dépôt appartient à l'intégrateur, sans cession ni licence explicites (LGPL ou OPL). Cela crée une dépendance et un coût de sortie. Le dépôt doit être au nom du client dès le premier jour.

**8. Processus, Studio et données absents**
Le devis ne parle ni de formation, ni de Studio, ni de reprise et nettoyage des données. Odoo ne couvre ni le nettoyage ni la formation. Or la 20 modifie plusieurs processus : écritures bancaires issues des transactions, statuts de paiement renommés, assistant de retour de stock supprimé, planification des OF par défaut. [fiche §5] Les apps utilisées par Transports Lemoine ne sont pas listées.

### Mineurs
- « Partenaire Gold certifié » n'est pas vérifiable dans le devis. À contrôler sur https://www.odoo.com/partners.
- « 497,50 €/mois » suggère une facturation mensuelle, alors que le prix cité est un prix annuel remisé. Le devis ne dit pas non plus qui facture les licences, alors qu'elles sont payées à Odoo.
- Le devis ne mentionne ni durée de validité, ni échéancier de paiement, ni garantie, ni hypercare, ni sous-traitance des données (RGPD), ni réversibilité.

## Positionnement prix

`position_quote` (ERP, 6 000 €, DECP, 24/09/2026) renvoie `out_of_range` : n=21, minimum 7 838 €, médiane 135 000 €. Ces données sont des marchés publics, souvent des plafonds pluriannuels licences et maintenance comprises. Elles ne sont pas comparables à une migration de 25 utilisateurs, donc **aucun repère exploitable**. Le 6 000 € ne prouve ni bon prix ni mauvais prix : il signale un périmètre incomplet.

Côté tarif journalier, `daily_rates` ne renvoie aucun profil Odoo. Le profil « Consultant ERP » indique 607 € en direct et 569 € via intermédiaire (Free-Work 2026). Le 850 €/j d'une agence n'est pas choquant en soi. Le vrai sujet est l'absence de plafond.

## Questions à poser à ERPNova

1. Le prix inclut-il le portage de nos 9 modules custom ? Demandez un détail en jours par module, avec `ir.access` et OWL 3. Sont-ils couverts par une maintenance Odoo ?
2. Quel est le statut 20.0 de chacun des 6 modules OCA aujourd'hui, et quel est le repli s'il n'est pas porté ?
3. Pourquoi la 20 plutôt que la 19, ou plutôt que d'attendre l'ouverture de 20.0 sur upgrade.odoo.com ? Comment produire la base de test avant le 05/10 ?
4. Quels appels API existent (`db`, `common`, `object`) et quel est le plan JSON-2 ? Sous quel plan Odoo ?
5. Combien de cycles de test, avec quels scénarios, quels testeurs métier nommés, quelle répétition et quel plan de retour arrière ?
6. Pourquoi le 05/10, hors clôture et hors pic d'activité ?
7. Le forfait est-il plafonné par lot ? Que couvre exactement la régie, et jusqu'à quel montant ?
8. Combien d'Users et de Light Users faut-il compter, sur quel plan, à quel prix daté ? Qu'en est-il de Studio ?
9. Le dépôt sera-t-il au nom du client dès le jour 1, avec quelle licence ?
10. Quel hypercare est prévu (durée, personnes, délai de réponse) ?
11. Quel lien vers la fiche de partenaire dans l'annuaire Odoo ?

## Suite recommandée

Demandez un devis révisé avec les éléments suivants :
- inventaire et jours par module, plus les intégrations ;
- forfait plafonné par lot ;
- 2 à 3 cycles de test avec recette écrite ;
- dépôt de code au nom du client ;
- licences recomptées (Users, Light Users, plan, prix daté).

Visez une mise en production avant fin mars 2027, quand la cible 20.0 sera ouverte et les modules OCA disponibles. Passer par la 19 maintenant obligerait à migrer une seconde fois vers la 20, ce que je déconseille (avis, non source).

Cette revue ne constitue pas un avis juridique. Faites relire le contrat par un juriste avant signature. Le plugin `software-buyer-france` n'est pas visible dans cette session : les points contractuels généraux sont traités ici brièvement.
