"""Reproducible scenario runner; frozen routes are never changed here."""
import concurrent.futures as cf, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/corrected';WORK=ROOT/'work/corrected'
def run(job):
 region,variant,mode,threshold,tol,base,rate,entry=job
 tag=f'{region}_{variant}_{mode}'
 if mode=='threshold':tag+=str(threshold)
 if (tol,base,rate,entry)!=(1e-6,20,300,15):tag+=f'_tol{tol:g}_b{base}_r{rate}_i{entry}'
 prefix=WORK/tag;source=OUT/f'{region}_{variant}.json';route=json.loads(source.read_text());digest=hashlib.sha256(source.read_bytes()).hexdigest()
 assert digest==source.with_suffix('.sha256').read_text().strip()
 txt=WORK/f'{region}_{variant}.route';txt.write_text(''.join(f'{p["unlocked"]} {p["wallet_cap"]} {len(p["pickups"])} '+ ' '.join(map(str,p['pickups']))+'\n' for p in route['phases']))
 config=dict(max_bundles=4 if region=='NTSC-U' else 3,region=region,route=variant,route_sha256=digest,mode=mode,threshold=threshold,tolerance_seconds=tol,pull_base_seconds=base,farming_rupees_per_minute=rate,entry_inputs_per_second=entry)
 complete=all(Path(str(prefix)+f'_phase{j}.policy').exists() and Path(str(prefix)+f'_phase{j}.policy').stat().st_size==(min(135,p['unlocked'])+1)*400000*2 for j,p in enumerate(route['phases']))
 if not prefix.with_suffix('.json').exists() or not complete:
  with prefix.with_suffix('.log').open('w') as err,prefix.with_suffix('.stdout').open('w') as stdout:
   subprocess.run([str(WORK/'full_solver'),str(txt),str(prefix),region,mode,str(threshold),str(tol),str(base),str(rate),str(entry)],stderr=err,stdout=stdout,check=True)
 result=json.loads(prefix.with_suffix('.json').read_text());result.update(config);(OUT/(tag+'_solve.json')).write_text(json.dumps(result,indent=2))
 subprocess.run([str(WORK/'evaluate_exact'),str(txt),str(prefix),region,str(OUT/(tag+'_exact.json')),str(base),str(rate),str(entry)],check=True)
 if abs(json.loads((OUT/(tag+'_exact.json')).read_text())['expected_seconds']-result['expected_seconds'])>max(1e-5,tol*1000):raise RuntimeError('independent evaluation mismatch')
 subprocess.run([str(WORK/'simulate'),str(txt),str(prefix),region,str(OUT/(tag+'_simulation.json')),'20000','20261007',str(base),str(rate),str(entry)],check=True)
 print(tag,result['expected_seconds'],flush=True);return tag
if __name__=='__main__':
 variants=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late']
 jobs=[(r,v,'optimal',27,1e-6,20,300,15) for r in ['PAL','NTSC-U'] for v in variants]
 jobs += [(r,'reference',m,27,1e-6,20,300,15) for r in ['PAL','NTSC-U'] for m in ['one','guarantee','eighty']]
 jobs += [(r,'reference','optimal',27,1e-7,20,300,15) for r in ['PAL','NTSC-U']]
 if len(sys.argv)>1 and sys.argv[1]=='sensitivity':
  jobs=[(r,'reference','optimal',27,1e-6,b,f,i) for r in ['PAL','NTSC-U'] for b,f,i in [(15,300,15),(25,300,15),(20,250,15),(20,350,15)]]
  jobs += [('PAL','reference','optimal',27,1e-6,20,300,i) for i in [12,18]]
 with cf.ThreadPoolExecutor(max_workers=2) as ex:
  for result in ex.map(run,jobs):pass
