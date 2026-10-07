# Journal de décisions

> Chaque choix structurant du projet est consigné ici : contexte, options envisagées, décision et justification.
> **Décideur :** Richard (chef de projet). Les options sont préparées avec l'assistance de Claude Code.
> **Statut :** décisions D1 à D17 validées par le chef de projet (D1 à D12 le 2026-09-29, D13 à D15 le 2026-09-30, D16 et D17 le 2026-10-01) ; précision de D13 (départ du critère n° 2) validée le 2026-10-02 (pull request #33) ; précision de D13 (fuseau du décompte) validée le 2026-10-06 (pull request #40) ; précision de D14 (nommage, complexité, couverture) validée le 2026-10-06 (pull request #41) ; D18 validée le 2026-10-03 (pull request #36) ; D19 validée le 2026-10-03 (pull request #37) ; D20 validée le 2026-10-07 (pull request #42) ; précision de D18 en revue (pull request #46).

| ID | Date | Sujet | Décision |
|---|---|---|---|
| D1 | 2026-09-29 | Mode de restitution | Page web statique (GitHub Pages) |
| D2 | 2026-09-29 | Stack technique | Python |
| D3 | 2026-09-29 | Exécution et hébergement | GitHub Actions planifié + GitHub Pages |
| D4 | 2026-09-29 | Méthode de classement | Mots-clés en V1, LLM en J4 (étudié, non retenu : D19) |
| D5 | 2026-09-29 | Sources et fréquence | ~6 flux RSS FR + EN, mise à jour quotidienne |
| D6 | 2026-09-29 | Langue du projet | Docs et page en français, code en anglais |
| D7 | 2026-09-29 | Nom et visibilité du repo | `veille-ia`, public dès J0 |
| D8 | 2026-09-29 | Méthode de suivi | Kanban + jalons |
| D9 | 2026-09-29 | Documentation en anglais | `README.en.md` seul, rédigé en J4 ; docs de pilotage en français |
| D10 | 2026-09-29 | Article retenu parmi des doublons | Niveau de confiance par source, puis antériorité ; doublons en « Aussi couvert par » |
| D11 | 2026-09-29 | Articles sans date de publication | Conservés, datés de leur date de collecte, étiquette « Date de publication inconnue » |
| D12 | 2026-09-29 | Contrôle qualité | Vérification indépendante aux moments clés : recette prouvée, sources, cohérence documentaire |
| D13 | 2026-09-29 | Replanification | Mise en ligne de la V1 avancée du 2026-10-14 au 2026-10-02 |
| D14 | 2026-09-30 | Outillage de développement | ruff (qualité et format du code) ; pip + venv, dépendances dans `pyproject.toml` ; nommage, complexité et couverture ≥ 85 % contrôlés (2026-10-06) |
| D15 | 2026-09-30 | Dates publiées sans fuseau horaire | Fuseau déclaré par source dans la configuration (UTC par défaut) |
| D16 | 2026-10-01 | Règles de regroupement des doublons | Nombres différents = actualités différentes ; comparaison avec l'article retenu, sans chaînage |
| D17 | 2026-10-01 | Garde sur les mots pour le regroupement | Un mot d'au moins 3 lettres présent dans un seul des deux titres = actualités différentes |
| D18 | 2026-10-03 | Extraits manquants | Début du texte principal de la page de l'article, extrait avec `trafilatura` ; site de la source seulement, 120 s au plus (2026-10-07) |
| D19 | 2026-10-03 | Modèle de langage (LLM) | Pas de LLM pour l'instant : classement par mots-clés conservé |
| D20 | 2026-10-07 | Découpage des thèmes | « Modèles & recherche » découpé en Modèles, Agents, Recherche & évaluation |

---

## D1 — Mode de restitution

- **Date :** 2026-09-29
- **Contexte :** le résumé de veille doit être consultable facilement, sans installation.
- **Options envisagées :**
  1. Page web statique sur GitHub Pages — visible en un clic, gratuite, pas d'identifiants à gérer.
  2. Email récapitulatif — s'intègre aux habitudes de lecture, mais sans point d'accès public permanent ; nécessite un compte SMTP, des secrets et de la gestion de délivrabilité.
  3. Les deux dès la V1 — plus complet, mais double l'effort de restitution et retarde la V1.
- **Décision :** option 1, page web statique.
- **Justification :** consultation en un clic par tout lecteur, coût nul, moins de risques techniques. L'email reste une évolution possible en J4.

## D2 — Stack technique

- **Date :** 2026-09-29
- **Contexte :** choix du langage pour la collecte, le traitement et la génération de la page.
- **Options envisagées :**
  1. Python — bibliothèques matures (`feedparser`, `Jinja2`), code concis, écosystème de référence pour le traitement de données.
  2. JavaScript / Node — faisable, sans avantage particulier pour ce besoin.
  3. Outil no-code (Make, n8n, Zapier) — rapide, mais logique difficile à versionner et à tester, souvent payant.
- **Décision :** option 1, Python.
- **Justification :** adapté au besoin, lisible, et facilite les évolutions prévues (traitement de texte, appel à un LLM).

## D3 — Exécution et hébergement

- **Date :** 2026-09-29
- **Contexte :** la veille doit se mettre à jour régulièrement sans intervention.
- **Options envisagées :**
  1. GitHub Actions planifié + GitHub Pages — gratuit pour un repo public, aucune machine à maintenir, historique d'exécution visible.
  2. Exécution manuelle en local — simple, mais la page devient obsolète dès qu'on arrête.
  3. Serveur / VPS — coûteux, administration nécessaire, hors périmètre d'une V1 rapide.
- **Décision :** option 1, GitHub Actions planifié + GitHub Pages.
- **Justification :** automatisation réelle à coût nul, avec un historique d'exécution consultable.

## D4 — Méthode de classement par thème

- **Date :** 2026-09-29
- **Contexte :** les articles doivent être regroupés par thème pour être lisibles.
- **Options envisagées :**
  1. Mots-clés en V1, LLM en J4 — transparent, gratuit, testable ; amélioration par LLM dans un second temps.
  2. LLM dès la V1 — résultat plus fin, mais clé API (coût, secret), sorties non déterministes, V1 retardée.
  3. Mots-clés uniquement — le plus sûr, mais sans possibilité d'améliorer la qualité du classement au-delà des mots-clés.
- **Décision :** option 1, mots-clés en V1 puis LLM en J4.
- **Justification :** livrer vite une V1 fiable, puis enrichir de façon incrémentale en maîtrisant le risque (coût, secret, qualité).
- **Suite :** le LLM a été étudié en J4 et n'est pas retenu pour l'instant (D19, 2026-10-03).

## D5 — Sources et fréquence de mise à jour

- **Date :** 2026-09-29
- **Contexte :** choix des sources de collecte et du rythme de mise à jour.
- **Options envisagées (sources) :**
  1. Mix français + anglais, environ 5 à 6 flux RSS — bonne couverture, le dédoublonnage prend son sens.
  2. Français uniquement — lisible, mais peu de sources spécialisées.
  3. Anglais uniquement — meilleures sources, mais contenu en anglais.
- **Options envisagées (fréquence) :**
  1. Quotidienne — page toujours à jour lors d'une consultation.
  2. Hebdomadaire — format « récap », mais page jusqu'à 6 jours d'ancienneté.
- **Décision :** mix FR + EN (6 flux, détaillés dans [sources.md](sources.md)) ; mise à jour quotidienne, affichage des 7 derniers jours.
- **Justification :** couverture représentative de l'actualité IA et page toujours fraîche, sans surcoût.

## D6 — Langue du projet

- **Date :** 2026-09-29
- **Contexte :** langue des documents, de la page et du code.
- **Options envisagées :**
  1. Documentation et page en français, code en anglais.
  2. Tout en français.
  3. Tout en anglais.
- **Décision :** option 1.
- **Justification :** documentation accessible au public visé (francophone) et respect des conventions de développement pour le code.

## D7 — Nom et visibilité du repo

- **Date :** 2026-09-29
- **Contexte :** identité du repo et moment de sa publication.
- **Options envisagées :**
  1. `veille-ia`, public dès J0.
  2. `ai-news-digest`, public dès J0.
  3. Privé jusqu'à la V1.
- **Décision :** option 1, `veille-ia`, public dès J0.
- **Justification :** nom clair pour un lecteur francophone ; le suivi (issues, jalons, board) est consultable par tout lecteur, et GitHub Pages / Actions sont gratuits en public.

## D8 — Méthode de suivi

- **Date :** 2026-09-29
- **Contexte :** organisation du suivi d'avancement.
- **Options envisagées :**
  1. Kanban (À faire / En cours / Revue / Terminé) + jalons GitHub.
  2. Sprints Scrum d'une semaine.
- **Décision :** option 1, kanban + jalons.
- **Justification :** adapté à un projet court mené seul ; les rituels Scrum seraient artificiels à cette échelle.

## D9 — Documentation en anglais

- **Date :** 2026-09-29
- **Contexte :** la documentation est en français (D6) ; il faut rendre le projet compréhensible pour des lecteurs non francophones.
- **Options envisagées :**
  1. `README.en.md` seul — présentation complète en anglais, lien croisé FR ⇄ EN ; docs de pilotage en français. Une seule traduction à maintenir.
  2. README + cahier des charges en anglais — cadrage accessible aussi, mais double maintenance du document le plus modifié.
  3. Toute la documentation doublée — le plus complet, mais maintenance lourde et risque de divergence.
- **Décision :** option 1, `README.en.md` seul.
- **Justification :** le README est le point d'entrée du projet ; le traduire seul donne l'essentiel à un lecteur anglophone pour un coût de maintenance limité.
- **Mise en œuvre :** le README anglais est rédigé en J4, une fois le README français stabilisé, afin que les deux versions décrivent le même état du projet (R9).

## D10 — Choix de l'article retenu parmi des doublons

- **Date :** 2026-09-29
- **Contexte :** lorsqu'une information est publiée par plusieurs sources, la règle initiale (« garder le plus ancien ») peut privilégier une source moins pertinente, par exemple un média généraliste qui publie avant un média spécialisé.
- **Options envisagées :**
  1. Niveau de confiance attribué à chaque source dans la configuration, puis antériorité à niveau égal — transparent, testable, modifiable sans code.
  2. Score calculé par article (source, longueur, vocabulaire…) — plus fin en apparence, mais opaque et difficile à régler.
  3. Jugement de pertinence par un LLM — meilleure qualité, mais dépend de la décision sur le LLM (J4).
- **Hiérarchie envisagée :** source primaire > presse spécialisée > presse généraliste, ou presse spécialisée > source primaire > presse généraliste.
- **Affichage des doublons envisagé :** suppression simple, ou mention « Aussi couvert par » sous l'article retenu.
- **Décision :** option 1, avec la hiérarchie **source primaire (1) > presse spécialisée IA/tech (2) > presse généraliste ou hors tech (3)** ; les autres articles du groupe sont affichés en « Aussi couvert par », avec leurs liens.
- **Justification :** l'information de première main prime, puis l'expertise du média ; la règle reste explicable et vérifiable. Afficher les autres sources ne perd aucune information et indique l'importance d'une actualité.
- **Limite connue :** en V1, seuls les titres quasi identiques sont reconnus comme doublons ; la détection de « même sujet, titres différents » relève d'une analyse sémantique, à étudier avec le LLM en J4. Étude faite en J4 : LLM non retenu pour l'instant (D19).

## D11 — Articles sans date de publication

- **Date :** 2026-09-29
- **Contexte :** certains flux publient des articles sans date. Il faut décider s'ils sont affichés et comment les situer dans le temps.
- **Options envisagées :**
  1. Exclure les articles sans date — simple, mais perte d'informations potentiellement récentes.
  2. Les conserver en les datant de leur date de collecte, sans le signaler — aucune perte, mais date affichée potentiellement trompeuse.
  3. Les conserver en les datant de leur date de collecte et en le signalant par une étiquette — aucune perte, et le lecteur sait que la date est approximative.
- **Décision :** option 3. La date de collecte sert au tri et à la fenêtre de 7 jours ; la page affiche l'étiquette « Date de publication inconnue ».
- **Justification :** ne perdre aucune information tout en restant transparent sur la fiabilité de la date affichée.

## D12 — Contrôle qualité

- **Date :** 2026-09-29
- **Contexte :** les documents du projet se répondent (cahier des charges, sources, décisions, risques, issues) ; une modification non répercutée partout, ou un critère d'acceptation déclaré rempli sans preuve, dégrade la fiabilité du pilotage.
- **Options envisagées :**
  1. Contrôle par la personne qui réalise — rapide, mais les oublis de la réalisation se retrouvent dans le contrôle.
  2. Vérification indépendante à des moments clés — un contrôle distinct de la réalisation, déclenché à des étapes définies.
- **Décision :** option 2, avec trois points de contrôle :
  - **Recette avant fermeture d'une issue :** chaque critère d'acceptation est vérifié un par un, preuve à l'appui (test, commande, capture) ; tout ajout hors périmètre est signalé.
  - **Vérification des sources :** à chaque ajout de source ou changement de niveau de confiance, un avis indépendant est établi avant comparaison avec le niveau proposé, et le flux est testé.
  - **Cohérence documentaire :** avant chaque enregistrement (commit) touchant la documentation ou la configuration, on vérifie que la modification est répercutée dans tous les documents concernés.
- **Justification :** séparer la réalisation du contrôle limite les incohérences entre documents et les critères validés sans preuve ; les points de contrôle sont ciblés pour garder un coût raisonnable.

## D13 — Replanification : mise en ligne de la V1 avancée

- **Date :** 2026-09-29
- **Contexte :** le planning initial (V1 le 2026-10-14) laissait une large marge. Le périmètre de la V1 est volontairement réduit (6 flux RSS, règles simples, une page statique) et peut être livré plus tôt ; un produit en ligne rapidement permet de mesurer son fonctionnement réel plus tôt.
- **Options envisagées :**
  1. V1 le 2026-10-02 — J0 le 29/09, J1 le 30/09, J2 le 01/10, J3 le 02/10, J4 le 06/10 ; suppose des arbitrages et recettes quotidiens.
  2. V1 le 2026-10-03 — une journée de marge sur le traitement (doublons, classement), la partie la plus délicate.
  3. Jalons sans échéance — souple, mais sans mesure des écarts entre prévu et réel.
- **Décision :** option 1, V1 en ligne le 2026-10-02.
- **Justification :** mise en ligne au plus tôt sur un périmètre maîtrisé ; les échéances restent des cibles, et tout écart est tracé.
- **Conséquences :** risque de retard (R5) réévalué ; le critère de réussite n° 2 est constaté au terme de 5 jours consécutifs de mise à jour automatique, comptés à partir de la première mise à jour automatique réussie (jour inclus) — précision du chef de projet du 2026-10-02, la mise en ligne s'étant faite par une publication manuelle et la première exécution planifiée n'ayant pas eu lieu ; les jours sont comptés en heure de Paris, l'heure affichée sur la page (précision du 2026-10-06) ; si ce constat intervient après l'échéance cible de J4, le bilan est complété à cette date. L'avancement est suivi au quotidien et tout écart (avance ou retard) est tracé.

## D14 — Outillage de développement

- **Date :** 2026-09-30
- **Contexte :** le code doit être vérifié automatiquement à chaque pull request (CdC §6) et installable de façon reproductible.
- **Options envisagées (qualité du code) :**
  1. ruff — un seul outil rapide pour l'analyse et le formatage, exécuté dans l'intégration continue.
  2. Aucun outil de style — plus simple, mais style et erreurs courantes non contrôlés.
- **Options envisagées (environnement) :**
  1. pip + venv — outils standard de Python, rien à installer en plus ; dépendances déclarées dans `pyproject.toml`.
  2. uv — plus rapide, versions figées, mais un outil supplémentaire à installer.
- **Décision :** ruff ; pip + venv.
- **Justification :** contrôle automatique de la qualité à coût nul, et installation reproductible avec les outils standard.
- **Précision (2026-10-06, #39) :** règles ruff de nommage (`N`) et de complexité (`C90`, au plus 10) activées ; couverture des tests mesurée avec `coverage` (outil de référence, sans extension pytest), la CI échoue sous 85 %.

## D15 — Dates publiées sans fuseau horaire

- **Date :** 2026-09-30
- **Contexte :** certains flux donnent l'heure de publication sans fuseau horaire (cas réel : Le Monde Informatique, heure de Paris). Lue comme de l'heure UTC, elle décale les articles de 1 à 2 heures, ce qui fausse le tri et la fenêtre de 7 jours. Défaut relevé par la revue de code de fin de J1.
- **Options envisagées :**
  1. Fuseau déclaré par source — champ facultatif `timezone` dans `config/sources.yaml`, UTC par défaut ; ajustable par la configuration seule (O5).
  2. Fuseau déduit de la langue (Paris pour les sources françaises) — plus simple, mais hypothèse fragile.
- **Décision :** option 1 ; Le Monde Informatique est déclaré en `Europe/Paris`.
- **Justification :** règle explicite, vérifiable et modifiable sans code ; une date qui porte son propre fuseau n'est jamais modifiée.

## D16 — Règles de regroupement des doublons

- **Date :** 2026-10-01
- **Contexte :** la recette du regroupement (issue #8) a montré deux effets indésirables du seul seuil de similarité de 90 % : des annonces différentes dont le titre ne diffère que d'un numéro de version (« GPT-5 » / « GPT-6 », similarité 0,98) étaient fusionnées, et des articles de plus en plus éloignés pouvaient être regroupés en chaîne (A proche de B, B proche de C, mais A éloigné de C).
- **Options envisagées (nombres) :**
  1. Titres dont les nombres diffèrent (versions, montants, années) jamais regroupés — règle simple et testable, adaptée à l'actualité IA.
  2. Seuil de similarité seul — une annonce peut disparaître de la page, fusionnée avec une autre.
- **Options envisagées (rattachement) :**
  1. Le titre de chaque article est comparé à celui de l'article retenu de chaque histoire (similaire à 90 % ou plus) — pas de chaînage ; un lien déjà présent dans une histoire la rejoint toujours, en priorité sur la comparaison des titres (même lien = même actualité).
  2. Regroupement en chaîne — une histoire peut absorber des articles de plus en plus éloignés.
- **Décision :** option 1 dans les deux cas. Un même lien publié par une autre source apparaît dans « Aussi couvert par » ; chaque autre source n'y figure qu'une fois, et une source n'est jamais listée sous son propre article.
- **Justification :** éviter qu'une actualité distincte disparaisse de la page ; règles explicites, vérifiables par des tests.

## D17 — Garde sur les mots pour le regroupement

- **Date :** 2026-10-01
- **Contexte :** la revue de code de fin de J2 a montré que le seuil de 90 %, calculé lettre par lettre, regroupe encore des titres longs qui ne diffèrent que par un mot (« amende à Google » / « amende à Meta » : 0,94 ; « lance » / « ne lance pas » : 0,90). La seconde actualité disparaîtrait de la page, ce que D16 vise à éviter.
- **Options envisagées :**
  1. Garde sur les mots — en plus du seuil, aucun mot d'au moins 3 lettres ne doit apparaître dans un seul des deux titres. Les doublons qui ne diffèrent que par la ponctuation ou de petits mots restent regroupés.
  2. Similarité calculée sur les mots plutôt que sur les lettres — efficace sur les titres courts, moins sur les titres très longs.
  3. Accepter le risque — cas rare, mais perte silencieuse.
- **Décision :** option 1.
- **Justification :** aucune actualité distincte ne doit disparaître ; un doublon reformulé d'un mot n'est plus regroupé, ce qui est préférable à une perte d'information (lié à R12).

## D18 — Extraits manquants

- **Date :** 2026-10-03
- **Contexte :** le flux de Hugging Face (S1) ne fournit aucun texte, et quelques entrées d'OpenAI (S2) non plus : ces articles s'affichaient sans extrait (issue #27). La description que les pages de Hugging Face publient pour les réseaux sociaux est générique (« A Blog post by … on Hugging Face », ou le slogan du site) : mesurée le 2026-10-03 sur les 6 articles concernés, elle n'apporte rien au lecteur.
- **Options envisagées :**
  1. Extraire le texte principal de la page de l'article avec une bibliothèque reconnue (`trafilatura`, licence Apache 2.0) et en garder le début comme extrait — essai du 2026-10-03 : 6 articles sur 6 complétés par le début de leur texte (pour l'un d'eux, la bibliothèque saute le premier paragraphe et l'extrait commence au deuxième), 0,3 à 0,5 s par page.
  2. Utiliser la description de partage de la page, en écartant les descriptions génériques — sans dépendance, mais rien de visible pour les sources actuelles.
  3. Ne rien faire et laisser le résumé au modèle de langage étudié en J4 (#15).
- **Décision :** option 1.
- **Justification :** gain immédiat et visible pour la source la plus touchée, avec une bibliothèque maintenue plutôt qu'une extraction propre à chaque site. Le texte est traité comme un extrait de flux : titre répété retiré, nettoyé, limité à environ 300 caractères (R6), affiché échappé (R13), et utilisé pour le classement par thème. Le site de Hugging Face autorise la lecture de ses pages par les robots (`robots.txt` : « Allow: / »).
- **Conséquences :** nouvelle dépendance ; une requête par article retenu sans extrait (6 par exécution le 2026-10-03, environ 2 s, soit environ 18 par jour avec les trois lancements de §4.4) ; une page inaccessible ou sans texte laisse l'article sans extrait et n'arrête pas la mise à jour (CdC §6) ; seule exception au « scraping » exclu du périmètre (CdC §5). Le site d'OpenAI refuse les requêtes automatiques : ses rares articles sans extrait le resteront. L'extraction n'est pas parfaite : il arrive que le premier paragraphe soit sauté.
- **Précision (2026-10-07, #45) :** seules les pages du site de la source (même domaine ou sous-domaine) sont lues, sans suivre de redirection vers un autre site ou hors http/https ; aucune nouvelle page n'est lue au-delà de 120 secondes par exécution ; contrairement à la justification initiale, le texte extrait n'est plus nettoyé une seconde fois (balises citées et entités conservées).

## D19 — Modèle de langage (LLM)

- **Date :** 2026-10-03
- **Contexte :** D4 (classement), le cahier des charges §5 (résumé, traduction) et D10 (doublons de même sujet) prévoyaient d'étudier en J4 un modèle de langage (issue #15 ; étude publiée en commentaire de l'issue). Mesures du 2026-10-03 : 76 % des actualités classées par mots-clés (critère de réussite ≥ 70 % tenu), 18 sur 75 en « Autres » ; environ deux tiers des articles en anglais ; aucun doublon de même sujet regroupé (R12).
- **Options envisagées :**
  1. LLM pour le classement et un résumé en français d'une phrase — gain attendu : classement selon le sens (moins d'actualités en « Autres », moins d'erreurs), page lisible en français ; coût estimé par mois (environ 75 actualités par exécution, trois exécutions par jour) : Claude Haiku 4.5 ≈ 2,5 $, Claude Sonnet 5.5 ≈ 5 $, Mistral Small ≈ 0,4 $, GPT-5 mini ≈ 0,9 $ (prix hors Claude indicatifs) ; clé API à créer et à protéger (R7) ; sorties non déterministes. La détection des doublons de même sujet (R12) serait possible mais plus délicate à fiabiliser.
  2. Essai comparatif de deux modèles avant de décider — décision mieux étayée, pour quelques centimes, mais suppose de créer la clé API dès maintenant.
  3. Pas de LLM pour l'instant — classement par mots-clés conservé ; le découpage des thèmes est étudié par ailleurs (#26).
- **Décision :** option 3.
- **Justification :** la V1 tient son critère de classement (≥ 70 %, critère n° 5) sans LLM ; le projet reste gratuit, déterministe et sans secret à gérer ; le découpage des thèmes, étudié dans #26, pourrait améliorer la lecture par simple configuration.
- **Conséquences :** pas de résumé ni de traduction en français ; les doublons de même sujet restent non regroupés (R12, limite acceptée) ; R7 devient sans objet ; la piste pourra être rouverte après le bilan, par une nouvelle décision.

## D20 — Découpage des thèmes

- **Date :** 2026-10-07
- **Contexte :** le thème « Modèles & recherche » regroupait près de la moitié des actualités et servait de fourre-tout : des mots très fréquents (« model », « agent », « GPT », « Claude ») y attiraient des articles d'autres thèmes (issue #26). D19 écartant le modèle de langage, l'amélioration passe par la configuration (O5).
- **Options envisagées :**
  1. Découper « Modèles & recherche » en trois thèmes : Modèles, Agents, Recherche & évaluation — mesuré sur trois jours de vrais flux (2026-10-03, 06 et 07) : 3 à 4 points de classement en plus (76 → 80 %, 77 → 81 %, 81 → 84 %), thème le plus gros divisé par 1,7 à 2 (29 → 14, 29 → 14, 33 → 19), « Autres » réduit (18 → 15, 17 → 14, 14 → 12).
  2. Garder les quatre thèmes — rien à changer, mais un thème trop gros pour être parcouru facilement.
- **Décision :** option 1.
- **Justification :** gain stable sur trois mesures, par simple configuration ; tous les mots-clés de l'ancien thème sont conservés dans les trois nouveaux, complétés par 24 mots-clés propres à ces thèmes (ceux du brouillon mesuré). À égalité de mots-clés, le premier thème du fichier l'emporte : un article contenant « safety cases » va ainsi en Recherche & évaluation plutôt qu'en Régulation & éthique.
- **Conséquences :** six thèmes sur la page (les six couleurs prévues par le gabarit sont toutes utilisées) ; les erreurs propres aux mots-clés demeurent (R2) ; les liens vers les sections et les couleurs des thèmes suivants changent, car elles suivent la position dans la configuration (`#theme-1` désigne désormais « Modèles ») ; captures du README refaites.
