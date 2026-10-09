import csv,hashlib,json
from pathlib import Path
O=Path(__file__).resolve().parent;W=O.parents[1]/'work/funded';LEDGERS=O.parent/'corrected'
variants=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late','missed_postgame']
rows=[];validation=[];convergence=[]
for region in ['PAL','NTSC-U']:
 for variant in variants:
  p=O/f'{region}_{variant}_optimal_exact.json'
  if not p.exists():continue
  d=json.loads(p.read_text());route=LEDGERS/f'{region}_{variant}.json';digest=hashlib.sha256(route.read_bytes()).hexdigest();assert digest==route.with_suffix('.sha256').read_text().strip()
  rows.append(dict(region=region,route=variant,route_sha256=digest,seconds=d['expected_seconds'],minutes=d['expected_seconds']/60,pulls=d['pulls'],duplicates=d['dupes'],natural_retained=d['retained'],overflow=d['lost'],consumed=d['used'],purchased=d['purchased'],farming_pickups=d['farm'],farming_seconds=4*d['farm'],farmed_rupees_gross=20*d['farm'],farmed_rupees_retained=d['farmrupees'],farmed_rupees_lost=20*d['farm']-d['farmrupees'],purchase_rupees=d['purchased']*(300 if region=='PAL' else 200)/30,refund_retained=d['refund'],refund_lost=d['refundlost'],trips=d['trips'],ending_shells=d['endS'],ending_rupees=d['endR']))
 base=W/f'{region}_reference_optimal';tight=W/f'{region}_reference_optimal_tol1e-07_b20_r300_i15'
 counts=[]
 for phase in range(9):
  changed=0
  with Path(str(base)+f'_phase{phase}.policy').open('rb') as a,Path(str(tight)+f'_phase{phase}.policy').open('rb') as b:
   while True:
    x=a.read(1<<20);y=b.read(1<<20)
    if not x:assert not y;break
    assert len(x)==len(y)
    if x!=y:changed+=sum(x[i:i+2]!=y[i:i+2] for i in range(0,len(x),2))
  counts.append(changed)
 samples={}
 for label,prefix in [('base',base),('tight',tight)]:
  samples[label]={(int(r['phase']),int(r['owned']),int(r['shells']),int(r['rupees'])):r for r in csv.DictReader(open(str(prefix)+'_values.csv'))}
 tied_changed=sum(samples['base'][key].get('tied_actions')!=samples['tight'][key].get('tied_actions') for key in samples['base'])
 validation.append(dict(region=region,policy_changes_by_phase=counts,sampled_tied_sets_changed=tied_changed,max_sample_value_difference=max(abs(float(v['seconds'])-float(samples['tight'][k]['seconds'])) for k,v in samples['base'].items())))
 ref=samples['base'];reference_route=json.loads((LEDGERS/f'{region}_reference.json').read_text())
 for variant in variants[1:]:
  path=W/f'{region}_{variant}_optimal_values.csv'
  if not path.exists():continue
  other={(int(r['phase']),int(r['owned']),int(r['shells']),int(r['rupees'])):r for r in csv.DictReader(open(path))};vr=json.loads((LEDGERS/f'{region}_{variant}.json').read_text())
  for phase in range(9):
   keys=[k for k in ref if k[0]==phase and k in other]
   convergence.append(dict(region=region,route=variant,phase=phase,milestone=reference_route['phases'][phase]['milestone'],same_available_pool=reference_route['phases'][phase]['unlocked']==vr['phases'][phase]['unlocked'],matched_sample_states=len(keys),max_value_difference=max(abs(float(ref[k]['seconds'])-float(other[k]['seconds'])) for k in keys),representative_action_disagreements=sum(ref[k]['action']!=other[k]['action'] for k in keys)))
for name,data in [('regional_route_results.csv',rows),('route_convergence.csv',convergence)]:
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
(O/'tolerance_validation.json').write_text(json.dumps(validation,indent=2))
sensitivity=[]
for region in ['PAL','NTSC-U']:
 d=[x for x in rows if x['region']==region];ref=next(x['seconds'] for x in d if x['route']=='reference');lo=min(x['seconds'] for x in d);hi=max(x['seconds'] for x in d)
 sensitivity.append(dict(region=region,routes=len(d),minimum_seconds=lo,maximum_seconds=hi,range_seconds=hi-lo,range_percent_of_reference=100*(hi-lo)/ref))
(O/'route_sensitivity.json').write_text(json.dumps(sensitivity,indent=2));print(json.dumps(validation,indent=2));print(json.dumps(sensitivity,indent=2))
