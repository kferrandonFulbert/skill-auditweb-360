# Dépendances GitHub vérifiées le 8 novembre 2026

| Domaine | Dépôt | Nom déclaré dans SKILL.md | Mode |
|---|---|---|---|
| SEO | https://github.com/kferrandonFulbert/skill-audit-seo | `audit-seo-qualite-web` | Skill agent et scripts locaux selon documentation |
| Juridique | https://github.com/kferrandonFulbert/skill-audit-juridique-web | `audit-juridique-rgpd` | Skill agent, `scripts/audit_pages.py`, `scripts/audit_cookies.mjs`, `scripts/report.py` |
| Cyber | https://github.com/kferrandonFulbert/skill-audit-cyber | `audit-cybersecurite-web` | Skill agent, méthodologie OWASP et outils disponibles autorisés |

## Installation suggérée (hors répertoire de l'orchestrateur)
```bash
git clone https://github.com/kferrandonFulbert/skill-audit-seo.git
git clone https://github.com/kferrandonFulbert/skill-audit-juridique-web.git
git clone https://github.com/kferrandonFulbert/skill-audit-cyber.git
```
Installer ou enregistrer chacun dans le répertoire de Skills reconnu par l'agent ; ce répertoire varie selon l'application. Vérifier les dépendances, instructions et scripts avant exécution. Épingler les commits pour la reproductibilité.

## Compatibilité
Les trois Skills ne promettent pas un format JSON identique. Leurs sorties doivent être converties au schéma `schemas/audit-result.schema.json` avec provenance conservée. Ne pas traiter un résultat d'inventaire ou de scan passif comme une conclusion juridique ou une preuve de vulnérabilité exploitable.

## Commandes connues du Skill juridique
```bash
python scripts/audit_pages.py https://example.org --out resultat.json
node scripts/audit_cookies.mjs https://example.org cookies.json
python scripts/report.py resultat.json --out-dir rapports
```
Les autres commandes doivent être déterminées en lisant les fichiers SKILL.md et scripts de la version locale effectivement installée, pas devinées.
