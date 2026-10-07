# Bilan de projet — Veille IA

> **Statut :** en revue (pull request #44)
> **Date :** 2026-10-07
> **Références :** [cahier des charges](cahier-des-charges.md) §8 et §9, [décisions](decisions.md) (D1 à D20), [registre des risques](risques.md) (R1 à R13)

## 1. Synthèse

La V1 est en ligne depuis le 2 octobre 2026 : [stryxman.github.io/veille-ia](https://stryxman.github.io/veille-ia/). Elle rassemble chaque jour l'actualité de l'IA de 6 sources, regroupe les doublons, complète les extraits manquants, classe les articles en 6 thèmes et se publie automatiquement.

**Les 8 critères de réussite du cahier des charges sont remplis** (§2). Le projet s'est déroulé en jalons courts, avec 20 décisions tracées et validées, 13 risques suivis, 21 issues fermées par une recette et 20 pull requests fusionnées avant ce bilan. La mise en ligne a tenu sa date cible ; la clôture de J3 et de J4 a pris du retard, pour l'essentiel à cause des exécutions planifiées de GitHub (§3).

## 2. Critères de réussite (cahier des charges §9)

| # | Critère | Résultat | Preuve |
|---|---|---|---|
| 1 | Page accessible publiquement via un lien du README | ✅ Rempli | Lien en tête du README ; la page répond (HTTP 200) |
| 2 | Mise à jour automatique au moins 5 jours consécutifs sans intervention manuelle | ✅ Rempli le 2026-10-07 | Jours de l'heure de Paris avec une exécution planifiée réussie : 3, 4, 5, 6 et 7 octobre (13 exécutions planifiées, toutes réussies ; la dernière le 7 à 13:06). Décompte selon D13, précisée les 2026-10-02 et 2026-10-06 |
| 3 | 6 sources collectées ; une source volontairement cassée n'empêche pas la génération | ✅ Rempli | Bilan de chaque exécution : 6 sources lues. Essai du 2026-10-07 avec l'adresse de S6 volontairement faussée : erreur 404 signalée, page générée avec 59 actualités et la mention « Source indisponible lors de la dernière mise à jour : Le Monde Informatique — IA » |
| 4 | Aucun doublon évident (même lien ou même titre) comme article distinct | ✅ Rempli | Page en ligne du 2026-10-07 : 71 actualités, 71 liens distincts, 71 titres distincts ; tests du regroupement (D10, D16, D17) |
| 5 | Au moins 70 % des articles classés hors « Autres » | ✅ Rempli | 90 % le 1er octobre ; 76 à 81 % avec 4 thèmes (mesures des 3, 6 et 7 octobre) ; 84 % avec les 6 thèmes de D20 ; affiché à chaque exécution |
| 6 | Une source ajoutée dans `config/sources.yaml` apparaît sans modifier le code | ✅ Rempli | Essai du 2026-10-07 : ajout de Google DeepMind Blog dans une copie de la configuration ; 100 articles lus, ses actualités apparaissent sur la page générée (77 actualités) |
| 7 | Tests automatisés au vert dans l'intégration continue | ✅ Rempli | 123 tests, couverture 91 % (seuil 85 %), contrôle du code ; CI verte sur `main` |
| 8 | Documentation de pilotage à jour, issues rattachées à des jalons, board, README FR | ✅ Rempli | Cahier des charges v1.18, sources, décisions D1 à D20, risques R1 à R13, issues avec critères d'acceptation dans les jalons J0 à J4 et V2, [tableau de suivi](https://github.com/users/Stryxman/projects/1), README français et anglais avec captures |

## 3. Planning : prévu et réel

| Jalon | Échéance cible | Clôture réelle | Écart | Cause |
|---|---|---|---|---|
| J0 — Cadrage | 2026-09-29 | 2026-09-30 | +1 jour | Allers-retours de validation des documents de cadrage |
| J1 — Collecte | 2026-09-30 | 2026-09-30 | à l'heure | — |
| J2 — Traitement | 2026-10-01 | 2026-10-01 | à l'heure | — |
| J3 — Restitution (V1) | 2026-10-02 | 2026-10-06 | +4 jours (V1 en ligne à la date cible) | L'exécution planifiée du 2 octobre et le premier créneau du 3 octobre (04:17 UTC) n'ont pas eu lieu ; trois créneaux par jour ont été mis en place (#34) et la clôture attendait la preuve d'exécutions planifiées fiables (9 réussies du 3 au 5 octobre, en UTC) |
| J4 — Finitions | 2026-10-06 | prévue le 2026-10-07, à la fusion de ce bilan | +1 jour | Le critère n° 2 ne pouvait être constaté qu'après 5 jours de mises à jour automatiques, à partir du 3 octobre (règle de D13) |

Au-delà du plan initial, J3 et J4 ont intégré des travaux arbitrés en cours de route : correctifs de la revue de code de fin de J3 (#31), fiabilisation de la planification (#34), extraits manquants (#27, D18), qualité et observabilité (#39), découpage des thèmes (#26, D20). Chacun a été décidé par le chef de projet et tracé.

## 4. Risques survenus et efficacité des mesures

| Risque | Survenu ? | Effet et efficacité des mesures |
|---|---|---|
| R1 — source qui change ou disparaît | Pas en production | Isolement des sources démontré par l'essai du critère 3 ; signalement sur la page en place |
| R2 — classement imprécis | Oui, partiellement | 90 % le 1er octobre ; 76 à 81 % avec 4 thèmes (3, 6 et 7 octobre) ; 84 % avec 6 thèmes ; découpage des thèmes (D20) efficace ; les erreurs propres aux mots-clés demeurent ; LLM non retenu pour l'instant (D19) |
| R3 — désactivation du workflow planifié | Non (désactivation) ; incidents voisins suivis sous R3 | La désactivation après 60 jours n'est pas survenue. Incidents de planification suivis sous ce risque : exécution du 2 octobre et premier créneau du 3 octobre sautés, puis retards de 3 à 9 heures ; trois créneaux par jour (#34) : aucune journée sans mise à jour depuis le 3 octobre |
| R4 — dérive du périmètre | Contenue | Ajouts en J3 et J4 (#27, #31, #34, #39, #26) tous arbitrés par le chef de projet et tracés ; la synthèse demandée le 2026-10-07 est renvoyée en V2 (#43) ; mesure efficace |
| R5 — retard du planning | **Oui** | +1 jour en J0, +4 jours en J3, +1 jour en J4 ; la V1 a pourtant tenu sa date de mise en ligne ; écarts tracés au fil de l'eau |
| R6 — droits d'auteur | Non | Titre, court extrait, lien et mention des éditeurs ; extraits issus des pages limités de la même façon (D18) |
| R7 — clé API d'un LLM | Sans objet | Aucun LLM utilisé (D19) ; redevient d'actualité avec #43 (V2) |
| R8 — dépendance à GitHub | Non | Page HTML unique, sans dépendance, déplaçable |
| R9 — divergence des README | Non | README anglais créé en J4, modifié dans les mêmes pull requests que le français |
| R10 — désalignement sources.md / configuration | Non | Test automatique en place |
| R11 — niveaux de confiance arbitraires | Non | Critères documentés ; vérification indépendante des sources |
| R12 — doublons de même sujet non détectés | **Oui (limite acceptée)** | Aucun regroupement des mêmes sujets titrés différemment en français et en anglais ; limite maintenue après l'étude LLM (D19) |
| R13 — contenu malveillant dans un flux | Détecté avant tout incident | La revue de sécurité a révélé qu'un lien `javascript:` aurait pu atteindre la page ; liens filtrés, liens relatifs complétés, texte échappé, tests dédiés |

## 5. Enseignements

- **Les contrôles indépendants paient.** La recette avant chaque fusion, le contrôle de cohérence de la documentation et la revue de code de fin de jalon ont trouvé à presque chaque passage de vrais défauts : faille de lien `javascript:`, extraits mal encodés, critère de réussite ambigu, dates incohérentes, formulations trop affirmatives.
- **Mesurer sur les vrais flux.** Les tests ne voient pas ce que montrent les données réelles : dates sans fuseau, flux sans aucun texte, description de partage générique, page dont l'extracteur saute le premier paragraphe. Chaque évolution a été vérifiée sur les vrais flux avant d'être proposée.
- **Une plateforme gratuite n'est pas une plateforme garantie.** GitHub ne garantit ni l'heure ni l'exécution des lancements planifiés : la redondance (trois créneaux par jour) a été plus efficace que la recherche de l'horaire idéal.
- **Décider avec des chiffres.** Le découpage des thèmes a été mesuré sur trois jours de vrais flux avant d'être adopté ; l'étude LLM a été chiffrée avant d'être écartée.
- **Tenir les promesses écrites.** Les textes publics ont été corrigés dès qu'ils promettaient plus que le produit (heures de mise à jour, nombre de publications par jour).

## 6. Pistes d'évolution

- **Synthèse par thème avec citations** (V2, [#43](https://github.com/Stryxman/veille-ia/issues/43)) : rouvre D19 ; à cadrer avec une attention particulière à la sécurité du jeton d'accès.
- **Doublons de même sujet** (R12) : à reconsidérer si un modèle de langage est adopté.
- **Maintenance** : figer les versions des dépendances et des actions GitHub ; suivre la migration de GitHub Actions (Node 24, Ubuntu 26 à partir du 2026-10-19) ; vérifier chaque mois que le workflow planifié reste actif (R3, désactivation après 60 jours sans activité).
- **Points mineurs reportés** pendant les revues : nettoyage du HTML de certains flux, comparaison des liens (http/https, www), quelques cas de dates et de compteurs ; aucun n'affecte les critères de réussite.
