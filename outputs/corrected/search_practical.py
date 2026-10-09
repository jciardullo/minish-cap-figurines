"""Pilot search only; final claims require exact evaluation and independent seeds."""
import concurrent.futures as cf,csv,itertools,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'work/corrected';O=ROOT/'outputs/corrected';(W/'pilot').mkdir(exist_ok=True)
variants=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late']
rules=[(x,h,p,stop) for x,h,p,stop in itertools.product([6,10,15,20,27],[700,800,900,950],[50,80,100],[0,100,300,500,700]) if stop<h]
def run(job):
 region,variant,x,h,p,stop=job;file=W/'pilot'/f'{region}_{variant}_{x}_{h}_{p}_{stop}.json'
 if not file.exists():subprocess.run([str(W/'simulate'),str(W/f'{region}_{variant}.route'),f'@{x}:{h}:{p}:{stop}',region,str(file),'500','424242'],check=True,stdout=subprocess.DEVNULL)
 d=json.loads(file.read_text());return dict(region=region,route=variant,threshold=x,inventory_trigger=h,early_target=p,stop_inventory=stop,mean_seconds=d['mean_seconds'],natural_retained=d['retained'],overflow=d['lost'],purchased=d['purchased'],trips=d['trips'])
if __name__=='__main__':
 jobs=[(r,v,*rule) for rule in rules for r in ['PAL','NTSC-U'] for v in variants]
 with cf.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(run,jobs))
 with (O/'practical_pilot.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 ranked=[]
 for x,h,p,stop in rules:
  subset=[a for a in rows if (a['threshold'],a['inventory_trigger'],a['early_target'],a['stop_inventory'])==(x,h,p,stop)]
  ranked.append(dict(threshold=x,inventory_trigger=h,early_target=p,stop_inventory=stop,worst_seconds=max(a['mean_seconds'] for a in subset),mean_seconds=sum(a['mean_seconds'] for a in subset)/len(subset)))
 ranked.sort(key=lambda d:d['worst_seconds']);(O/'practical_pilot_ranking.json').write_text(json.dumps(ranked,indent=2));print(json.dumps(ranked[:10],indent=2))
