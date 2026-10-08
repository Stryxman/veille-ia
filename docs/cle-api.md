# Clé de l'API du modèle de langage — procédure

> **Statut :** en revue (pull request #48)
> **Références :** [D21](decisions.md#d21--synthèse-par-thème-modèle-de-langage), [R7](risques.md), `config/synthesis.yaml`

La synthèse par thème (D21) appelle l'API gratuite de Mistral. La clé de cette API est le seul secret du projet. Elle n'est **jamais** écrite dans le code, la configuration, une issue, une pull request ou une conversation.

## Où la clé est lisible

| Endroit | Accès à la clé |
|---|---|
| Secret `LLM_API_KEY` de l'environnement GitHub `synthese` | Stockage chiffré par GitHub ; valeur illisible, même pour le propriétaire du dépôt |
| Workflow de publication, étape « Build the page », sur la branche `main` | Oui, et seulement cette étape (variable `LLM_API_KEY`) |
| Autres étapes et autres jobs, intégration continue (`ci.yml`) | Non |
| Pull requests, forks, autres branches | Non : l'environnement `synthese` n'accepte que `main` |
| Journal d'exécution | Non : le code n'écrit jamais la clé et GitHub masque sa valeur (`***`) |

Le compte Mistral est **gratuit, sans moyen de paiement** : une clé divulguée ne peut rien coûter ; au pire, un tiers épuise le quota gratuit et la page sort sans synthèse.

## Créer ou remplacer la clé

1. Dans la console Mistral (compte gratuit, sans moyen de paiement), créer une clé dédiée à ce projet.
2. L'enregistrer dans GitHub, en saisie masquée :

   ```bash
   gh secret set LLM_API_KEY --env synthese --repo Stryxman/veille-ia
   ```

3. Lancer le workflow de publication (« Run workflow » sur `main`) et vérifier la ligne `Summaries: k of n` dans le bilan d'exécution.
4. En cas de remplacement, révoquer l'ancienne clé dans la console Mistral.

**Rotation :** tous les 90 jours.

## En cas de doute (clé affichée, copiée ou divulguée)

1. Révoquer immédiatement la clé dans la console Mistral.
2. Soit enregistrer une nouvelle clé (étapes ci-dessus), soit supprimer le secret :

   ```bash
   gh secret delete LLM_API_KEY --env synthese --repo Stryxman/veille-ia
   ```

   Sans clé, la page continue d'être publiée, sans synthèse.

## Désactiver la synthèse

Mettre `enabled: false` dans `config/synthesis.yaml` : aucun appel n'est fait et la page redevient celle de la V1.
