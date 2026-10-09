"""Count the actual printed human concepts/clauses, not unused interpreter parameters."""
import json
from pathlib import Path
from search import *

def normalize(parameters):
 v=parameters.copy()
 if len(v)==19:v.append(0)
 for ix in [3,7,11,13,15]+([22,26] if v[0]==-2 else []):
  if v[ix]==0 or v[ix+1] in [1,-1]:v[ix:ix+2]=[0,100]
 if v[0]!=-2 and v[1:5]==v[5:9]:v[0]=-1
 if v[0]==-1:v[5:9]=v[1:5]
 return v

def audit(parameters):
 v=normalize(parameters);normal=[v[1:5]] if v[0]==-1 else [v[1:5],v[5:9]] if v[0]!=-2 else [v[1:5],v[20:24],v[24:28],v[5:9]]
 # Adjacent identical story rows need no remembered boundary.
 routines=[normal[0]]
 for r in normal[1:]:
  if r!=routines[-1]:routines.append(r)
 P=len(routines);shell=set();chance=set();inter=set();M=0;gates=set()
 for trigger,stop,cut,target in routines:
  if trigger>999:continue
  if stop>0:shell.add(stop)
  if trigger!=stop+1:shell.add(trigger);M=1
  if trigger>1 or v[19]>0:gates.add(trigger)
  if cut not in [0,100]:chance.add(cut)
  if cut>0 and target not in [1,100]:inter.add(target)
 if v[19]>0:chance.add(v[19]);M=1
 bandlimits=v[9:11];rows=[v[11:13],v[13:15],v[15:17]]
 active=[rows[0]] if bandlimits[0]>=999 else rows[:2] if bandlimits[1]>=999 else rows
 post=[active[0]]
 for ix,r in enumerate(active[1:]):
  if r!=post[-1]:shell.add(bandlimits[ix]);post.append(r)
 for cut,target in post:
  if cut not in [0,100]:chance.add(cut)
  if cut>0 and target not in [1,100]:inter.add(target)
 partial=bool(v[18] and any(cut>0 and target not in [1,-1] for cut,target in ([r[2:] for r in routines if r[0]<=999]+post)))
 B=2 if v[17]==2 else 1
 L=len(routines)+len(post)+len(gates)+1+int(partial)
 universal=len(routines)==1 and routines[0][0:2]==[1,0] and not gates and len(post)==1 and post[0]==routines[0][2:]
 if universal:L-=1
 vec=[P,len(shell),len(chance),len(inter),L,M,0,B];C=sum(a*b for a,b in zip(vec,[4,2,1,2,1,2,0,1]))
 tier1=P<=1 and len(shell)<=1 and len(chance)<=1 and not inter and M==0 and len(post)==1 and post[0]==routines[0][2:] and not partial
 tier2=P<=1 and len(shell)<=2 and len(chance)<=3 and len(inter)<=1
 tier3=P<=2 and len(shell)<=3 and len(chance)<=4 and len(inter)<=3
 compact=L<=8 and len(inter)<=4
 tier=1 if tier1 else 2 if tier2 else 3 if tier3 else 4
 valid=tier<=3 or compact
 return vec,C,tier,compact,valid

if __name__=='__main__':
 candidates=json.loads((OUT/'candidates.json').read_text());changes=0
 for p in candidates:
  if 'generation_features' not in p:p['generation_features']=p['features'];p['generation_complexity']=p['complexity']
  vec,C,tier,compact,valid=audit(p['parameters']);changes+=C!=p['complexity'];p.update(features=vec,complexity=C,tier=tier,compact=compact,valid=valid)
 (OUT/'candidates.json').write_text(json.dumps(candidates,indent=2))
 for path in (OUT/'exact').glob('*.json'):
  d=json.loads(path.read_text());p=candidates[d['id']];d.update(features=p['features'],complexity=p['complexity'],tier=p['tier'],compact=p['compact'],valid=p['valid']);path.write_text(json.dumps(d,indent=2))
 (OUT/'complexity_audit.json').write_text(json.dumps(dict(changed_scores=changes,convention='Count a shared entry gate once, each distinct story/postgame decision row, the shortage fallback when partial wagers matter, and one conditional restocking clause. B separately counts its branches. Zero shells and pool exhaustion are mandatory feasibility endpoints, not learned numeric thresholds. Inactive values/identical adjacent rules are removed.',generated_candidates=len(candidates),invalid_tier_limits=sum(not p['valid'] for p in candidates)),indent=2));print(changes,'scores corrected',sum(not p['valid'] for p in candidates),'outside tier constraints')
