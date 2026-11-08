---
name: audit-web-360
description: Orchestre les trois Skills GitHub de kferrandonFulbert (audit-seo-qualite-web, audit-juridique-rgpd, audit-cybersecurite-web) pour auditer un site et consolider les constats dans un rapport JSON, Markdown et HTML.
---
# Audit Web 360° — orchestrateur des Skills GitHub

## Dépendances exactes (obligatoires)
Lire `references/skills-github.md` avant chaque audit. Les trois Skills à rechercher, charger et invoquer sont :
1. **SEO** : `audit-seo-qualite-web` — https://github.com/kferrandonFulbert/skill-audit-seo — `SKILL.md` à la racine.
2. **Juridique** : `audit-juridique-rgpd` — https://github.com/kferrandonFulbert/skill-audit-juridique-web — `SKILL.md` à la racine.
3. **Cyber** : `audit-cybersecurite-web` — https://github.com/kferrandonFulbert/skill-audit-cyber — `SKILL.md` à la racine.

**Important :** le nom d'un dépôt GitHub n'est pas le nom du Skill. Ne pas substituer un Skill générique ou un scan improvisé aux trois dépendances nommées. Le simple fait de connaître l'URL GitHub n'installe ni n'active un Skill.

## Déclenchement
Pour toute demande d'audit web 360°, audit complet SEO + juridique + cyber ou rapport consolidé de ces trois domaines.

## Workflow
1. Définir la cible (URL ou projet local), le périmètre, le contexte métier et les autorisations. Auditer en lecture seule par défaut.
2. Découvrir les Skills installés par leur **nom exact** dans l'environnement agent ; lire leurs `SKILL.md` et références pertinentes. S'ils sont absents, proposer l'installation depuis les dépôts exacts. Ne jamais exécuter du code distant non inspecté ou supposer qu'un dépôt est déjà installé.
3. Exécuter séparément `audit-seo-qualite-web`, `audit-juridique-rgpd`, `audit-cybersecurite-web` en respectant leurs propres procédures et limites. Si l'environnement ne permet pas l'invocation de Skills, n'utiliser que leurs scripts locaux effectivement présents et préalablement examinés, sans les présenter comme un audit complet du Skill.
4. Le cyber commence par l'observation passive ; aucune exploitation, scan agressif, brute force, tests de modification ou soumission de formulaires sans autorisation explicite et périmètre défini. Ne pas franchir les frontières d'hôtes autorisés.
5. Chaque module fournit ses résultats natifs, sources, preuves, version/commit, contrôles non réalisés et limites. Adapter au contrat `schemas/audit-result.schema.json` sans inventer de score, couverture ou observation. Le Skill cyber n'exige pas de note globale ; conserver `score=null` si non fourni.
6. Déposer `seo.json`, `juridique.json`, `cybersecurite.json` dans le dossier d'entrée. Pour tout module non exécuté, utiliser `status=non_execute` et expliquer pourquoi. Pour une exécution incomplète, utiliser `status=partiel`.
7. Consolider avec `python scripts/consolidate.py --input-dir resultats --out-dir rapports --target https://exemple.fr` ; générer `rapport-360.json`, `rapport-360.md`, `rapport-360.html`.
8. Vérifier la traçabilité des constats et dédoublonner uniquement les anomalies véritablement équivalentes, sans supprimer leur provenance. Classer les actions P0–P3, indiquer responsables suggérés, preuves et retests.
9. Livrer un rapport clair avec périmètre, versions des Skills, couverture par module, résultats, limites, points à vérifier humainement et plan d'action. Ne jamais certifier conformité RGPD ni absence de vulnérabilités.

## Notation
Ne calculer un score de domaine que s'il est fourni et documenté par le module. Pondération indicative SEO 35 %, juridique 35 %, cyber 30 % ; calcul global uniquement si trois scores valides et couverture >= 50 % par module. Sinon indiquer « note globale indisponible ». Un audit partiel ne vaut ni zéro ni cent.

## Exécution locale
`scripts/run.py` exécute uniquement les commandes explicitement inscrites dans un manifeste local validé, avec `--execute`. Aucun script des dépôts n'est lancé automatiquement sur la seule base d'une URL GitHub. Consulter `README.md` et `references/skills-github.md`.
