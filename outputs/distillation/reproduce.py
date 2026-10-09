"""Recompute selected deterministic forward occupancy evaluations independently of published result caches.
Use --all for every recorded receiving deterministic forward evaluation regional policy (potentially hours).
"""
import argparse,json,subprocess,concurrent.futures as cf
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];W=ROOT/'work/distillation/reproduction';W.mkdir(parents=True,exist_ok=True)
a=argparse.ArgumentParser();a.add_argument('--all',action='store_true');args=a.parse_args()
subprocess.run(['clang++','-std=c++17','-O2',str(P/'exact.cpp'),'-o',str(W/'exact')],check=True)
candidates=json.loads((P/'candidates.json').read_text());selected=json.loads((P/'selections.json').read_text());ids=json.loads((P/'exact_evaluated_ids.json').read_text()) if args.all else {r:[s[k] for k in ['minimal','knee','compact']] for r,s in selected.items()}
variants=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late','missed_postgame']
def run(job):
 r,i=job;p=W/f'{r}_{i}.txt';p.write_text(' '.join(map(str,[i,*candidates[i]['parameters']]))+'\n');expected=json.loads((P/'exact'/f'{r}_{i}.json').read_text());largest=0
 for v in variants:
  out=W/f'{r}_{i}_{v}.json';subprocess.run([str(W/'exact'),str(p),str(ROOT/'outputs/funded/route_inputs'/f'{r}_{v}.route'),r,str(out)],check=True);d=json.loads(out.read_text());target=next(x['resources'] for x in expected['cases'] if x['scenario']==f'{r}:route:{v}');largest=max(largest,abs(d['expected_seconds']-target['expected_seconds']));assert largest<1e-5,(r,i,v,largest)
 return dict(region=r,id=i,max_absolute_seconds_difference=largest)
with cf.ThreadPoolExecutor(max_workers=2) as ex:checks=list(ex.map(run,[(r,i) for r in ids for i in ids[r]]))
(W/'checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
