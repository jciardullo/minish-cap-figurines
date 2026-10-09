"""Predeclared regional Pareto and named-selection rules, without Monte Carlo ranking."""
import csv,json,math
from pathlib import Path
from search import *
from evaluate import canonical
from complexity_audit import normalize
WEIGHTS=[4,2,1,2,1,2,0,1]
def cost(row,weights=WEIGHTS):return sum(a*b for a,b in zip(row['features'],weights))
def frontier(rows,weights=WEIGHTS):
 out=[];best=math.inf
 for C in sorted({cost(r,weights) for r in rows}):
  group=[r for r in rows if abs(cost(r,weights)-C)<1e-10];p=min(group,key=lambda r:(r['worst_regret'],r['mean_regret'],r['id']))
  if p['worst_regret']<best-1e-10:out.append(p);best=p['worst_regret']
 return out

def knee(rows,weights=WEIGHTS):
 f=frontier(rows,weights);lo=min(cost(p,weights) for p in f);hi=max(cost(p,weights) for p in f);rlo=min(p['worst_regret'] for p in f);rhi=max(p['worst_regret'] for p in f)
 scores=[]
 for p in f:
  x=(cost(p,weights)-lo)/(hi-lo) if hi>lo else 0;y=(p['worst_regret']-rlo)/(rhi-rlo) if rhi>rlo else 0;distance=(1-x-y)/math.sqrt(2) if hi>lo and rhi>rlo else 0;scores.append(dict(id=p['id'],normalized_complexity=x,normalized_regret=y,signed_distance=distance))
 interior=[p for p in scores[1:-1] if p['signed_distance']>1e-12]
 if not interior:return f[0],scores,False
 maximum=max(p['signed_distance'] for p in interior);ids={p['id'] for p in interior if abs(p['signed_distance']-maximum)<=1e-10};selected=min((p for p in f if p['id'] in ids),key=lambda p:(cost(p,weights),p['mean_regret'],p['id']));return selected,scores,True

def selections(rows):
 Cmin=min(r['complexity'] for r in rows);minimal=min((r for r in rows if r['complexity']==Cmin),key=lambda r:(r['worst_regret'],r['mean_regret'],r['id']));compact=min((r for r in rows if r['compact']),key=lambda r:(r['worst_regret'],r['complexity'],r['mean_regret'],r['id']));qualified=[r for r in rows if r['worst_regret']<=.05];simple5=min(qualified,key=lambda r:(r['complexity'],r['worst_regret'],r['mean_regret'],r['id'])) if qualified else None;chosen,geometry,exists=knee(rows);return dict(minimal=minimal['id'],knee=chosen['id'],compact=compact['id'],simplest_5_percent=simple5['id'] if simple5 else None,interior_knee_detected=exists,knee_meets_5_percent=chosen['worst_regret']<=.05,geometry=geometry)

def robustness(rows,candidates):
 selected,_,_=knee(rows);results=[]
 for ix,label in enumerate(['P','S','Q','I','L','M','D','B']):
  if label=='D':continue
  for factor in [.8,1.2]:
   w=WEIGHTS.copy();w[ix]*=factor;p,_,has=knee(rows,w);results.append(dict(change=f'{label} weight x{factor}',selected=p['id'],changed=p['id']!=selected['id'],interior=has))
 # Canonical duplicates are behaviorally identical for every legal observation.
 representatives={}
 for r in rows:
  key=tuple(normalize(candidates[r['id']]['parameters']));old=representatives.get(key)
  if old is None or (r['complexity'],r['mean_regret'],r['id'])<(old['complexity'],old['mean_regret'],old['id']):representatives[key]=r
 p,_,_=knee(list(representatives.values()));results.append(dict(change='Remove behaviorally identical candidates',selected=p['id'],changed=p['id']!=selected['id']))
 f=frontier(rows);clean=[]
 for r in f:
  if clean and r['complexity']-clean[-1]['complexity']<=1 and max(abs(a['seconds']-b['seconds']) for a,b in zip(r['cases'],clean[-1]['cases']))<=1:continue
  clean.append(r)
 p,_,_=knee(clean);results.append(dict(change='Remove adjacent near duplicates: delta C<=1 and every-case delta time<=1 s',selected=p['id'],changed=p['id']!=selected['id']))
 return results

if __name__=='__main__':
 candidates=json.loads((OUT/'candidates.json').read_text());selected={};allrows=[];stability={}
 for region in ['PAL','NTSC-U']:
  rows=[d for p in (OUT/'exact').glob(region+'_*.json') if (d:=json.loads(p.read_text())).get('valid',True)];selected[region]=selections(rows);stability[region]=robustness(rows,candidates);f=frontier(rows);(OUT/f'{region}_frontier.json').write_text(json.dumps(f,indent=2));ids={r['id'] for r in f}
  for r in rows:
   dominated=any(q['complexity']<=r['complexity'] and q['worst_regret']<=r['worst_regret']+1e-10 and (q['complexity']<r['complexity'] or q['worst_regret']<r['worst_regret']-1e-10) for q in f);candidates[r['id']]['regions'][region]['status']='exactly_dominated' if dominated else 'exactly_evaluated';r['status']='exactly_dominated' if dominated else 'exactly_evaluated';allrows.append(r)
  print(region,selected[region],flush=True)
 (OUT/'selections.json').write_text(json.dumps(selected,indent=2));(OUT/'knee_stability.json').write_text(json.dumps(stability,indent=2));(OUT/'candidates.json').write_text(json.dumps(candidates,indent=2))
 export=[]
 for r in allrows:
  ref=next(c for c in r['cases'] if c['scenario']==f'{r["region"]}:route:reference');d=ref['resources'];export.append(dict(region=r['region'],id=r['id'],tier=r['tier'],complexity=r['complexity'],features=json.dumps(r['features']),status=r['status'],reference_minutes=ref['seconds']/60,mean_regret_seconds=r['mean_seconds'],mean_regret_percent=100*r['mean_regret'],worst_regret_seconds=r['worst_seconds'],worst_regret_percent=100*r['worst_regret'],shells_consumed=d['used'],pulls=d['cost_mean'][0],purchased_shells=d['purchased'],farming_seconds=4*d['cost_mean'][2],trips=d['trips']))
 with (OUT/'exact_policy_summary.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(export[0]));w.writeheader();w.writerows(export)
