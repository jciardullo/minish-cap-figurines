"""Export regional benchmark and unchanged-observable timing-regret tables."""
import csv,json
from pathlib import Path
O=Path(__file__).resolve().parent
rows=[]
for region in ['PAL','NTSC-U']:
 for mode in ['one','guarantee','eighty','threshold9' if region=='PAL' else 'threshold10','threshold27','optimal']:
  d=json.loads((O/f'{region}_reference_{mode}_exact.json').read_text());rows.append(dict(region=region,policy=mode,**d))
with (O/'regional_benchmarks.csv').open('w') as f:
 keys=list(dict.fromkeys(k for r in rows for k in r));w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
profiles=['reference','earlier','missed_postgame','cap_reference','mid_reference','halfmid_reference','halfcap_reference'];weights=json.loads((O/'minimax_lookup_profiles.json').read_text())['weights'];rows=[]
for region in ['PAL','NTSC-U']:
 for base,rate,entry in [(20,300,15),(15,300,15),(25,300,15),(20,250,15),(20,350,15)]+([(20,300,12),(20,300,18)] if region=='PAL' else []):
  filename=f'{region}_reference_optimal_exact.json' if (base,rate,entry)==(20,300,15) else f'{region}_reference_optimal_tol1e-06_b{base}_r{rate}_i{entry}_exact.json';opt=json.loads((O/filename).read_text())['expected_seconds'];vals={}
  for profile in profiles:
   d=json.loads((O/f'{region}_reference_observable_{profile}_exact.json').read_text());fixed=45*d['trips']-25*d['shop_only_trips']+.5*d['purchased'];inputs=15*(d['expected_seconds']-20*d['pulls']-4*d['farm']-fixed);vals[profile]=base*d['pulls']+1200/rate*d['farm']+fixed+inputs/entry
  vals['balanced']=sum(weights[k]*vals[k] for k in profiles)
  for p,t in vals.items():rows.append(dict(region=region,pull_base_seconds=base,farming_rupees_per_minute=rate,entry_inputs_per_second=entry,policy=p,optimum_seconds=opt,practical_seconds=t,regret_seconds=t-opt,regret_percent=100*(t-opt)/opt))
with (O/'observable_timing_sensitivity.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Benchmark and timing-regret exports written')
