# Registre des risques

> Probabilité notée **Faible / Moyenne / Élevée**, impact noté **Faible / Moyen / Élevé**. La colonne « Mise en œuvre » indique le jalon où la mesure s'applique. Registre revu à chaque fin de jalon.
> **Statut :** version initiale validée par le chef de projet (Richard) le 2026-09-29 ; mise à jour liée à D13 (R5) validée le 2026-09-30 — revue à chaque fin de jalon.
> **Dernière revue :** 2026-09-29 (J0)

| ID | Risque | Probabilité | Impact | Mesure prévue | Mise en œuvre | Statut |
|---|---|---|---|---|---|---|
| R1 | Une source RSS change d'URL, de format ou disparaît | Moyenne | Moyen | Sources isolées les unes des autres (une source en panne n'arrête pas les autres) ; liste modifiable dans `config/sources.yaml` ; source indisponible signalée sur la page | J1 | Ouvert |
| R2 | Le classement par mots-clés est imprécis (beaucoup d'articles en « Autres ») | Élevée | Moyen | Critère de réussite mesurable (≥ 70 % classés) ; ajustement itératif de `config/themes.yaml` ; amélioration par LLM prévue en J4 | J2, puis J4 | Ouvert |
| R3 | GitHub désactive le workflow planifié après 60 jours sans activité sur le repo | Élevée à terme | Élevé | Date de dernière mise à jour affichée sur la page ; vérification mensuelle et réactivation ; décider de la durée de vie souhaitée de la page à la clôture du projet | J3, puis continu | Ouvert |
| R4 | Dérive du périmètre (ajout de fonctionnalités avant la V1) | Moyenne | Élevé | Hors périmètre explicite dans le cahier des charges ; toute nouvelle idée va en J4 ou dans le backlog, et toute modification du périmètre est tracée dans `decisions.md` | Continu | Ouvert |
| R5 | Retard du planning (disponibilité limitée : chef de projet seul ; planning resserré depuis D13) | Élevée | Moyen | V1 volontairement minimale ; arbitrages et recettes quotidiens ; livrables de J0 utilisables indépendamment ; J4 facultatif ; écarts tracés | Continu | Ouvert |
| R6 | Réutilisation abusive du contenu des sources (droits d'auteur) | Faible | Moyen | Affichage limité au titre, à un court extrait et au lien vers l'article original ; sources citées | J3 | Ouvert |
| R7 | Coût ou fuite de la clé API lors de l'ajout du LLM (J4) | Moyenne | Moyen | Clé stockée en secret GitHub, jamais dans le code ; plafond de dépense chez le fournisseur ; fonctionnalité désactivable (retour au classement par mots-clés) | J4 | Ouvert (J4) |
| R8 | Dépendance à GitHub (Actions, Pages) | Faible | Élevé | Page HTML statique portable, hébergeable ailleurs sans modification | J3 | Accepté le 2026-09-29 |
| R9 | Divergence entre `README.md` (FR) et `README.en.md` (EN) | Moyenne | Faible | README anglais rédigé seulement en J4, une fois le README français stabilisé ; ensuite, les deux README sont modifiés dans la même pull request (case à cocher dans le modèle de pull request) | J4, puis continu | Ouvert |
| R10 | Désalignement entre `docs/sources.md` et `config/sources.yaml` | Moyenne | Faible | Test automatisé vérifiant que chaque source de la configuration est documentée | J1 | Ouvert |
| R11 | Niveaux de confiance des sources jugés arbitraires | Moyenne | Faible | Critères de chaque niveau documentés dans `sources.md` ; niveaux révisables par configuration ; toute modification tracée | J0, puis continu | Ouvert |
| R12 | Doublons de même sujet non détectés en V1 (titres différents) | Élevée | Faible | Limite acceptée et documentée pour la V1 ; doublons visibles regroupés via « Aussi couvert par » quand les titres sont proches ; détection sémantique étudiée avec le LLM en J4 | J0, puis J2, puis J4 (étude) | Accepté pour la V1 le 2026-09-29 |
