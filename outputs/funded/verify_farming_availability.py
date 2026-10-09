"""Feasible-policy / relaxed-lower-bound certificate after disabling pre-Mitts farming."""
import concurrent.futures as cf,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'work/funded';O=ROOT/'outputs/funded';B=ROOT/'work/corrected'
def check(p):
 tag=p.name.removesuffix('_exact.json');r=tag.split('_')[0];variants=['missed_postgame','missed_early','missed_late','fusion_early','fusion_late','reference','earlier','later'];v=next((v for v in variants if tag.startswith(r+'_'+v+'_')),None)
 if not v:return
 prefix=W/tag
 if not Path(str(prefix)+'_phase0.policy').exists():return
 cfgpath=O/(tag+'_solve.json');cfg=json.loads(cfgpath.read_text()) if cfgpath.exists() else {};out=W/(tag+'_legality.json')
 args=[str(cfg.get(k,d)) for k,d in [('pull_base_seconds',20),('farming_rupees_per_minute',300),('entry_inputs_per_second',15)]]
 proc=subprocess.run([str(B/'evaluate_exact'),str(W/f'{r}_{v}.route'),str(prefix),r,str(out),*args],capture_output=True,text=True)
 if proc.returncode:return dict(tag=tag,legal=False,error=proc.stderr)
 d=json.loads(out.read_text());old=json.loads(p.read_text());delta=d['expected_seconds']-old['expected_seconds'];assert abs(delta)<1e-5,(tag,delta)
 return dict(tag=tag,legal=True,expected_seconds=d['expected_seconds'],difference_seconds=delta,certificate='Selected reachable policy is feasible without pre-Mitts farming; equals relaxed initial value within 1e-5 seconds.')
if __name__=='__main__':
 with cf.ThreadPoolExecutor(max_workers=2) as ex:results=[d for d in ex.map(check,O.glob('*_exact.json')) if d]
 assert all(d['legal'] for d in results),results
 (O/'farming_availability_validation.json').write_text(json.dumps(results,indent=2));print(len(results),'legality checks passed')
