# Audit Web 360°

Skill orchestrateur autonome, conçu pour être utilisé avec trois modules : SEO, juridique/RGPD et cybersécurité.

## Installation
Copier le dossier `audit-web-360` dans le répertoire de Skills de l'agent utilisé. Installer séparément les Skills spécialisés. Leur disponibilité dépend de l'environnement ; le présent Skill ne les installe pas et ne garantit pas leur invocation automatique.

## Utilisation
1. Exécuter les audits spécialisés autorisés et enregistrer leurs résultats au format `schemas/audit-result.schema.json` sous `seo.json`, `juridique.json`, `cybersecurite.json` dans un dossier `resultats/`.
2. Un résultat manquant sera signalé `non_execute`. Adapter les résultats d'autres Skills à ce contrat sans inventer de scores.
3. Lancer :

```bash
python scripts/consolidate.py --input-dir resultats --out-dir rapports --target https://exemple.fr
```

4. Optionnel : déclarer les commandes exactes dans un manifeste sur le modèle `examples/manifest.example.json`, puis :

```bash
python scripts/run.py --manifest manifest.json
python scripts/run.py --manifest manifest.json --execute
```

Le runner n'effectue aucun scan sans commandes explicitement renseignées et sans `--execute`. Les commandes s'exécutent avec les permissions du processus : vérifier le manifeste et l'autorisation avant exécution.

## Important
Le domaine cyber ne comprend aucun scanner actif. Le Skill juridique déjà créé peut fournir des constats, mais son JSON doit être adapté au schéma commun. Les résultats d'exemple sont fictifs et ne doivent jamais être présentés comme un audit réel.

## Dépendances GitHub officielles de cet orchestrateur

- SEO : https://github.com/kferrandonFulbert/skill-audit-seo (`audit-seo-qualite-web`)
- Juridique : https://github.com/kferrandonFulbert/skill-audit-juridique-web (`audit-juridique-rgpd`)
- Cybersécurité : https://github.com/kferrandonFulbert/skill-audit-cyber (`audit-cybersecurite-web`)

Le fichier `references/skills-github.md` détaille l'installation et la compatibilité. L'orchestrateur recherche les **noms déclarés dans les SKILL.md**, pas les noms des dépôts. Les trois modules doivent être installés et accessibles à l'agent pour être invoqués comme Skills. Le lanceur Python ne sait pas invoquer un Skill agent à lui seul ; il peut exécuter uniquement des commandes locales configurées explicitement.
