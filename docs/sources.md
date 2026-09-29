# Sources de la veille

> Liste des sources collectées par la veille, avec la raison de leur sélection.
> La configuration technique correspondante se trouve dans `config/sources.yaml` ; ce document et ce fichier doivent rester alignés.
> **Dernière vérification des flux :** 2026-09-29

## Critères de sélection

Une source est retenue si elle :

1. publie régulièrement sur l'intelligence artificielle (au moins plusieurs articles par semaine, ou des annonces de référence) ;
2. propose un **flux RSS public et fonctionnel** ;
3. contribue à l'équilibre de la veille : annonces d'éditeurs (source primaire) et presse (analyse, recul), en anglais et en français.

## Niveaux de confiance

Chaque source reçoit un niveau de confiance. Lorsque plusieurs sources publient la même information, l'article de la source au meilleur niveau est retenu (à niveau égal, le plus ancien) ; les autres apparaissent en « Aussi couvert par » sous l'article retenu ([D10](decisions.md#d10--choix-de-larticle-retenu-parmi-des-doublons)).

| Niveau | Catégorie | Justification |
|---|---|---|
| 1 | Source primaire | L'éditeur qui fait l'annonce : information de première main |
| 2 | Presse spécialisée IA ou tech | Journalistes du domaine, recoupement et mise en contexte |
| 3 | Presse généraliste ou hors tech | Couverture moins experte du sujet IA |

## Liste des sources (V1)

| # | Source | Langue | Type | Niveau | Site | Flux RSS | Pourquoi cette source |
|---|---|---|---|---|---|---|---|
| S1 | Hugging Face Blog | EN | Éditeur / communauté open source | 1 | [huggingface.co/blog](https://huggingface.co/blog) | [feed.xml](https://huggingface.co/blog/feed.xml) | Référence de l'IA open source : nouveaux modèles, bibliothèques et tutoriels |
| S2 | OpenAI News | EN | Éditeur | 1 | [openai.com/news](https://openai.com/news) | [rss.xml](https://openai.com/news/rss.xml) | Annonces de première main d'un acteur majeur (modèles, produits, politique) |
| S3 | TechCrunch — IA | EN | Presse tech | 2 | [techcrunch.com/…/artificial-intelligence](https://techcrunch.com/category/artificial-intelligence/) | [feed](https://techcrunch.com/category/artificial-intelligence/feed/) | Couverture business : levées de fonds, startups, acquisitions |
| S4 | The Verge — IA | EN | Presse tech grand public | 2 | [theverge.com/ai-artificial-intelligence](https://www.theverge.com/ai-artificial-intelligence) | [index.xml](https://www.theverge.com/rss/ai-artificial-intelligence/index.xml) | Produits et usages grand public, régulation |
| S5 | ActuIA | FR | Média spécialisé IA | 2 | [actuia.com](https://www.actuia.com/) | [feed](https://www.actuia.com/feed/) | Média français dédié à l'IA : recherche, écosystème français et européen |
| S6 | Le Monde Informatique — IA | FR | Presse IT professionnelle | 2 | [lemondeinformatique.fr](https://www.lemondeinformatique.fr/) | [rss.xml](https://www.lemondeinformatique.fr/flux-rss/thematique/intelligence-artificielle/rss.xml) | Angle entreprise et DSI : adoption de l'IA, offres des éditeurs, cas d'usage |

## Notes techniques

- **S1 — Hugging Face :** le blog publie aussi des billets d'autres organisations (partenaires, laboratoires) ; ce sont également des annonces de première main, d'où le niveau 1. Le flux contient tout l'historique depuis 2020 : la collecte doit filtrer par date.
- **S2 — OpenAI :** le site web bloque les requêtes automatisées (code 403), mais le flux RSS répond normalement. Le flux contient tout l'historique depuis 2015 : la collecte doit filtrer par date.
- **S4 — The Verge :** le flux ne contient que les 10 derniers articles ; une collecte quotidienne suffit à ne rien manquer.
- **S6 — Le Monde Informatique :** flux au format RSS 1.0 (RDF), encodé en ISO-8859-15 ; à couvrir par un test de collecte.

## Historique des modifications

| Date | Modification | Décision |
|---|---|---|
| 2026-09-29 | Sélection initiale des 6 sources | [D5](decisions.md#d5--sources-et-fréquence-de-mise-à-jour) |
| 2026-09-29 | Ajout des niveaux de confiance | [D10](decisions.md#d10--choix-de-larticle-retenu-parmi-des-doublons) |
| 2026-09-29 | Vérification indépendante des 6 sources (niveaux confirmés) ; notes techniques S1 et S4 ajoutées | — |
