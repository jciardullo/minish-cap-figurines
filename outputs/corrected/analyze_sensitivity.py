"""Exact re-costing of fixed observable policies: transitions do not change."""
import csv,json
from pathlib import Path
O=Path(__file__).resolve().parent
rows=[]
for region in ['PAL','NTSC-U']:
 profiles=[json.loads((O/f'{region}_reference_observable_{p}_exact.json').read_text()) for p in ['reference','earlier']]
 settings=[(15,300,15),(20,300,15),(25,300,15),(20,250,15),(20,350,15)]+([(20,300,12),(20,300,18)] if region=='PAL' else [])
 for base,rate,entry in settings:
  tag=f'{region}_reference_optimal'
  if (base,rate,entry)!=(20,300,15):tag+=f'_tol1e-06_b{base}_r{rate}_i{entry}'
  optimum=json.loads((O/(tag+'_solve.json')).read_text())['expected_seconds']
  costs=[]
  for d in profiles:
   input_count=15*(d['expected_seconds']-20*d['pulls']-4*d['farm']-45*d['trips']-.5*d['purchased'])
   costs.append(base*d['pulls']+1200/rate*d['farm']+45*d['trips']+.5*d['purchased']+input_count/entry)
  for profile,value in [('reference',costs[0]),('earlier',costs[1]),('balanced_50_50',sum(costs)/2)]:
   rows.append(dict(region=region,base_pull_seconds=base,farming_rupees_per_minute=rate,entry_inputs_per_second=entry,profile=profile,optimum_seconds=optimum,practical_seconds=value,regret_seconds=value-optimum,regret_percent=100*(value-optimum)/optimum))
with (O/'observable_timing_sensitivity.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for x in rows:
 if x['profile']=='balanced_50_50':print(x)
