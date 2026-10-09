"""One fixed observable lookup, evaluated unchanged on every frozen route.
Its sole alternate-table trigger is current displayed probability and owned count.
No future route resources are queried by the policy.
"""
import concurrent.futures as cf,csv,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'work/corrected';O=ROOT/'outputs/corrected'
base=sys.argv[1] if len(sys.argv)>1 else 'reference'
variants=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late','missed_postgame']
def run(job):
 region,variant=job;sourcebase=base.removeprefix('cap_').removeprefix('mid_').removeprefix('halfmid_').removeprefix('halfcap_');prefixmode='halfcap' if base.startswith('halfcap_') else 'halfmid' if base.startswith('halfmid_') else 'mid' if base.startswith('mid_') else 'observable';spec=f'{prefixmode}:{W}/{region}_{sourcebase}_optimal|{W}/{region}_fusion_early_optimal';
 if base.startswith(('cap_','mid_','halfmid_','halfcap_')):spec+=f'|{W}/{region}_missed_postgame_optimal'
 tag=f'{region}_{variant}_observable_{base}';out=O/(tag+'_exact.json')
 subprocess.run([str(W/'evaluate_exact'),str(W/f'{region}_{variant}.route'),spec,region,str(out)],check=True)
 subprocess.run([str(W/'simulate'),str(W/f'{region}_{variant}.route'),spec,region,str(O/(tag+'_simulation.json')),'20000','20261011'],check=True)
 d=json.loads(out.read_text());opt=json.loads((O/f'{region}_{variant}_optimal_exact.json').read_text())['expected_seconds'];d.update(region=region,route=variant,optimum_seconds=opt,regret_seconds=d['expected_seconds']-opt,regret_percent=100*(d['expected_seconds']-opt)/opt);out.write_text(json.dumps(d,indent=2));print(region,variant,d['regret_seconds'],d['regret_percent'],flush=True);return d
if __name__=='__main__':
 with cf.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(run,[(r,v) for r in ['PAL','NTSC-U'] for v in variants]))
 keys=['region','route','expected_seconds','optimum_seconds','regret_seconds','regret_percent','retained','lost','purchased','farmrupees','trips','pulls','dupes']
 with (O/f'observable_{base}_regret.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)
