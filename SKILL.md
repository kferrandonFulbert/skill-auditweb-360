---
name: audit-web-360
description: Orchestre un audit SEO, un audit juridique RGPD et un audit de cybersécurité autorisé, normalise les résultats et produit un rapport consolidé JSON, Markdown et HTML avec couverture, preuves et plan d'action.
---
# Audit Web 360°

## Déclenchement
Quand l'utilisateur demande un audit global d'un site, ou souhaite lancer SEO + juridique/RGPD + cybersécurité dans un même rapport.

## Procédure impérative
1. Définir la cible exacte, le périmètre (URL publique ou projet local), le propriétaire et l'autorisation. Pour la cybersécurité, limiter par défaut aux contrôles passifs et non intrusifs. Aucun scan agressif, brute force, exploitation, contournement ou formulaire envoyé sans autorisation explicite et périmètre documenté.
2. Rechercher les Skills `audit-seo`, `audit-juridique-rgpd`, `audit-cybersecurite` dans l'environnement réellement disponible. Les noms sont indicatifs : identifier les capacités et lire leurs instructions. Ne pas prétendre pouvoir invoquer un Skill inaccessible.
3. Pour chaque domaine, exécuter le Skill ou son outil/script documenté si accessible et autorisé. Ne pas inventer les observations. Si un domaine ne peut être exécuté, inscrire `non_execute` avec raison et actions nécessaires.
4. Enregistrer chaque résultat dans un fichier JSON conforme à `schemas/audit-result.schema.json`. Si le Skill émet un autre format, le convertir avec traçabilité ; ne pas transformer une absence de preuve en succès.
5. En option, utiliser `scripts/run.py` avec un manifeste de commandes locales explicitement approuvées. Il ne découvre ni n'exécute automatiquement des scripts arbitraires. L'exécution est désactivée par défaut (`--execute` requis).
6. Consolider avec `python scripts/consolidate.py --input-dir <dossier> --out-dir <dossier> --target <URL>`. Générer JSON, Markdown et HTML. Examiner la couverture et les alertes avant de restituer.
7. Prioriser les anomalies par gravité, preuve et effort estimé. Dédupliquer seulement les constats véritablement équivalents en conservant leur provenance ; les rapprochements interdomaines sont des suggestions, pas des suppressions automatiques.
8. Citer les sources officielles vérifiées et leurs dates, en particulier pour les obligations juridiques. Distinguer loi, recommandation et bonne pratique. Ne pas certifier la conformité juridique ou la sécurité absolue.

## Entrées
- URL HTTPS ou chemin local autorisé ; contexte du site et type d'activité ; date ; périmètre ; permissions ; trois JSON d'audit normalisés.
- Format : un fichier par domaine (`seo.json`, `juridique.json`, `cybersecurite.json`). Voir `examples/`.

## Sorties
- `rapport-360.json` : machine-readable, scores et couverture.
- `rapport-360.md` et `rapport-360.html` : synthèse, état des trois modules, constats avec preuves, plan d'action et contrôles manuels.
- Si tous les audits n'ont pas été réalisés, afficher explicitement « audit partiel ».

## Notation
- Score indicatif par domaine seulement si `status=execute`, si un `score` de 0 à 100 est fourni et si `coverage` est documentée. Les notes des modules ne doivent pas être inventées à partir du nombre d'anomalies.
- Score global pondéré par défaut : SEO 35 %, juridique 35 %, cybersécurité 30 %. Ne le calculer que si les trois modules ont une note et une couverture >= 0,5 ; afficher le seuil et les poids. Une note n'est jamais une certification.
- Le statut `non_execute` ou `partiel` n'est jamais assimilé à un score zéro ou cent.

## Limites
- L'orchestrateur n'est pas lui-même un moteur de scan SEO, juridique ou cyber. Il pilote les outils réellement disponibles et consolide les preuves.
- Le Skill cybersécurité est un prérequis distinct : s'il manque, le signaler et fournir la liste des contrôles passifs envisageables sans inventer de résultats.
- Lire `references/controls.md` pour les garde-fous et `schemas/audit-result.schema.json` pour le contrat d'interface.
