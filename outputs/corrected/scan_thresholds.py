import concurrent.futures as cf,csv,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'work/corrected';O=ROOT/'outputs/corrected'
def run(job):
 region,x=job;prefix=W/f'{region}_reference_threshold{x}'
 if not prefix.with_suffix('.json').exists():
  with prefix.with_suffix('.log').open('w') as err:
   subprocess.run([str(W/'full_solver'),str(W/f'{region}_reference.route'),str(prefix),region,'threshold',str(x),'1e-6','20','300','15','0'],stdout=subprocess.DEVNULL,stderr=err,check=True)
 d=json.loads(prefix.with_suffix('.json').read_text());row=dict(region=region,threshold=x,seconds=d['expected_seconds'],residual=d['max_residual_seconds']);print(region,x,row['seconds'],flush=True);return row
if __name__=='__main__':
 with cf.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(run,[(r,x) for r in ['PAL','NTSC-U'] for x in range(101)]))
 with (O/'threshold_scan.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 best={r:min([d for d in rows if d['region']==r],key=lambda d:d['seconds']) for r in ['PAL','NTSC-U']};(O/'best_threshold.json').write_text(json.dumps(best,indent=2))
