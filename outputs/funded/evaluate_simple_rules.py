import concurrent.futures as cf,subprocess,json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'outputs/funded';W=ROOT/'work/corrected'
variants=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late','missed_postgame']
def run(job):
 r,v=job;t=9 if r=='PAL' else 10;spec=f'rules:{t}:600:150:700:800:900:20:80';tag=f'{r}_{v}_simple_rules';out=O/(tag+'_exact.json')
 subprocess.run([str(W/'evaluate_exact'),str(W/f'{r}_{v}.route'),spec,r,str(out)],check=True)
 subprocess.run([str(W/'simulate'),str(W/f'{r}_{v}.route'),spec,r,str(O/(tag+'_simulation.json')),'20000','20261020'],check=True)
 d=json.loads(out.read_text());opt=json.loads((O/f'{r}_{v}_optimal_exact.json').read_text())['expected_seconds'];d.update(region=r,route=v,policy=spec,optimum_seconds=opt,regret_seconds=d['expected_seconds']-opt,regret_percent=100*(d['expected_seconds']-opt)/opt);out.write_text(json.dumps(d,indent=2));print(r,v,d['regret_percent'],flush=True);return d
with cf.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(run,[(r,v) for r in ['PAL','NTSC-U'] for v in variants]))
with (O/'simple_rules_regret.csv').open('w') as f:
 keys=['region','route','policy','expected_seconds','regret_seconds','regret_percent','observable_entry_mismatch','retained','lost','purchased','farmrupees','trips','pulls','dupes'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)
