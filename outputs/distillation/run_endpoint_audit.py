import sys,json,concurrent.futures as cf
from pathlib import Path
sys.path.insert(0,'outputs/distillation')
from search import policy
from complexity_audit import audit
from evaluate import state_metrics
from frontier import selections,frontier,knee
O=Path('outputs/distillation')
v=policy(early=(1000,0,0,100),post=((0,100),)*3)
f,C,t,compact,valid=audit(v)
p=dict(id=10000,parameters=v,features=f,complexity=C,tier=t,compact=compact,family='targeted_endpoint_audit')
with cf.ThreadPoolExecutor(max_workers=2) as pool:
 rows=list(pool.map(lambda r:state_metrics(r,p),['PAL','NTSC-U']))
a=dict(policy=p,present_in_frozen_list=False,removal_reason='Never generated: all frozen early triggers <=971; generation grid omitted no-early-pull option. Not removed by screening.',regions={})
for r in rows:
 region=r['region']; existing=[json.loads(x.read_text()) for x in (O/'exact').glob(region+'_*.json') if json.loads(x.read_text()).get('valid',True)]
 before=selections(existing);after=selections(existing+[r]);ref=next(x for x in r['cases'] if x['scenario']==region+':route:reference')
 a['regions'][region]=dict(evaluation=r,reference_minutes=ref['seconds']/60,before_selection=before,after_selection=after,dominators=[x['id'] for x in existing if x['complexity']<=C and x['worst_regret']<=r['worst_regret']],frontier_changed=[x['id'] for x in frontier(existing)]!=[x['id'] for x in frontier(existing+[r])])
(O/'endpoint_audit.json').write_text(json.dumps(a,indent=2)+'\n')
print(json.dumps({r:{k:v for k,v in d.items() if k not in ['evaluation','before_selection','after_selection']} for r,d in a['regions'].items()},indent=2))
