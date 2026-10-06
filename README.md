# Veille IA

*Français · [English](README.en.md)*

Une page web qui rassemble chaque jour l'actualité de l'intelligence artificielle, dédoublonnée et classée par thème, à partir de sources françaises et anglophones.

> **Statut :** cadrage (J0) terminé le 30 septembre 2026 ; collecte (J1) terminée le 30 septembre 2026 ; traitement (J2) terminé le 1er octobre 2026 ; restitution (J3) terminée le 6 octobre 2026 (V1 en ligne le 2 octobre, mise à jour automatique depuis le 3) ; finitions (J4) en cours.

**Page en ligne :** [stryxman.github.io/veille-ia](https://stryxman.github.io/veille-ia/) — mise à jour automatique plusieurs fois par jour (trois lancements planifiés ; GitHub les exécute souvent avec plusieurs heures de retard).

| Sur ordinateur (mode clair) | Sur téléphone (mode sombre) |
|---|---|
| ![La page sur ordinateur, en mode clair : sommaire en pastilles et cartes d'articles](docs/captures/page-bureau-clair.png) | ![La page sur téléphone, en mode sombre](docs/captures/page-mobile-sombre.png) |

## Le besoin

L'actualité IA est dispersée entre de nombreux sites et très redondante : une même annonce est reprise partout le même jour. Suivre ce flux prend du temps et produit beaucoup de doublons.

## La solution

1. **Collecte** de 6 flux RSS, 4 anglophones et 2 francophones ([sources et raisons de leur choix](docs/sources.md)). Une source en panne n'arrête pas les autres.
2. **Traitement** : nettoyage du texte, conservation des 7 derniers jours, regroupement des doublons (l'article retenu vient de la source la plus fiable, les autres sont cités en « Aussi couvert par »), extrait complété depuis la page de l'article quand le flux n'en fournit pas, classement par thème à partir de mots-clés.
3. **Restitution** : une page web unique, en français, lisible sur téléphone, en mode clair ou sombre, sans compte ni installation.
4. **Publication automatique** sur GitHub Pages (trois lancements planifiés par jour) ; si aucune source ne répond, la page précédente reste en ligne.

```
config/sources.yaml ─► collect ─► process ─► enrich ─► render ─► site/index.html ─► GitHub Pages
config/themes.yaml ─────────────────┘
```

Sources et thèmes se règlent dans deux fichiers de configuration, sans toucher au code. Le projet est gratuit : dépôt public, GitHub Actions et GitHub Pages.

## La démarche

Le projet est mené en jalons courts, avec des documents de pilotage tenus à jour :

| Jalon | Contenu | Date |
|---|---|---|
| J0 — Cadrage | Cahier des charges, sources, décisions, risques | 30 septembre 2026 |
| J1 — Collecte | Lecture des flux RSS | 30 septembre 2026 |
| J2 — Traitement | Nettoyage, doublons, classement | 1er octobre 2026 |
| J3 — Restitution | Page web, publication quotidienne : V1 en ligne | 6 octobre 2026 (V1 en ligne le 2 octobre) |
| J4 — Finitions | Extraits manquants, étude d'un modèle de langage, thèmes, documentation, bilan | cible : 6 octobre 2026 |

- **Décisions tracées** : chaque choix structurant est consigné avec les options envisagées et sa justification, puis validé par le chef de projet ([journal de décisions](docs/decisions.md)).
- **Risques suivis** : probabilité, impact et mesures, revus à chaque fin de jalon ([registre des risques](docs/risques.md)).
- **Contrôle qualité** : recette de chaque fonctionnalité avant fermeture de son issue, critère par critère et preuve à l'appui, vérification indépendante des sources et contrôle de cohérence de la documentation à chaque modification ([D12](docs/decisions.md#d12--contrôle-qualité)) ; revue de code indépendante en fin de jalon ; tests automatisés et contrôle du code à chaque pull request ([cahier des charges §6](docs/cahier-des-charges.md#6-exigences-non-fonctionnelles), [D14](docs/decisions.md#d14--outillage-de-développement)).
- **Suivi** : [jalons](https://github.com/Stryxman/veille-ia/milestones), [issues](https://github.com/Stryxman/veille-ia/issues) et [tableau de suivi](https://github.com/users/Stryxman/projects/1).

## Limites connues

- Le classement par mots-clés reste approximatif : une partie des articles tombe dans « Autres » ou dans un thème voisin ([R2](docs/risques.md)). Un modèle de langage a été étudié et n'est pas retenu pour l'instant ([D19](docs/decisions.md#d19--modèle-de-langage-llm)).
- Seuls les titres quasi identiques sont reconnus comme doublons : une même nouvelle titrée différemment en français et en anglais n'est pas regroupée ([R12](docs/risques.md)).
- Certaines pages d'articles refusent la lecture automatique ; leurs articles sans extrait dans le flux restent sans extrait ([sources](docs/sources.md)).
- GitHub ne garantit pas l'heure ni même l'exécution des lancements planifiés (retards de 3 à 9 heures constatés), d'où trois créneaux par jour ([cahier des charges §4.4](docs/cahier-des-charges.md#44-automatisation), [R3](docs/risques.md)).

## Développement

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest          # tests (sans accès réseau)
.venv/bin/ruff check .    # qualité du code
.venv/bin/ruff format --check .   # format du code
.venv/bin/python -m veille.render --output site   # génère la page dans site/index.html
```

## Documentation du projet

| Document | Contenu |
|---|---|
| [Cahier des charges](docs/cahier-des-charges.md) | Contexte, objectifs, périmètre, critères de réussite, planning |
| [Sources](docs/sources.md) | Sources suivies et raisons de leur choix |
| [Journal de décisions](docs/decisions.md) | Choix structurants, options envisagées, justifications |
| [Registre des risques](docs/risques.md) | Risques, probabilité, impact, mesures et jalon de mise en œuvre |
