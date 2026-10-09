"""Independent deterministic forward occupancy evaluation; conservative screening is updated using deterministically evaluated incumbents."""
import concurrent.futures as cf,json,hashlib,subprocess,time,threading
LOCKS={}
from pathlib import Path
from search import *

def canonical(v):
 v=v.copy()
 if v[0]==-1:v[5:9]=v[1:5]
 if v[9]>=999:v[9:11]=[1000,1000];v[13:17]=v[11:13]*2
 elif v[10]>=999:v[10]=1000;v[15:17]=v[13:15]
 for i in [3,7,11,13,15]+([22,26] if v[0]==-2 else []):
  if v[i]==0:v[i+1]=100
 if len(v)==19:v.append(0)
 return v

def state_metrics(region,p):
 key=hashlib.sha256(json.dumps(canonical(p['parameters'])).encode()).hexdigest()[:20];directory=W/'exact_cache'/region/key;directory.mkdir(parents=True,exist_ok=True);pol=directory/'policy.txt';textrows([p],pol);data={}
 for variant in VARIANTS:
  out=directory/(variant+'.json')
  if not out.exists():subprocess.run([str(BIN/'exact'),str(pol),str(F/'route_inputs'/f'{region}_{variant}.route'),region,str(out)],check=True)
  data[variant]=json.loads(out.read_text())
 scenario=[]
 for c in CASES:
  if c['region']!=region:continue
  d=data[c['route']];coeff=[c['base'],1/c['entry'],1200/c['rate'],1];seconds=sum(a*b for a,b in zip(coeff,d['cost_mean']));regret=seconds-c['optimum_seconds'];scenario.append(dict(scenario=c['id'],seconds=seconds,optimum_seconds=c['optimum_seconds'],regret_seconds=regret,regret_percent=100*regret/c['optimum_seconds'],resources=d))
 return dict(id=p['id'],region=region,cache_key=key,complexity=p['complexity'],features=p['features'],tier=p['tier'],compact=p['compact'],worst_regret=max(c['regret_percent'] for c in scenario)/100,worst_seconds=max(c['regret_seconds'] for c in scenario),mean_regret=sum(c['regret_percent'] for c in scenario)/len(scenario)/100,mean_seconds=sum(c['regret_seconds'] for c in scenario)/len(scenario),cases=scenario)

def run(job):
 region,p=job;file=OUT/'exact'/f'{region}_{p["id"]}.json'
 if file.exists():return json.loads(file.read_text())
 key=(region,tuple(canonical(p['parameters'])))
 with LOCKS.setdefault(key,threading.Lock()):result=state_metrics(region,p)
 file.write_text(json.dumps(result,indent=2));return result

def leaders(candidates,region):
 keep={p['id'] for p in candidates if p['complexity']==min(q['complexity'] for q in candidates)}
 for tier in range(1,5):keep.update(p['id'] for p in sorted([p for p in candidates if p['tier']==tier],key=lambda p:p['regions'][region]['screen']['point'])[:6])
 for C in sorted({p['complexity'] for p in candidates}):keep.update(p['id'] for p in sorted([p for p in candidates if p['complexity']==C],key=lambda p:p['regions'][region]['screen']['point'])[:3])
 return keep

if __name__=='__main__':
 (OUT/'exact').mkdir(exist_ok=True);candidates=[p for p in json.loads((OUT/'candidates.json').read_text()) if p.get("valid",True)];evaluated=[];protected={r:leaders(candidates,r) for r in ['PAL','NTSC-U']};jobs=[(r,p) for r in protected for p in candidates if p['id'] in protected[r]]
 print('Exact complexity-band/tier leaders',len(jobs),flush=True)
 with cf.ThreadPoolExecutor(max_workers=2) as ex:
  for n,d in enumerate(ex.map(run,jobs)):evaluated.append(d)
 print('Leader evaluation complete',flush=True)
 # Deterministically evaluated feasible incumbents tighten only the SCREENING uncertainty test. This is not deterministic empirical dominance of unevaluated candidates.
 keep={r:set(protected[r]) for r in protected};reasons={}
 for r in keep:
  incumbents=[d for d in evaluated if d['region']==r]
  for p in candidates:
   lower=p['regions'][r]['screen']['lower'];available=[d['worst_regret'] for d in incumbents if d['complexity']<=p['complexity']]
   bound=min(available) if available else float('inf')
   if lower<=bound:keep[r].add(p['id'])
   reasons[r,p['id']]=dict(screen_lower_regret=lower,exact_incumbent_regret=bound,protected_band_or_tier_leader=p['id'] in protected[r])
 remaining=[(r,p) for r in keep for p in candidates if p['id'] in keep[r] and not (OUT/'exact'/f'{r}_{p["id"]}.json').exists()]
 print('Additional confidence-compatible candidates',len(remaining),flush=True)
 with cf.ThreadPoolExecutor(max_workers=2) as ex:
  for n,d in enumerate(ex.map(run,remaining)):
   evaluated.append(d)
   if n%100==0:print('Exact additional',n,'/',len(remaining),flush=True)
 for p in candidates:
  for r in keep:
   p['regions'][r]['status']='exactly_evaluated' if (OUT/'exact'/f'{r}_{p["id"]}.json').exists() else 'not_retained_after_screening';p['regions'][r]['retention']=reasons[r,p['id']]
 catalog=json.loads((OUT/'candidates.json').read_text());
 for p in candidates:catalog[p['id']]=p
 (OUT/'candidates.json').write_text(json.dumps(catalog,indent=2));(OUT/'exact_evaluation_configuration.json').write_text(json.dumps(dict(initial_leaders={r:len(protected[r]) for r in protected},exact_evaluated={r:len(keep[r]) for r in keep},screening_update='Candidate simultaneous lower regret interval compared against a lower/equal-complexity receiving deterministic forward evaluation feasible incumbent; plus protected band/tier leaders. No point-estimate-only rejection or deterministic dominance claim for unevaluated candidates.'),indent=2));print('Deterministic forward evaluation complete',flush=True)
