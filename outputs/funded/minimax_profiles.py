import csv,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
O=Path(__file__).resolve().parent
profiles=['reference','earlier','missed_postgame','cap_reference','mid_reference','halfmid_reference','halfcap_reference']
variants=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late','missed_postgame']
rows=[]
for region in ['PAL','NTSC-U']:
 for route in variants:
  rows.append((region,route,[json.loads((O/f'{region}_{route}_observable_{p}_exact.json').read_text())['regret_percent'] for p in profiles]))
for region in ['PAL','NTSC-U']:
 for base,rate,entry in [(15,300,15),(25,300,15),(20,250,15),(20,350,15)]+([(20,300,12),(20,300,18)] if region=='PAL' else []):
  optimum=json.loads((O/f'{region}_reference_optimal_tol1e-06_b{base}_r{rate}_i{entry}_exact.json').read_text())['expected_seconds'];regrets=[]
  for profile in profiles:
   d=json.loads((O/f'{region}_reference_observable_{profile}_exact.json').read_text());fixed=45*d['trips']-25*d['shop_only_trips']+.5*d['purchased'];inputs=15*(d['expected_seconds']-20*d['pulls']-4*d['farm']-fixed);value=base*d['pulls']+1200/rate*d['farm']+fixed+inputs/entry;regrets.append(100*(value-optimum)/optimum)
  rows.append((region,f'reference_b{base}_r{rate}_i{entry}',regrets))
A=np.array([x[2]+[-1] for x in rows]);result=linprog([0]*len(profiles)+[1],A_ub=A,b_ub=np.zeros(len(rows)),A_eq=[[1]*len(profiles)+[0]],b_eq=[1],bounds=[(0,1)]*len(profiles)+[(0,None)],method='highs');assert result.success
weights=dict(zip(profiles,result.x[:-1]));out=dict(weights=weights,worst_route_regret_percent=float(result.x[-1]),criterion_percent=5,passes=bool(result.x[-1]<=5));(O/'minimax_lookup_profiles.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
for region,route,regret in rows:print(region,route,float(np.dot(result.x[:-1],regret)))
