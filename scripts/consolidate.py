#!/usr/bin/env python3
"""Consolide trois rapports normalisés. Bibliothèque standard uniquement."""
import argparse, json, html
from pathlib import Path
from datetime import datetime, timezone

DOMAINS = ('seo', 'juridique', 'cybersecurite')
WEIGHTS = {'seo': .35, 'juridique': .35, 'cybersecurite': .30}
SEVERITY = {'critique': 0, 'elevee': 1, 'moyenne': 2, 'faible': 3, 'information': 4}
LABELS = {'seo': 'SEO', 'juridique': 'Juridique & RGPD', 'cybersecurite': 'Cybersécurité'}


def validate(data, domain, target):
    if not isinstance(data, dict): raise ValueError('Le rapport doit être un objet JSON')
    for k in ('schema_version', 'domain', 'status', 'target', 'findings'):
        if k not in data: raise ValueError(f'Champ obligatoire manquant : {k}')
    if data['schema_version'] != '1.0' or data['domain'] != domain: raise ValueError('Version ou domaine incompatible')
    if data['target'].rstrip('/') != target.rstrip('/'): raise ValueError('Cible différente du périmètre demandé')
    if data['status'] not in ('execute','partiel','non_execute'): raise ValueError('Statut inconnu')
    if not isinstance(data['findings'], list): raise ValueError('findings doit être une liste')
    if data['status'] == 'non_execute' and data['findings']: raise ValueError('Un audit non exécuté ne peut contenir des constats')
    for key, upper in [('score', 100), ('coverage', 1)]:
        v = data.get(key)
        if v is not None and (isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= upper): raise ValueError(f'{key} hors limites')
    if data['status'] == 'non_execute' and data.get('score') is not None: raise ValueError('Pas de score pour un audit non exécuté')
    for i, f in enumerate(data['findings']):
        if not isinstance(f, dict) or any(k not in f for k in ('id','title','status','severity','evidence','recommendation')): raise ValueError(f'Constat {i} incomplet')
        if f['severity'] not in SEVERITY or f['status'] not in ('non_conformite_demontree','risque','a_verifier','conforme_perimetre','non_applicable'): raise ValueError(f'Constat {i} invalide')
        if not isinstance(f['evidence'], list) or any(not isinstance(x,str) for x in f['evidence']): raise ValueError(f'Preuves invalides : {i}')
        if f['status'] == 'non_conformite_demontree' and not f['evidence']: raise ValueError(f'Preuve obligatoire pour non-conformité démontrée : {i}')
    return data


def build(indir, target):
    modules = {}; errors = []
    for domain in DOMAINS:
        path = indir / f'{domain}.json'
        if not path.exists():
            modules[domain] = {'schema_version':'1.0','domain':domain,'target':target,'status':'non_execute','reason':'Rapport absent','score':None,'coverage':None,'findings':[],'manual_checks':[]}
            continue
        try:
            modules[domain] = validate(json.loads(path.read_text(encoding='utf-8')), domain, target)
        except (ValueError, json.JSONDecodeError) as e:
            errors.append(f'{path.name} : {e}')
            modules[domain] = {'schema_version':'1.0','domain':domain,'target':target,'status':'non_execute','reason':f'Rapport invalide : {e}','score':None,'coverage':None,'findings':[],'manual_checks':[]}
    complete = all(m['status']=='execute' for m in modules.values())
    scored = all(m['status']=='execute' and m.get('score') is not None and m.get('coverage') is not None and m['coverage'] >= .5 for m in modules.values())
    score = round(sum(modules[d]['score']*WEIGHTS[d] for d in DOMAINS),1) if scored else None
    findings = [dict(f, domain=d) for d in DOMAINS for f in modules[d]['findings']]
    actionable = sorted((f for f in findings if f['status'] in ('non_conformite_demontree','risque','a_verifier')), key=lambda f:(SEVERITY[f['severity']], f['domain'],f['id']))
    return {'schema_version':'1.0','target':target,'generated_at':datetime.now(timezone.utc).isoformat(), 'status':'complet' if complete else 'partiel','global_score':score,'weights':WEIGHTS,'minimum_coverage_for_score':.5,'modules':modules,'findings':findings,'action_plan':actionable,'validation_errors':errors}


def markdown(report):
    lines = ['# Rapport Audit Web 360°', '', f"**Cible :** {report['target']}",f"**Date :** {report['generated_at']}",f"**État :** {report['status']}",f"**Score global indicatif :** {str(report['global_score']) + '/100' if report['global_score'] is not None else 'Non calculable (modules ou couverture insuffisants)'}",'', '## Synthèse des modules', '']
    for d,m in report['modules'].items():
        lines += [f"### {LABELS[d]}",f"- État : {m['status']}",f"- Note : {str(m.get('score'))+'/100' if m.get('score') is not None else 'Non disponible'}",f"- Couverture : {str(round(m['coverage']*100))+'%' if m.get('coverage') is not None else 'Inconnue'}"]
        if m.get('reason'): lines.append(f"- Limite : {m['reason']}")
        lines.append('')
    lines += ['## Plan d’action priorisé','']
    if not report['action_plan']: lines.append('Aucun constat actionnable rapporté ; cela ne prouve pas une conformité totale.\n')
    for f in report['action_plan']:
        lines += [f"### [{LABELS[f['domain']]}] {f['title']} — {f['severity']}",f"- Statut : {f['status']}",f"- Correction : {f['recommendation']}",f"- Preuves : {' ; '.join(f['evidence']) if f['evidence'] else 'Non fournies'}"]
        for ref in f.get('references',[]): lines.append(f"- Référence : {ref.get('title','')} — {ref.get('url','')} (consultée : {ref.get('checked_at','non renseignée')})")
        lines.append('')
    lines += ['## Vérifications humaines restantes','']
    checks = [(d,c) for d,m in report['modules'].items() for c in m.get('manual_checks',[])]
    lines += [f'- {LABELS[d]} : {c}' for d,c in checks] if checks else ['Aucune liste fournie par les modules.']
    lines += ['','## Limites','', 'Rapport fondé uniquement sur les données fournies. Les modules non exécutés et les contrôles non observables ne sont pas évalués. Les notes ne constituent ni certification de conformité juridique ni garantie de sécurité.']
    if report['validation_errors']: lines += ['','## Erreurs de validation'] + [f'- {e}' for e in report['validation_errors']]
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser(); p.add_argument('--input-dir',type=Path,required=True); p.add_argument('--out-dir',type=Path,required=True); p.add_argument('--target',required=True); a=p.parse_args()
    r=build(a.input_dir,a.target); a.out_dir.mkdir(parents=True,exist_ok=True)
    (a.out_dir/'rapport-360.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    md=markdown(r); (a.out_dir/'rapport-360.md').write_text(md,encoding='utf-8')
    # HTML texte sûr : aucune interpolation HTML non échappée depuis les résultats
    (a.out_dir/'rapport-360.html').write_text('<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Audit Web 360°</title><style>body{font:16px/1.6 system-ui;max-width:960px;margin:40px auto;padding:0 20px;color:#17212e}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f7fa;padding:24px;border-radius:12px}</style><main><pre>'+html.escape(md)+'</pre></main></html>',encoding='utf-8')
    print(f"Rapports créés dans {a.out_dir}; état={r['status']}; note={r['global_score']}")

if __name__=='__main__': main()
