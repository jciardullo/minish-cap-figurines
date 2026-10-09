"""Independent finite toy SSP: policy iteration versus LP and exhaustive Bellman actions."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
states=[(j,f,s,r) for j in [0,1] for f in range((1 if j==0 else 2)+1) for s in range(5) for r in range((3 if j==0 else 5)+1)]
index={x:i for i,x in enumerate(states)};actions=[]
for j,f,s,r in states:
 u=1 if j==0 else 2;w=3 if j==0 else 5;row=[]
 if f==2:row=[('terminal',0,[])]
 else:
  if j==0:row.append(('advance',0,[(1,index[(1,f,min(4,s+3),r)])]))
  if f<u:
   b=max(1,100*(u-f)//u)
   for wager in range(1,min(s,101-b)+1):
    p=max(15,b+wager-1)/100
    row.append((f'pull {wager}',2+(wager-1)/15,[(p,index[(j,f+1,s-wager,r)]),(1-p,index[(j,f,s-wager,min(w,r+1))])]))
  if s+2<=4:
   n=0
   while True:
    rr=min(w,r+2*n)
    if rr>=3:row.append((f'buy n={n}',3+n,[(1,index[(j,f,s+2,rr-3)])]))
    if rr==w:break
    n+=1
 assert row;actions.append(row)
size=len(states)
A=[];rhs=[]
for i,row in enumerate(actions):
 for name,c,edges in row:
  v=np.zeros(size);v[i]=1
  for p,dest in edges:v[dest]-=p
  A.append(v);rhs.append(c)
lp=linprog(-np.ones(size),A_ub=np.array(A),b_ub=np.array(rhs),bounds=[(0,None)]*size,method='highs');assert lp.success,lp.message
# Exhaustively compare all actions at every state for each horizon/value-iteration step.
v=np.zeros(size)
for vi in range(10000):
 nv=np.array([min(c+sum(p*v[d] for p,d in edges) for _,c,edges in row) for row in actions])
 if max(abs(nv-v))<1e-12:v=nv;break
 v=nv
else:raise AssertionError('VI convergence')
policy=[]
for i,(j,f,s,r) in enumerate(states):
 if f==2:choice=0
 elif j==0:choice=0
 elif s:choice=next(a for a,item in enumerate(actions[i]) if item[0]=='pull 1')
 else:choice=next(a for a,item in enumerate(actions[i]) if item[0].startswith('buy'))
 policy.append(choice)
for pi in range(100):
 M=np.eye(size);c=np.zeros(size)
 for i,a in enumerate(policy):
  _,c[i],edges=actions[i][a]
  for p,dest in edges:M[i,dest]-=p
 value=np.linalg.solve(M,c)
 changes=0
 for i,row in enumerate(actions):
  q=[c+sum(p*value[d] for p,d in edges) for _,c,edges in row];a=int(np.argmin(q))
  if q[a]<value[i]-1e-11:policy[i]=a;changes+=1
 if not changes:break
else:raise AssertionError('PI convergence')
assert max(abs(value-lp.x))<1e-8
assert max(abs(value-v))<1e-8
residual=max(abs(value[i]-min(c+sum(p*value[d] for p,d in edges) for _,c,edges in row)) for i,row in enumerate(actions))
assert residual<1e-10
result=dict(states=size,actions=sum(map(len,actions)),policy_iterations=pi+1,value_iterations=vi+1,lp_policy_max_difference=float(max(abs(value-lp.x))),value_iteration_max_difference=float(max(abs(value-v))),bellman_residual=float(residual),initial_seconds=float(value[index[(0,0,3,0)]]))
Path(__file__).with_name('reduced_validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
