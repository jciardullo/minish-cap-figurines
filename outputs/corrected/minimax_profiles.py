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
A=np.array([x[2]+[-1] for x in rows]);result=linprog([0]*len(profiles)+[1],A_ub=A,b_ub=np.zeros(len(rows)),A_eq=[[1]*len(profiles)+[0]],b_eq=[1],bounds=[(0,1)]*len(profiles)+[(0,None)],method='highs');assert result.success
weights=dict(zip(profiles,result.x[:-1]));out=dict(weights=weights,worst_route_regret_percent=float(result.x[-1]),criterion_percent=5,passes=bool(result.x[-1]<=5));(O/'minimax_lookup_profiles.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
for region,route,regret in rows:print(region,route,float(np.dot(result.x[:-1],regret)))
