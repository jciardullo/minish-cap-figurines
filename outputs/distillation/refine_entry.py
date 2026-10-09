import json
from pathlib import Path
from search import *
candidates=json.loads((OUT/'candidates.json').read_text());seedparents=set()
for region in ['PAL','NTSC-U']:
 seedparents.update(p['id'] for p in sorted(candidates,key=lambda p:p['regions'][region]['screen']['point'])[:32])
 for family in ['universal','two_phase','cap_pressure','inventory','intermediate_table','story_phase']:
  group=[p for p in candidates if p['family'].startswith(family)];seedparents.update(p['id'] for p in sorted(group,key=lambda p:p['regions'][region]['screen']['point'])[:12])
 for C in sorted({p['complexity'] for p in candidates}):seedparents.add(min((p for p in candidates if p['complexity']==C),key=lambda p:p['regions'][region]['screen']['point'])['id'])
seen={tuple(p['parameters']+[0]) for p in candidates};fresh=[]
for id in sorted(seedparents):
 for cutoff in [5,10,15,20,25,30,40,50,60,80]:
  v=candidates[id]['parameters']+[cutoff]
  if tuple(v) in seen:continue
  vec,C,tier,compact=features(v)
  if not compact or vec[2]>4:continue
  seen.add(tuple(v));fresh.append(dict(id=len(candidates)+len(fresh),family=candidates[id]['family']+'_entry_chance',parameters=v,features=vec,complexity=C,tier=tier,compact=compact,status='generated'))
assert len(candidates)+len(fresh)<=LIMIT
print('Entry-chance variants',len(fresh),flush=True);new=screen(fresh,'entry');newrows,critical=scores(fresh,new)
for p in fresh:p['regions']={r:dict(screen=newrows[r,p['id']],status='screened') for r in ['PAL','NTSC-U']}
candidates+=fresh;rows={(r,p['id']):p['regions'][r]['screen'] for r in ['PAL','NTSC-U'] for p in candidates}
protected={r:retain(candidates,rows,r) for r in ['PAL','NTSC-U']}
for p in candidates:
 for r in protected:p['regions'][r]['status']='retained_for_exact' if p['id'] in protected[r] else 'not_retained_after_screening'
(OUT/'candidates.json').write_text(json.dumps(candidates,indent=2));textrows(candidates,OUT/'candidates.txt');cfg=json.loads((OUT/'screening_configuration.json').read_text());cfg.update(generated=len(candidates),protected_counts={r:len(v) for r,v in protected.items()},entry_threshold_refinement='Observable chance on arrival, retained session activation; seeded from best 32, family leaders, and each complexity band.');(OUT/'screening_configuration.json').write_text(json.dumps(cfg,indent=2));print('Retained',cfg['protected_counts'],flush=True)
