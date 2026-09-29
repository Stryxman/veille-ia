# Journal de décisions

> Chaque choix structurant du projet est consigné ici : contexte, options envisagées, décision et justification.
> **Décideur :** Richard (chef de projet). Les options sont préparées avec l'assistance de Claude Code.

| ID | Date | Sujet | Décision |
|---|---|---|---|
| D1 | 2026-09-29 | Mode de restitution | Page web statique (GitHub Pages) |
| D2 | 2026-09-29 | Stack technique | Python |
| D3 | 2026-09-29 | Exécution et hébergement | GitHub Actions planifié + GitHub Pages |
| D4 | 2026-09-29 | Méthode de classement | Mots-clés en V1, LLM en J4 |
| D5 | 2026-09-29 | Sources et fréquence | ~6 flux RSS FR + EN, mise à jour quotidienne |
| D6 | 2026-09-29 | Langue du projet | Docs et page en français, code en anglais |
| D7 | 2026-09-29 | Nom et visibilité du repo | `veille-ia`, public dès J0 |
| D8 | 2026-09-29 | Méthode de suivi | Kanban + jalons |
| D9 | 2026-09-29 | Documentation en anglais | `README.en.md` seul, rédigé en J4 ; docs de pilotage en français |
| D10 | 2026-09-29 | Article retenu parmi des doublons | Niveau de confiance par source, puis antériorité ; doublons en « Aussi couvert par » |
| D11 | 2026-09-29 | Articles sans date de publication | Conservés, datés de leur date de collecte, étiquette « Date de publication inconnue » |

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
- **Limite connue :** en V1, seuls les titres quasi identiques sont reconnus comme doublons ; la détection de « même sujet, titres différents » relève d'une analyse sémantique, à étudier avec le LLM en J4.

## D11 — Articles sans date de publication

- **Date :** 2026-09-29
- **Contexte :** certains flux publient des articles sans date. Il faut décider s'ils sont affichés et comment les situer dans le temps.
- **Options envisagées :**
  1. Exclure les articles sans date — simple, mais perte d'informations potentiellement récentes.
  2. Les conserver en les datant de leur date de collecte, sans le signaler — aucune perte, mais date affichée potentiellement trompeuse.
  3. Les conserver en les datant de leur date de collecte et en le signalant par une étiquette — aucune perte, et le lecteur sait que la date est approximative.
- **Décision :** option 3. La date de collecte sert au tri et à la fenêtre de 7 jours ; la page affiche l'étiquette « Date de publication inconnue ».
- **Justification :** ne perdre aucune information tout en restant transparent sur la fiabilité de la date affichée.
