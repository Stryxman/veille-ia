# Cahier des charges — Veille IA

> **Statut :** v1.16 — validé par le chef de projet le 2026-10-06
> **Chef de projet :** Richard
> **Date :** 2026-09-29
> **Décisions associées :** voir [decisions.md](decisions.md) (D1 à D19)
> **Risques associés :** voir [risques.md](risques.md)
> **Sources :** voir [sources.md](sources.md)

### Historique des versions

| Version | Date | Modifications |
|---|---|---|
| v0.1 | 2026-09-29 | Première rédaction |
| v0.2 | 2026-09-29 | O5 remplacé par un objectif d'évolutivité ; sources détaillées dans `sources.md` ; ajout du README anglais (D9) |
| v0.3 | 2026-09-29 | Articles sans date signalés (D11) ; dédoublonnage selon le niveau de confiance des sources, doublons affichés en « Aussi couvert par » (D10) ; README anglais reporté en J4 |
| v1.0 | 2026-09-29 | Organisation qualité ajoutée (§8, D12) ; validation par le chef de projet |
| v1.1 | 2026-09-29 | Replanification : mise en ligne de la V1 avancée au 2026-10-02 (D13) ; validée le 2026-09-30 |
| v1.2 | 2026-09-30 | Vocabulaire du traitement (§4.2) et du planning (§8) aligné sur D10 (« regroupement des doublons ») |
| v1.3 | 2026-09-30 | Outillage : ruff, pip + venv (D14) ; validée le 2026-09-30 (pull request #16) |
| v1.4 | 2026-09-30 | §4.1 : entrées sans titre ou sans lien ignorées et signalées dans le journal d'exécution ; §6 : taille maximale d'un flux (10 Mio) ; validée le 2026-09-30 (pull request #17) |
| v1.5 | 2026-09-30 | §4.1 : dates sans fuseau horaire (D15) ; §6 : flux vide, tronqué ou sans entrée exploitable traité comme indisponible ; validée le 2026-09-30 (pull request #20) |
| v1.6 | 2026-10-01 | §4.2 : règles de regroupement des doublons (D16) ; validée le 2026-10-01 (pull request #22) |
| v1.7 | 2026-10-01 | §4.2 : garde sur les mots pour le regroupement (D17) ; validée le 2026-10-01 (pull request #25) |
| v1.8 | 2026-10-01 | §4.1 et §4.3 : extrait affiché seulement si le flux en fournit un (voir sources.md) ; §4.1 : lien relatif complété avec l'adresse du flux, entrée ignorée si son lien n'est pas une adresse web ; validée le 2026-10-01 (pull request #28) |
| v1.9 | 2026-10-01 | §4.4 : horaire de la mise à jour quotidienne ; validée le 2026-10-02 (pull request #29) |
| v1.10 | 2026-10-02 | §4.1 : lien sans nom de site ignoré ; §4.4 : lancement décalé de l'heure pile ; §6 : aucun article des 7 derniers jours traité comme aucune source ; validée le 2026-10-02 (pull request #32) |
| v1.11 | 2026-10-02 | §8 : critère n° 2 compté à partir de la première mise à jour automatique réussie (précision de D13) ; validée le 2026-10-02 (pull request #33) |
| v1.12 | 2026-10-03 | §4.4 : trois lancements planifiés par jour ; validée le 2026-10-03 (pull request #35) |
| v1.13 | 2026-10-03 | §4.1, §4.2, §4.3 : extrait manquant complété par le début du texte de la page de l'article (D18) ; §4.4 : étape d'extraits manquants ; §5 : exception au « scraping » exclu ; §6 : page d'article illisible sans effet sur la mise à jour, quatre modules ; §7 : étape `enrich`, bibliothèque `trafilatura` ; validée le 2026-10-03 (pull request #36) |
| v1.14 | 2026-10-03 | §4.2, §5, §8 : LLM étudié et non retenu pour l'instant (D19) ; validée le 2026-10-03 (pull request #37) |
| v1.15 | 2026-10-03 | §8 : contenu de J4 aligné sur le jalon (extraits manquants, découpage des thèmes) ; validée le 2026-10-06 (pull request #38) |
| v1.16 | 2026-10-06 | §4.4 : aucune heure de mise à jour promise (retards constatés) ; §8 : jours du critère n° 2 comptés en heure de Paris (précision de D13) ; validée le 2026-10-06 (pull request #40) |

---

## 1. Contexte

L'actualité de l'intelligence artificielle est abondante, dispersée entre de nombreuses sources (blogs d'éditeurs, presse tech, médias français et anglophones) et très redondante : une même annonce est reprise par plusieurs sites le même jour. Suivre ce flux demande un temps important et produit beaucoup de doublons.

Ce projet vise à automatiser cette veille : collecter l'actualité IA depuis quelques sources choisies, la dédoublonner, la classer par thème et la restituer sous forme d'une page web unique, mise à jour chaque jour.

La solution doit rester simple, gratuite et fonctionner sans intervention, afin de pouvoir être maintenue par une seule personne.

## 2. Objectifs

| # | Objectif | Indicateur |
|---|---|---|
| O1 | Donner en un coup d'œil l'actualité IA de la semaine | Une page unique, articles groupés par thème |
| O2 | Réduire le bruit | Doublons entre sources regroupés : chaque information n'apparaît qu'une fois |
| O3 | Fonctionner sans intervention | Mise à jour quotidienne automatique, sans action manuelle |
| O4 | Coût nul | 0 € d'hébergement et d'exécution en V1 |
| O5 | Faire évoluer la veille sans développement | Ajout ou retrait d'une source ou d'un thème par simple modification de la configuration, sans toucher au code |

## 3. Utilisateurs cibles

- **Lecteur :** une personne ou une petite équipe qui souhaite suivre l'actualité IA sans y passer plus de 5 minutes par jour, depuis un navigateur, sans rien installer.
- **Mainteneur :** la personne qui ajuste les sources et les thèmes de la veille ; elle modifie des fichiers de configuration, pas le code.

## 4. Périmètre V1

### 4.1 Collecte
- Lecture automatique de **6 flux RSS** (4 anglophones, 2 francophones) : Hugging Face Blog, OpenAI News, TechCrunch (IA), The Verge (IA), ActuIA, Le Monde Informatique (IA).
- Le détail de chaque source (site, flux, langue, type, niveau de confiance, raison du choix) et la date de dernière vérification des flux sont documentés dans [sources.md](sources.md).
- La liste des sources est définie dans un fichier de configuration (`config/sources.yaml`) : ajouter ou retirer une source ne nécessite pas de modifier le code.
- Pour chaque article, on conserve : titre, lien, source, date de publication (si disponible), extrait, langue. Un article retenu (7 derniers jours) dont le flux ne fournit pas d'extrait reçoit, si sa page peut être lue, le début de son texte principal, sans le titre répété (D18). Un article sans date de publication n'est pas rejeté. Une date publiée sans fuseau horaire est lue dans le fuseau déclaré pour la source (UTC par défaut, D15).
- Une entrée de flux sans titre ou sans lien est ignorée, car elle ne peut ni être affichée ni renvoyer à l'article d'origine ; un lien relatif (par exemple `/blog/article`) est complété avec l'adresse du flux ; une entrée dont le lien, une fois complété, n'est pas une adresse web (`http` ou `https`, avec un nom de site) est ignorée, car un tel lien pourrait exécuter du code sur la page (par exemple un lien `javascript:`) ; le nombre d'entrées ignorées par source est signalé dans le journal d'exécution.

### 4.2 Traitement
- **Nettoyage :** suppression du HTML et des espaces superflus dans les titres et extraits ; extrait tronqué à environ 300 caractères, qu'il vienne du flux ou de la page de l'article (D18). L'extrait complété est pris en compte pour le classement par thème.
- **Fenêtre temporelle :** seuls les articles des **7 derniers jours** sont conservés.
- **Article sans date de publication :** il est conservé et daté de sa date de collecte, qui sert au tri et à la fenêtre temporelle ; il est signalé sur la page par l'étiquette « Date de publication inconnue ».
- **Regroupement des doublons :** deux articles sont considérés comme doublons s'ils ont le même lien, ou des titres très similaires. L'article retenu est celui de la source au **meilleur niveau de confiance** ; à niveau égal, le plus ancien. Les autres sont rattachés à l'article retenu. Le titre d'un article est comparé à celui de l'article retenu de chaque histoire (pas de regroupement en chaîne) ; un lien déjà présent dans une histoire la rejoint toujours, en priorité sur la comparaison des titres ; chaque autre source n'apparaît qu'une fois dans « Aussi couvert par », jamais sous son propre article ; deux titres dont les nombres diffèrent (versions, montants, années) ne sont jamais regroupés (D16), ni deux titres dont un mot d'au moins 3 lettres n'apparaît que dans l'un des deux (D17).
- **Niveaux de confiance des sources** (définis dans `config/sources.yaml`, justifiés dans [sources.md](sources.md)) :
  1. Source primaire (l'éditeur qui fait l'annonce)
  2. Presse spécialisée IA ou tech
  3. Presse généraliste ou hors tech
- **Limite V1 :** seuls les titres quasi identiques sont reconnus comme doublons ; deux articles traitant du même sujet avec des titres différents ne le sont pas (piste d'amélioration par LLM écartée pour l'instant, D19).
- **Classement par thème** par mots-clés, définis dans `config/themes.yaml`. Thèmes initiaux :
  1. Modèles & recherche
  2. Produits & outils
  3. Business & financement
  4. Régulation & éthique
  5. Autres (articles non classés)

### 4.3 Restitution
- Une **page web statique unique**, en français, publiée sur GitHub Pages.
- Articles groupés par thème, triés du plus récent au plus ancien.
- Chaque article affiche : titre (lien vers la source originale), source, date, extrait (s'il n'a pu être obtenu ni du flux ni de la page de l'article, l'article s'affiche sans extrait ; voir [sources.md](sources.md)).
- Un article sans date de publication affiche sa date de collecte et l'étiquette « Date de publication inconnue ».
- Sous un article qui a des doublons : mention « Aussi couvert par : » suivie des autres sources, avec leurs liens.
- En tête de page : date et heure de la dernière mise à jour, nombre d'articles.
- En pied de page : liste des sources et signalement des sources indisponibles lors de la dernière exécution.
- Lisible sur mobile.

### 4.4 Automatisation
- Exécution **quotidienne** planifiée via GitHub Actions : collecte → traitement → extraits manquants (D18) → génération → publication. Trois lancements planifiés par jour (04:17, 10:17 et 16:17 UTC), en dehors de l'heure pile : GitHub ne garantit ni l'heure ni l'exécution des lancements planifiés (retards de 3 à 9 heures constatés du 3 au 5 octobre 2026, en UTC), et un seul lancement réussi suffit à mettre la page à jour dans la journée. Aucune heure de mise à jour n'est donc promise.
- Déclenchement manuel possible (bouton « Run workflow »).

## 5. Hors périmètre V1

Les éléments suivants sont **exclus de la V1**. Certains sont candidats pour le jalon J4 (bonus), sur décision du chef de projet :

| Élément | Statut |
|---|---|
| Classement et résumé par modèle de langage (LLM) | Étudié en J4, non retenu pour l'instant (D19) |
| Envoi du résumé par email | Candidat J4 |
| Archives / historique des éditions précédentes | Candidat J4 |
| Traduction des articles anglophones | Non retenu pour l'instant (supposait un LLM, D19) |
| Sources non-RSS (API, réseaux sociaux, scraping de sites comme source d'articles) | Exclu ; seule exception : lecture de la page d'un article déjà collecté pour compléter son extrait manquant (D18) |
| Comptes utilisateurs, personnalisation, abonnements | Exclu |
| Base de données | Exclu |
| Serveur ou hébergement payant | Exclu |

## 6. Exigences non fonctionnelles

- **Robustesse :** l'indisponibilité d'une source n'empêche pas la génération de la page. Si **aucune** source ne répond, ou si aucun article ne date des 7 derniers jours, la page précédente reste en ligne et l'exécution est signalée en échec. Un flux de plus de 10 Mio (téléchargé ou décompressé), vide, tronqué ou sans aucune entrée exploitable est traité comme une source indisponible. Une page d'article illisible (inaccessible, refusée, sans texte) laisse l'article sans extrait et n'empêche pas la génération de la page (D18).
- **Coût :** 0 € (repo public, GitHub Actions et GitHub Pages gratuits).
- **Maintenabilité :** code Python découpé en quatre modules indépendants (`collect`, `process`, `enrich`, `render`), testés.
- **Qualité :** tests automatisés (pytest) et contrôle de la qualité du code (ruff) exécutés à chaque pull request ; les tests n'appellent pas le réseau.
- **Respect des sources :** seuls le titre, un court extrait et le lien vers l'article original sont affichés.
- **Évolutivité :** sources et thèmes définis uniquement dans `config/sources.yaml` et `config/themes.yaml`.
- **Langue :** documentation et page en français ; code, noms techniques et messages de commit en anglais. Un README en anglais (`README.en.md`) présente le projet aux lecteurs non francophones ; il est rédigé en J4, une fois le README français stabilisé.

## 7. Solution technique (résumé)

```
config/sources.yaml ─► collect ─► process ─► enrich ─► render ─► site/index.html ─► GitHub Pages
config/themes.yaml ─────────────────┘   (enrich : extraits manquants, D18)
```

- **Langage :** Python ≥ 3.12 (bibliothèques : `feedparser`, `Jinja2`, `PyYAML`, `trafilatura` ; outils : `pytest`, `ruff`).
- **Environnement :** pip + venv, dépendances déclarées dans `pyproject.toml` (D14).
- **Exécution :** workflow GitHub Actions planifié (quotidien) + workflow d'intégration continue (tests).
- **Hébergement :** GitHub Pages.
- **Stockage :** aucun ; la page est entièrement régénérée à chaque exécution.

Justification des choix : voir [decisions.md](decisions.md).

## 8. Organisation et planning

- **Méthode :** kanban (board GitHub Projects : À faire / En cours / Revue / Terminé) + jalons GitHub.
- **Backlog :** une issue GitHub par fonctionnalité, avec critères d'acceptation.
- **Qualité :** une issue n'est fermée qu'après une recette prouvant chaque critère d'acceptation ; sources et cohérence documentaire vérifiées de façon indépendante (D12).
- **Rôles :** Richard — chef de projet (décide, arbitre, valide) ; Claude Code — assistant technique et méthodologique (propose, rédige, développe).

| Jalon | Contenu | Livrable | Échéance cible |
|---|---|---|---|
| **J0 — Cadrage** | Cahier des charges, sources, décisions, risques, backlog, board | Repo public avec pilotage complet | 2026-09-29 |
| **J1 — Collecte** | Lecture des 6 flux, format d'article commun | Module `collect` testé | 2026-09-30 |
| **J2 — Traitement** | Nettoyage, fenêtre 7 jours, regroupement des doublons, classement | Module `process` testé | 2026-10-01 |
| **J3 — Restitution (V1)** | Page HTML, workflow quotidien, publication Pages | **V1 en ligne** | 2026-10-02 |
| **J4 — Finitions (bonus)** | README FR et EN avec captures, extraits manquants (D18), découpage des thèmes (#26), étude LLM (non retenue, D19), bilan de projet | V1.1 | 2026-10-06 |

> Échéances arbitrées par le chef de projet le 2026-09-29 (D13). Ce sont des cibles ; le critère de réussite n° 2 est constaté au terme de 5 jours consécutifs de mise à jour automatique, comptés en jours de l'heure de Paris à partir de la première mise à jour automatique réussie (jour inclus ; D13) ; si ce constat intervient après l'échéance cible de J4, le bilan est complété à cette date. L'avancement est suivi au quotidien et tout écart (avance ou retard) est tracé. Les écarts sont analysés dans le bilan de projet.

## 9. Critères de réussite

La V1 est considérée comme réussie lorsque **tous** les critères suivants sont remplis :

1. La page est accessible publiquement via un lien présent dans le README.
2. La page a été mise à jour automatiquement au moins 5 jours consécutifs sans intervention manuelle.
3. Les 6 sources sont collectées ; une source volontairement cassée n'empêche pas la génération de la page.
4. Aucun doublon évident (même lien ou même titre) n'apparaît comme article distinct sur la page.
5. Au moins 70 % des articles sont classés dans un thème autre que « Autres » (mesuré sur une exécution).
6. Une source ajoutée uniquement dans `config/sources.yaml` apparaît sur la page à l'exécution suivante, sans modification du code.
7. Les tests automatisés passent dans l'intégration continue.
8. Le repo contient, à jour : cahier des charges, sources, journal de décisions, registre des risques, issues avec critères d'acceptation rattachées à des jalons, board de suivi, README en français (la version anglaise est un livrable de J4).
