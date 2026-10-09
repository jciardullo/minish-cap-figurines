import json,sys,hashlib,csv
from pathlib import Path
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O))
from complexity_audit import audit
from frontier import selections,frontier
A=json.loads((O/'endpoint_audit.json').read_text());candidates=json.loads((O/'candidates.json').read_text())
assert len(candidates)==10000
assert audit(A['policy']['parameters'])[0:2]==([1,0,0,0,3,0,0,1],8)
for p in candidates:assert audit(p['parameters'])[0:2]==(p['features'],p['complexity'])
for region in ['PAL','NTSC-U']:
 rows=[json.loads(p.read_text()) for p in (O/'exact').glob(region+'_*.json') if json.loads(p.read_text()).get('valid',True)]+[A['regions'][region]['evaluation']]
 selected=selections(rows);assert selected==json.loads((O/'selections.json').read_text())[region]
 assert selected['minimal']==500 and selected['knee']==(6457 if region=='PAL' else 6098)
 assert selected['compact']==(8911 if region=='PAL' else 8560)
 assert [p['id'] for p in frontier(rows)]==[p['id'] for p in json.loads((O/(region+'_frontier.json')).read_text())]
 for p in rows[:-1]:assert (p['features'],p['complexity'])==(candidates[p['id']]['features'],candidates[p['id']]['complexity'])
r=json.loads((O/'exact/NTSC-U_6098.json').read_text())
a=next(c for c in r['cases'] if c['scenario'].endswith(':missed_late'));b=next(c for c in r['cases'] if c['scenario'].endswith(':missed_postgame'))
assert a['seconds']==b['seconds'] and a['resources']==b['resources']
assert a['optimum_seconds']!=b['optimum_seconds']
print('All candidate/evaluation complexity vectors, named selections, updated frontier, and duplicate raw rows verified.')
