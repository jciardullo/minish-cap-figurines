"""Bounded observable-policy search. Frozen mechanics/optima are read-only inputs."""
import concurrent.futures as cf,csv,hashlib,itertools,json,math,random,subprocess,sys
from pathlib import Path
import numpy as np
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/distillation';W=ROOT/'work/distillation';F=ROOT/'outputs/funded';BIN=W
VARIANTS=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late','missed_postgame']
SEED=20261031;LIMIT=10000;BEAM=32
# Boundary is a recognizable flag, never a frozen event ID: 3=completed Fortress of Winds,4=Water Element,6=Wind Element.
def policy(boundary=-1,early=(1,0,0,100),late=None,bands=(1000,1000),post=((0,100),)*3,restock=0,partial=0):
 return [boundary,*early,*(late or early),*bands,*sum((tuple(p) for p in post),()),restock,partial]
def features(v):
 boundary=v[0];early=v[1:5];late=v[5:9];bands=v[9:11];post=[v[11+2*i:13+2*i] for i in range(3)];routines=[early] if boundary==-1 else [early,late]
 if boundary==-2:routines=[early,v[20:24],v[24:28],late]
 P=4 if boundary==-2 else 1+int(boundary!=-1);shell=set();chance=set();inter=set();memory=0;clauses=0
 for trigger,stop,cut,target in routines:
  # stop=trigger-1 represents one stateless threshold (S>stop).
  if trigger<=999:
   if stop>0:shell.add(stop)
   if trigger!=stop+1:shell.add(trigger);memory=1
   if cut not in [0,100]:chance.add(cut)
   if cut>0 and target not in [1,100]:inter.add(target)
   clauses+=1+int(trigger>1 or stop>0)
  else:clauses+=1
 activepost=post[:1] if bands[0]>=999 else post[:2] if bands[1]>=999 else post
 for band in bands:
  if 0<band<999:shell.add(band)
 for cut,target in activepost:
  if cut not in [0,100]:chance.add(cut)
  if cut>0 and target not in [1,100]:inter.add(target)
 clauses+=len(activepost)
 if boundary==-1 and early[:2]==[1,0] and all(row==early[2:] for row in activepost) and bands[0]>=999:clauses-=1
 if len(v)>19 and v[19]>0:chance.add(v[19]);memory=1
 B=2 if v[17]==2 else 1;clauses+=B
 vector=[P,len(shell),len(chance),len(inter),clauses,memory,0,B];C=4*P+2*len(shell)+len(chance)+2*len(inter)+clauses+2*memory+B
 if P<=1 and len(shell)<=1 and len(chance)<=1 and len(inter)==0 and memory==0:tier=1
 elif P<=1 and len(shell)<=2 and len(chance)<=3 and len(inter)<=1:tier=2
 elif P<=2 and len(shell)<=3 and len(chance)<=4 and len(inter)<=3:tier=3
 else:tier=4
 if boundary==-2:clauses=len(routines)+len(activepost)+B+len({a[0] for a in routines if a[0]<=999})
 vector=[P,len(shell),len(chance),len(inter),clauses,memory,0,B];C=4*P+2*len(shell)+len(chance)+2*len(inter)+clauses+2*memory+B
 compact=clauses<=8 and len(inter)<=4
 return vector,C,tier,compact

def cases():
 out=[]
 for region in ['PAL','NTSC-U']:
  for variant in VARIANTS:
   d=json.loads((F/f'{region}_{variant}_optimal_exact.json').read_text());out.append(dict(id=f'{region}:route:{variant}',scenario_class='route',region=region,route=variant,base=20,rate=300,entry=15,optimum_seconds=d['expected_seconds']))
  for b,r,i in [(15,300,15),(25,300,15),(20,250,15),(20,350,15)]+([(20,300,12),(20,300,18)] if region=='PAL' else []):
   d=json.loads((F/f'{region}_reference_optimal_tol1e-06_b{b}_r{r}_i{i}_exact.json').read_text());out.append(dict(id=f'{region}:timing:b{b}:r{r}:i{i}',scenario_class='timing',region=region,route='reference',base=b,rate=r,entry=i,optimum_seconds=d['expected_seconds']))
 assert len(out)==26 and len({x['id'] for x in out})==26;return out
