# Veille IA

Une page web qui rassemble chaque jour l'actualité de l'intelligence artificielle, dédoublonnée et classée par thème, à partir de sources françaises et anglophones.

> **Statut :** cadrage (J0) terminé le 30 septembre 2026 ; collecte (J1) en cours. Mise en ligne de la V1 visée le 2 octobre 2026.

## Le besoin

L'actualité IA est dispersée entre de nombreux sites et très redondante : une même annonce est reprise partout le même jour. Suivre ce flux prend du temps et produit beaucoup de doublons.

## La solution (V1)

1. **Collecte** automatique de 6 flux RSS (4 anglophones, 2 francophones).
2. **Traitement** : nettoyage, conservation des 7 derniers jours, regroupement des doublons, classement par thème.
3. **Restitution** : une page web unique, mise à jour chaque jour, gratuite et sans installation.

## Développement

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest          # tests (sans accès réseau)
.venv/bin/ruff check .    # qualité du code
.venv/bin/ruff format --check .   # format du code
```

## Documentation du projet

| Document | Contenu |
|---|---|
| [Cahier des charges](docs/cahier-des-charges.md) | Contexte, objectifs, périmètre, critères de réussite |
| [Sources](docs/sources.md) | Sources suivies et raisons de leur choix |
| [Journal de décisions](docs/decisions.md) | Choix structurants, options envisagées, justifications |
| [Registre des risques](docs/risques.md) | Risques, probabilité, impact, mesures et jalon de mise en œuvre |

Le suivi d'avancement se fait via les [jalons](https://github.com/Stryxman/veille-ia/milestones) et le board du projet.
