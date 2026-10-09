"""Globally compare threshold percentages; certify dominated cases with a relaxed SSP lower bound."""
import concurrent.futures as cf,csv,json,math,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'work/funded';O=ROOT/'outputs/funded';BIN=ROOT/'work/corrected';LEDGERS=ROOT/'outputs/corrected'
def lower_bound(region,x):
 route=json.loads((LEDGERS/f'{region}_reference.json').read_text());us=[p['unlocked'] for p in route['phases']];natural=route['natural_shells'];unit=2 if region=='PAL' else 4/3;bundles=3 if region=='PAL' else 4;overhead=.5+20/(30*bundles);bounds=[]
 for alpha in [0,.25,.5,.75,1]:
  for beta in [0,overhead*.25,overhead*.5,overhead*.75,overhead]:
   c=alpha*unit+beta;nxt=[math.inf]*137;nxt[136]=0
   for U in reversed(us):
    v=[math.inf]*137;v[136]=0
    for f in range(min(135,U),-1,-1):
     pull=math.inf
     if f<U:
      b=max(1,100*(U-f)//U);s=1 if b>x else 101-b;h=15 if f<50 else 12 if f<80 else 9 if f<110 else 6;p=max(h,b+s-1)/100;entry=(s-1)/15 if region=='PAL' else math.ceil((s-1)/10)/15
      pull=(20+entry+c*s-alpha*(1-p))/p+v[f+1]
     v[f]=min(nxt[f],pull)
    nxt=v
   bounds.append(nxt[0]-c*natural)
 return max(bounds)
upper={'PAL':7848.58533309075,'NTSC-U':7439.0422104335}
for r in upper:
 values=[json.loads(p.read_text())['expected_seconds'] for p in W.glob(f'{r}_reference_threshold*.json')]
 if values:upper[r]=min(upper[r],min(values))
def run(job):
 region,x=job;prefix=W/f'{region}_reference_threshold{x}';lb=lower_bound(region,x)
 if not prefix.with_suffix('.json').exists() and lb>upper[region]+1e-5:return dict(region=region,threshold=x,seconds=None,residual=None,lower_bound_seconds=lb,status='certified_dominated')
 if not prefix.with_suffix('.json').exists():
  with prefix.with_suffix('.log').open('w') as err:
   subprocess.run([str(BIN/'full_solver'),str(W/f'{region}_reference.route'),str(prefix),region,'threshold',str(x),'1e-6','20','300','15','0'],stdout=subprocess.DEVNULL,stderr=err,check=True)
 d=json.loads(prefix.with_suffix('.json').read_text());assert lb<=d['expected_seconds']+1e-5;row=dict(region=region,threshold=x,seconds=d['expected_seconds'],residual=d['max_residual_seconds'],lower_bound_seconds=lb,status='solved');print(region,x,row['seconds'],flush=True);return row
if __name__=='__main__':
 with cf.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(run,[(r,x) for r in ['PAL','NTSC-U'] for x in range(101)]))
 with (O/'threshold_scan.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 best={r:min([d for d in rows if d['region']==r and d['status']=='solved'],key=lambda d:d['seconds']) for r in ['PAL','NTSC-U']};(O/'best_threshold.json').write_text(json.dumps(best,indent=2));print(best)