CASES=cases()  # Imports must not rewrite frozen release metadata.

def generate():
 rng=random.Random(SEED);seen=set();out=[]
 def add(v,family):
  key=tuple(v)
  if key in seen or len(out)>=LIMIT:return
  vector,C,tier,compact=features(v)
  if not compact or vector[2]>4:return
  seen.add(key);out.append(dict(id=len(out),family=family,parameters=v,features=vector,complexity=C,tier=tier,compact=compact,status='generated'))
 # Exhaustive displayed threshold 0..100 at each stateless cap cutoff.
 for cutoff in range(101):
  for reserve in [0,700,800,900,950]:add(policy(early=(reserve+1,reserve,cutoff,100),post=((cutoff,100),)*3),'universal')
 for reserve in [0,700,800,900,950]:add(policy(early=(reserve+1,reserve,100,100),post=((100,100),)*3),'universal')
 pools={}
 pools['two_phase']=[policy(early=(g,stop,t0,100),post=((t1,100),)*3,restock=r,partial=p) for g,stop,t0,t1,r,p in itertools.product([1,701,801,901,951],[0,300,600,800],[0,20,50,80,100],[0,5,9,10,15,20,27,100],[0,1,2],[0,1]) if stop<g]
 pools['cap_pressure']=[policy(early=(g,stop,t0,100),post=((t1,100),)*3,restock=r) for g,stop,t0,t1,r in itertools.product([700,800,850,900,950],[0,100,300,500,700,800],[0,80,100],[0,5,9,10,15,20,27],[0,1,2]) if stop<g]
 pools['inventory']=[policy(early=(g,stop,80,100),bands=(band,1000),post=((t,lo),(t,hi),(t,hi)),restock=r,partial=p) for g,stop,band,t,lo,hi,r,p in itertools.product([700,800,900],[0,300,600],[100,300,500,700],[5,9,10,15,20],[40,60,80,100,-10,-30,-50],[60,80,100,-30,-50,-80],[0,1,2],[0,1]) if stop<g]
 pools['intermediate_table']=[policy(early=(g,stop,100,100),bands=(b1,b2),post=((t0,lo),(t1,mid),(t2,hi)),restock=r) for g,stop,b1,b2,t0,t1,t2,lo,mid,hi,r in itertools.product([800,900],[0,300],[100,200],[500,700],[5,9,10],[9,15],[15,20],[40,-30],[60,80],[100,-80],[0,1])]
 pools['story_phase']=[policy(boundary=boundary,early=(g,stop,t0,100),late=(g,0,t1,100),post=((t2,100),)*3,restock=r,partial=p) for boundary,g,stop,t0,t1,t2,r,p in itertools.product([3,4,6],[700,800,900],[0,100,300,600],[0,80,100],[0,15,20,40,80,100],[5,9,10,15,20],[0,1,2],[0,1]) if stop<g]
 for family,pool in pools.items():
  rng.shuffle(pool);before=len(out)
  for v in pool:
   add(v,family)
   if len(out)-before>=600:break
 return out

def textrows(candidates,path):path.write_text(''.join(' '.join(map(str,[p['id'],*p['parameters']]))+'\n' for p in candidates))
def screen(candidates,suffix):
 txt=W/f'candidates_{suffix}.txt';textrows(candidates,txt)
 def run(job):
  region,variant=job;output=W/f'{region}_{variant}_screen_{suffix}.jsonl'
  subprocess.run([str(BIN/'screen'),str(txt),str(F/'route_inputs'/f'{region}_{variant}.route'),region,str(output),'512',str(SEED)],check=True)
  return region,variant,{d['id']:d for d in map(json.loads,output.read_text().splitlines())}
 with cf.ThreadPoolExecutor(max_workers=2) as ex:parts=list(ex.map(run,[(r,v) for r in ['PAL','NTSC-U'] for v in VARIANTS]))
 return {(r,v):d for r,v,d in parts}

