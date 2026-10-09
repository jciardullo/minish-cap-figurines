import json,math,hashlib,sys
from pathlib import Path
D=Path(__file__).resolve().parents[1];S=D/'supplemental';sys.path.insert(0,str(D))
from complexity_audit import audit,normalize
from frontier import knee
b=json.loads((S/'predeclared_bounds.json').read_text());assert hashlib.sha256((D/'candidates.txt').read_bytes()).hexdigest()==b['frozen_candidate_sha256']
allp=json.loads((S/'candidate_definitions.json').read_text());low=allp['low']+json.loads((S/'C8_definitions.json').read_text());assert len(low)==214 and len({tuple(normalize(p['parameters'])) for p in low})==214
assert sum(p['complexity']==7 for p in low)==4 and sum(p['complexity']==8 for p in low)==210
for p in low:assert audit(p['parameters'])[0:2]==(p['features'],p['complexity'])
for r in ['PAL','NTSC-U']:
 for p in low+allp['tier5'][r]:
  d=json.loads((S/f'evaluations/{r}_{p["id"]}.json').read_text());assert d['features']==p['features'] and d['complexity']==p['complexity'];assert len(d['cases'])==(14 if r=='PAL' else 12)
  ref=next(c['resources'] for c in d['cases'] if c['scenario']==r+':route:reference')
  for c in d['cases']:
   if ':timing:' in c['scenario']:assert c['resources']==ref
   z=c['resources'];assert abs(z['complete']-1)<1e-8 and abs(z['shellerr'])<1e-7 and abs(z['casherr'])<1e-7
  if p['id']>=12000 and p['id']<14000:assert p['features'][4]<=12 and p['features'][3]<=4
 f=json.loads((S/(r+'_expanded_frontier.json')).read_text());k,_,_=knee(f);assert k['id']==(6457 if r=='PAL' else 6098)
m=json.loads((S/'restricted_information_benchmark.json').read_text())
for r,v in m.items():
 for prior,p in v.items():
  for q in p['policies'].values():assert abs(q['prior_mean_future_informed_gap_seconds']-(q['restricted_benchmark_minus_future_informed_seconds']+q['policy_minus_restricted_benchmark_seconds']))<1e-8
paper=(D/'paper.tex').read_text();guide=(D/'player_strategy.md').read_text()
for r,id in [('PAL',8911),('NTSC-U',8560)]:
 d=json.loads((D/f'exact/{r}_{id}.json').read_text());ref=next(c for c in d['cases'] if c['scenario']==r+':route:reference');assert f'{ref["seconds"]/60:.2f}' in paper and f'{ref["seconds"]/60:.2f}' in guide;assert f'{100*d["worst_regret"]:.2f}' in paper and f'{100*d["worst_regret"]:.2f}' in guide
assert 'holding B' in paper and 'Project lead and curator: jciardullo' in paper
assert '4{,}000{,}000' not in paper
print('Supplemental definitions, all 490 regional records, timing invariance, conservation, knees, additive gaps, headlines and frozen hash verified.')
