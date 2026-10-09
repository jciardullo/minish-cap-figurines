"""Predeclared supplemental deterministic evaluations; original candidates and model immutable."""
import json,sys,time,resource,concurrent.futures as cf,hashlib,itertools
from pathlib import Path
D=Path(__file__).resolve().parents[1];sys.path.insert(0,str(D))
from search import policy
from complexity_audit import audit,normalize
from evaluate import state_metrics
S=D/'supplemental';original=json.loads((D/'candidates.json').read_text());bounds=json.loads((S/'predeclared_bounds.json').read_text());start=time.monotonic();oldusage=resource.getrusage(resource.RUSAGE_CHILDREN)
assert hashlib.sha256((D/'candidates.txt').read_bytes()).hexdigest()==bounds['frozen_candidate_sha256']
def candidate(v,i,family):
 f,C,t,compact,valid=audit(v)
 return dict(id=i,parameters=v,features=f,complexity=C,tier=t,compact=compact,family=family,valid=True)
low=[candidate(policy(early=(1,0,t,100),post=((t,100),)*3,restock=r),11000+j,'supplemental_exhaustive_C7') for j,(t,r) in enumerate(itertools.product([0,100],[0,1]))]
assert len(low)==4 and all(p['complexity']==7 for p in low)
# Behavior aliases irrelevant to the published C7 representatives are normalized out.
byregion={};counts={}
for region,seedid in [('PAL',8911),('NTSC-U',8560)]:
 seed=original[seedid]['parameters'];rows=[];rejected=[]
 for ix,target in itertools.product([3,22,26,11],bounds['tier5']['intermediate_values']):
  v=seed.copy();v[ix+1]=target;rows.append(v)
 for band,target,threshold in itertools.product([100,300,600],bounds['tier5']['intermediate_values'],[None,0]):
  v=seed.copy();v[9:11]=[band,1000];v[11:13]=[seed[11] if threshold is None else threshold,target];v[13:17]=seed[11:13]*2;rows.append(v)
 seen={};base=12000 if region=='PAL' else 13000
 for n,v in enumerate(rows):
  p=candidate(v,base+n,'supplemental_Tier5');key=tuple(normalize(v))
  if p['features'][4]>12 or p['features'][3]>4:rejected.append(p);continue
  # semantic inactive target removal in normalize; no sampling-based dedup.
  if key not in seen:seen[key]=p
 byregion[region]=list(seen.values());counts[region]=dict(raw_generated=len(rows),invalid=len(rejected),after_dedup=len(seen))
(S/'candidate_definitions.json').write_text(json.dumps(dict(low=low,tier5=byregion,counts=counts),indent=2)+'\n')
# Protect a reproducible policy row registry and every numerical evaluation.
for region in ['PAL','NTSC-U']:
 (S/(region+'_policies.txt')).write_text('\n'.join(' '.join(map(str,[p['id'],*p['parameters']])) for p in low+byregion[region])+'\n')
jobs=[(r,p) for r in ['PAL','NTSC-U'] for p in low+byregion[r]]
def run(job):
 r,p=job;out=S/f'evaluations/{r}_{p["id"]}.json';out.parent.mkdir(exist_ok=True)
 if out.exists():return json.loads(out.read_text())
 d=state_metrics(r,p);out.write_text(json.dumps(d,indent=2)+'\n');return d
with cf.ThreadPoolExecutor(max_workers=2) as pool:
 for n,d in enumerate(pool.map(run,jobs)):
  if n%4==0:print('Completed',n+1,'/',len(jobs),d['region'],d['id'],flush=True)
u=resource.getrusage(resource.RUSAGE_CHILDREN)
(S/'compute_resources.json').write_text(json.dumps(dict(wall_seconds=time.monotonic()-start,child_user_seconds=u.ru_utime-oldusage.ru_utime,child_system_seconds=u.ru_stime-oldusage.ru_stime,child_peak_rss_bytes=u.ru_maxrss,peak_rss_units='bytes on macOS; maximum single child, not aggregate',new_policy_region_records=len(jobs),route_evaluation_upper_bound=8*len(jobs),environment=bounds['compute_environment']),indent=2)+'\n')
print('All supplemental evaluation complete',flush=True)
