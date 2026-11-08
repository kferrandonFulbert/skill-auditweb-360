#!/usr/bin/env python3
"""Exécute uniquement des commandes explicitement configurées, sans shell."""
import argparse, json, subprocess, sys
from pathlib import Path

DOMAINS = ('seo','juridique','cybersecurite')
p=argparse.ArgumentParser()
p.add_argument('--manifest',type=Path,required=True)
p.add_argument('--execute',action='store_true',help='Autorise les commandes déclarées')
a=p.parse_args()
manifest=json.loads(a.manifest.read_text(encoding='utf-8'))
if not a.execute:
    print('Mode aperçu : aucune commande exécutée. Ajouter --execute après vérification du manifeste.')
    print(json.dumps(manifest,ensure_ascii=False,indent=2)); sys.exit(0)
for domain in DOMAINS:
    cfg=manifest.get('modules',{}).get(domain,{})
    cmd=cfg.get('command')
    if not cmd:
        print(f'{domain}: aucune commande configurée — non exécuté'); continue
    if not isinstance(cmd,list) or not cmd or any(not isinstance(x,str) or not x for x in cmd):
        print(f'{domain}: commande invalide',file=sys.stderr); continue
    try:
        print(f'{domain}: exécution de {cmd[0]}',flush=True)
        result=subprocess.run(cmd,cwd=cfg.get('cwd') or None,timeout=min(int(cfg.get('timeout_seconds',180)),900),check=False)
        print(f'{domain}: code retour {result.returncode}')
    except (OSError,subprocess.TimeoutExpired,ValueError) as e:
        print(f'{domain}: échec : {e}',file=sys.stderr)
