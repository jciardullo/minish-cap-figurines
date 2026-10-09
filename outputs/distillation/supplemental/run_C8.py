"""Complete canonical C8 partition, declared before evaluation; C7 computed separately."""
import sys,json,itertools,concurrent.futures as cf,time,resource
from pathlib import Path
D=Path(__file__).resolve().parents[1];sys.path.insert(0,str(D))
from search import policy
from complexity_audit import audit,normalize
from evaluate import state_metrics
S=D/'supplemental';vectors=[]
for t,r in itertools.product(range(1,100),[0,1]):vectors.append(policy(early=(1,0,t,100),post=((t,100),)*3,restock=r))
for early,post,r in itertools.product([0,100],[0,100],[0,1]):
 if early!=post:vectors.append(policy(early=(1,0,early,100),post=((post,100),)*3,restock=r))
for post,r in itertools.product([0,100],[0,1]):vectors.append(policy(early=(1000,0,0,100),post=((post,100),)*3,restock=r))
for r in [0,1]:vectors.append(policy(early=(1,0,100,100),post=((100,100),)*3,restock=r,partial=1))
for t in [0,100]:vectors.append(policy(early=(1,0,t,100),post=((t,100),)*3,restock=2))
assert len(vectors)==210 and len({tuple(normalize(v)) for v in vectors})==210
rows=[]
for n,v in enumerate(vectors):
 f,C,t,compact,valid=audit(v);assert C==8,(v,C)
 rows.append(dict(id=14000+n,parameters=v,features=f,complexity=C,tier=t,compact=compact,valid=True,family='supplemental_exhaustive_C8'))
(S/'C8_definitions.json').write_text(json.dumps(rows,indent=2)+'\n')
start=time.monotonic();old=resource.getrusage(resource.RUSAGE_CHILDREN)
def run(job):
 r,p=job;out=S/f'evaluations/{r}_{p["id"]}.json'
 if out.exists():return
 out.write_text(json.dumps(state_metrics(r,p),indent=2)+'\n')
with cf.ThreadPoolExecutor(max_workers=2) as pool:
 for n,_ in enumerate(pool.map(run,[(r,p) for r in ['PAL','NTSC-U'] for p in rows])):
  if n%40==0:print('C8',n+1,'/420',flush=True)
u=resource.getrusage(resource.RUSAGE_CHILDREN);(S/'C8_compute_resources.json').write_text(json.dumps(dict(wall_seconds=time.monotonic()-start,child_user_seconds=u.ru_utime-old.ru_utime,child_system_seconds=u.ru_stime-old.ru_stime,child_peak_rss_bytes=u.ru_maxrss,policy_region_records=420),indent=2)+'\n')
print('C8 complete',flush=True)
