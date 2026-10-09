"""Exact mixture evaluation and genuine 20,000-run mixture distributions."""
import concurrent.futures as cf,collections,csv,json,math,random,statistics,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'outputs/funded';W=ROOT/'work/funded';BIN=ROOT/'work/corrected'
weights={p:v for p,v in json.loads((O/'minimax_lookup_profiles.json').read_text())['weights'].items() if v>0}
variants=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late','missed_postgame'];rng=random.Random(20261021);counts=collections.Counter(rng.choices(list(weights),weights=list(weights.values()),k=20000))
def spec(r,p):
 mode='halfcap' if p=='halfcap_reference' else 'observable';source='reference' if p=='halfcap_reference' else p
 result=f'player:{mode}:{W}/{r}_{source}_optimal|{W}/{r}_fusion_early_optimal'
 if mode=='halfcap':result+=f'|{W}/{r}_missed_postgame_optimal'
 return result
def run(job):
 r,v=job;exact=json.loads((O/f'{r}_{v}_observable_reference_exact.json').read_text());out=O/f'{r}_{v}_selected_single_simulation.json';subprocess.run([str(BIN/'simulate'),str(W/f'{r}_{v}.route'),spec(r,'reference'),r,str(out),'20000','20261022'],check=True)
 profiles={p:json.loads((O/f'{r}_{v}_observable_{p}_exact.json').read_text()) for p in weights};mix={k:sum(weights[p]*profiles[p][k] for p in weights) for k,val in exact.items() if isinstance(val,(int,float))};mix.update(region=r,route=v,weights=weights,observable_classifier_error_seconds_bound=300000*mix['observable_entry_mismatch']);(O/f'{r}_{v}_selected_balanced_exact.json').write_text(json.dumps(mix,indent=2))
 samples=[];parts=[]
 for i,p in enumerate(weights):
  raw=W/f'{r}_{v}_balanced_{p}_times.txt';file=O/f'{r}_{v}_balanced_{p}_part.json';subprocess.run([str(BIN/'simulate'),str(W/f'{r}_{v}.route'),spec(r,p),r,str(file),str(counts[p]),str(20261023+i),'20','300','15','iid','-',str(raw)],check=True);samples.extend(map(float,raw.read_text().splitlines()));parts.append((counts[p],json.loads(file.read_text())))
 assert len(samples)==20000;samples.sort();mean=statistics.mean(samples);sd=statistics.stdev(samples);ci=1.959963984540054*sd/math.sqrt(len(samples));d=dict(runs=20000,preset_seed=20261021,game_seeds=[20261023+i for i in range(len(weights))],preset_counts=dict(counts),mean_seconds=mean,ci95_mean_low=mean-ci,ci95_mean_high=mean+ci,median_seconds=statistics.median(samples),p90_seconds=samples[18000],p95_seconds=samples[19000],sd_seconds=sd)
 for k in ['pulls','duplicates','used','received','retained','lost','refund','refundlost','farm','farmrupees','purchased','trips','shop_only_trips','earlyvisits','endS','endR']:d[k]=sum(n*part[k] for n,part in parts)/20000
 (O/f'{r}_{v}_selected_balanced_simulation.json').write_text(json.dumps(d,indent=2));print(r,v,'mixture',mix['regret_percent'],flush=True);return mix
with cf.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(run,[(r,v) for r in ['PAL','NTSC-U'] for v in variants]))
keys=['region','route','expected_seconds','optimum_seconds','regret_seconds','regret_percent','observable_classifier_error_seconds_bound','retained','lost','purchased','farmrupees','trips','pulls','dupes']
with (O/'selected_balanced_regret.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)