def scores(candidates,data):
 critical=float(t.ppf(1-.01/(2*LIMIT*26),511));rows={}
 for region in ['PAL','NTSC-U']:
  regioncases=[c for c in CASES if c['region']==region]
  for p in candidates:
   metrics=[]
   for c in regioncases:
    z=data[region,c['route']][p['id']];coeff=np.array([c['base'],1/c['entry'],1200/c['rate'],1]);mu=float(np.dot(coeff,z['cost_mean']));se=math.sqrt(max(0,float(coeff@np.array(z['cost_cov']).reshape(4,4)@coeff))/512);opt=c['optimum_seconds'];metrics.append(((mu-opt)/opt,(mu-critical*se-opt)/opt,(mu+critical*se-opt)/opt))
   rows[region,p['id']]=dict(point=max(x[0] for x in metrics),lower=max(x[1] for x in metrics),upper=max(x[2] for x in metrics),mean=sum(x[0] for x in metrics)/len(metrics))
 return rows,critical

def retain(candidates,rows,region):
 # No deterministic dominance claim is made here. Confidence-compatible and best-in-band are protected.
 byC={};keep=set()
 for p in candidates:byC.setdefault(p['complexity'],[]).append(p)
 for group in byC.values():keep.update(p['id'] for p in sorted(group,key=lambda p:rows[region,p['id']]['point'])[:3])
 for tier in range(1,5):keep.update(p['id'] for p in sorted([p for p in candidates if p['tier']==tier],key=lambda p:rows[region,p['id']]['point'])[:6])
 for p in candidates:
  bound=min(rows[region,q['id']]['upper'] for q in candidates if q['complexity']<=p['complexity'])
  if rows[region,p['id']]['lower']<=bound:keep.add(p['id'])
 return keep

if __name__=='__main__':
 (OUT/'scenarios.json').write_text(json.dumps(CASES,indent=2))
 candidates=generate();print('Generated',len(candidates),'coarse candidates',flush=True);data=screen(candidates,'coarse');rows,critical=scores(candidates,data)
 # Nominal best-32 beams by region plus one representative from each complexity band seed refinement.
 beam=set()
 for region in ['PAL','NTSC-U']:
  beam.update(p['id'] for p in sorted(candidates,key=lambda p:rows[region,p['id']]['point'])[:BEAM])
  for C in sorted({p['complexity'] for p in candidates}):beam.add(min((p for p in candidates if p['complexity']==C),key=lambda p:rows[region,p['id']]['point'])['id'])
 seen={tuple(p['parameters']) for p in candidates};fine=[]
 for id in sorted(beam):
  p=candidates[id]
  for index in [3,7,11,13,15,1,2,5,6,9,10]:
   for delta in ([-2,-1,1,2] if index in [3,7,11,13,15] else [-20,-10,10,20]):
    v=p['parameters'].copy();v[index]+=delta
    if index in [3,7,11,13,15] and not 0<=v[index]<=100:continue
    if index not in [3,7,11,13,15] and not 0<=v[index]<=1000:continue
    if v[1]<=v[2] or v[5]<=v[6] or v[9]>v[10]:continue
    if tuple(v) in seen:continue
    vector,C,tier,compact=features(v)
    if not compact or vector[2]>4:continue
    if len(candidates)+len(fine)>=LIMIT:break
    seen.add(tuple(v));fine.append(dict(id=len(candidates)+len(fine),family=p['family']+'_refined',parameters=v,features=vector,complexity=C,tier=tier,compact=compact,status='generated'))
 if fine:
  print('Generated',len(fine),'integer/ten-shell refinements',flush=True);new=screen(fine,'fine')
  for k in data:data[k].update(new[k])
  candidates+=fine;rows,critical=scores(candidates,data)
 protected={r:retain(candidates,rows,r) for r in ['PAL','NTSC-U']}
 for p in candidates:
  p['regions']={r:dict(screen=rows[r,p['id']],status='retained_for_exact' if p['id'] in protected[r] else 'not_retained_after_screening') for r in protected}
 (OUT/'candidates.json').write_text(json.dumps(candidates,indent=2));(OUT/'screening_configuration.json').write_text(json.dumps(dict(seed=SEED,runs=512,limit=LIMIT,nominal_beam=BEAM,simultaneous_family_confidence=.99,student_t_critical=critical,interval_assumption='Studentized normal approximation; not a distribution-free bound. Protected best three per complexity and six per tier.',protected_counts={r:len(v) for r,v in protected.items()},generated=len(candidates)),indent=2))
 textrows(candidates,OUT/'candidates.txt')
 print('Retained', {r:len(v) for r,v in protected.items()},flush=True)
