import itertools,random,json
from search import *
candidates=json.loads((OUT/'candidates.json').read_text());pool=[]
for gate,fort,water,windreserve,entrycut,windcut,postcut,target,restock in itertools.product([700,800,900],[100,150,300],[600,700,800],[0,100],[10,15,20],[15,20,25],[8,9,10],[60,100],[0,2]):
 v=policy(boundary=-2,early=(gate,600,80,100),late=(gate,windreserve,windcut,100),post=((postcut,target),)*3,restock=restock,partial=1)+[entrycut,gate,fort,100,100,gate,water,100,100];pool.append(v)
rng=random.Random(SEED+1);rng.shuffle(pool);fresh=[];seen={tuple(p['parameters']) for p in candidates}
def add(v,family):
 if tuple(v) in seen or len(candidates)+len(fresh)>=LIMIT:return
 vec,C,tier,compact=features(v)
 if not compact or vec[2]>4:return
 seen.add(tuple(v));fresh.append(dict(id=len(candidates)+len(fresh),family=family,parameters=v,features=vec,complexity=C,tier=tier,compact=compact,status='generated'))
for v in pool:
 add(v,'compact_story_table')
 if len(fresh)>=1000:break
parents=set()
for r in ['PAL','NTSC-U']:
 parents.update(p['id'] for p in sorted(candidates,key=lambda p:p['regions'][r]['screen']['point'])[:32])
for id in sorted(parents):
 for ix in [3,7,11,19,1,2,5,6]:
  v0=candidates[id]['parameters']
  if ix>=len(v0):continue
  for delta in ([-2,-1,1,2] if ix in [3,7,11,19] else [-20,-10,10,20]):
   v=v0.copy();v[ix]+=delta
   if not 0<=v[ix]<=(100 if ix in [3,7,11,19] else 1000):continue
   if v[1]<=v[2] or v[5]<=v[6]:continue
   add(v,candidates[id]['family']+'_last_refinement')
print('Last bounded candidates',len(fresh),flush=True);new=screen(fresh,'compact');newrows,critical=scores(fresh,new)
for p in fresh:p['regions']={r:dict(screen=newrows[r,p['id']],status='screened') for r in ['PAL','NTSC-U']}
candidates+=fresh;rows={(r,p['id']):p['regions'][r]['screen'] for r in ['PAL','NTSC-U'] for p in candidates};protected={r:retain(candidates,rows,r) for r in ['PAL','NTSC-U']}
for p in candidates:
 for r in protected:p['regions'][r]['status']='retained_for_exact' if p['id'] in protected[r] else 'not_retained_after_screening'
(OUT/'candidates.json').write_text(json.dumps(candidates,indent=2));textrows(candidates,OUT/'candidates.txt');cfg=json.loads((OUT/'screening_configuration.json').read_text());cfg.update(generated=len(candidates),protected_counts={r:len(v) for r,v in protected.items()},compact_table_refinement='Four recognizable phases, seven/eight rows maximum. Seeded grid, no new mechanics/route changes.');(OUT/'screening_configuration.json').write_text(json.dumps(cfg,indent=2));print('Retained',cfg['protected_counts'],flush=True)
