"""Targeted supplemental audit; no generation, screening, mechanics or optimizer rerun."""
import sys,json,csv,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent
sys.path.insert(0,str(O))
from frontier import frontier,selections,robustness
A=json.loads((O/'endpoint_audit.json').read_text());candidates={p['id']:p for p in json.loads((O/'candidates.json').read_text())}
candidates[10000]=A['policy'];selected={};stability={};overlay={}
for region,d in A['regions'].items():
 rows=[json.loads(p.read_text()) for p in (O/'exact').glob(region+'_*.json') if json.loads(p.read_text()).get('valid',True)]+[d['evaluation']]
 selected[region]=selections(rows);stability[region]=robustness(rows,candidates);f=frontier(rows)
 (O/(region+'_frontier.json')).write_text(json.dumps(f,indent=2))
 overlay[region]={str(r['id']):('exactly_dominated' if any(q['complexity']<=r['complexity'] and q['worst_regret']<=r['worst_regret']+1e-10 and (q['complexity']<r['complexity'] or q['worst_regret']<r['worst_regret']-1e-10) for q in f) else 'exactly_evaluated') for r in rows}
(O/'selections.json').write_text(json.dumps(selected,indent=2));(O/'knee_stability.json').write_text(json.dumps(stability,indent=2))
(O/'endpoint_status_overlay.json').write_text(json.dumps(overlay,indent=2))
import subprocess
subprocess.run([sys.executable,str(O/'plot_frontier.py')],check=True)
# Update only PAL coordinates; endpoints and knee/compact highlights unchanged.
p=O/'paper.tex';s=p.read_text();old='(7,184.362551) (8,77.630346) (9,73.479126) (10,59.629187)';new='(7,184.362551) (8,64.214470) (10,59.629187)';assert s.count(old)==2 or s.count(new)==2;s=s.replace(old,new)
audit='''\\paragraph{Targeted endpoint audit.}
The seemingly simpler rule ``wait for full eligibility, then always wager one shell'' was absent from the frozen list, not screened out. Its early and postgame clauses differ, giving $(P,S,Q,I,L,M,D,B)=(1,0,0,0,3,0,0,1)$ and $C=8$, versus the shared universal wager clause of ID 500 at $C=7$. Supplemental audit ID 10000 uses maximum-bundle restocking and was evaluated deterministically on the existing 26 cases: reference 173.67 minutes in each region, mean regret 47.10\\% PAL / 55.88\\% US, and worst regret 64.21\\% / 71.64\\%. It adds the PAL $C=8$ frontier point and dominates the former $C=8$ and $C=9$ points; it is dominated in US. ID 500 remains the minimum-complexity endpoint. Both endpoint chords and knee IDs 6457/6098 remain unchanged after recomputation, including the bounded weight/duplicate checks. The original 10,000 candidates remain frozen; this is one explicitly separate audit policy, not a new search. Table~\\ref{tab:result-2}'s future-informed one-shell benchmark also rounds to 173.67 minutes, but this numerical agreement does not equate the policies or their information sets. The supplemental rule loses 2592 natural shells to the cap and arrives at full eligibility with 999; its tiny nonzero expected purchases are retained in machine-readable results.
'''
if '\\paragraph{Targeted endpoint audit.}' not in s:s=s.replace('The best minimal rule is the lowest worst regret',audit+'\nThe best minimal rule is the lowest worst regret')
if 'including the supplemental audit, attained' not in s:s=s.replace('at the minimum observed complexity.','at the minimum observed complexity. No human policy assessed by deterministic forward occupancy evaluation in this bounded tested set, including the supplemental audit, attained 5\\% worst-tested regret.',1)
if 'equality is machine-generated' not in s:s=s.replace('Full eligibility removes future-unlock uncertainty,','The identical NTSC-U knee totals for missed\\_late and missed\\_postgame were verified directly in both forward-evaluation and selected-case records; equality is machine-generated, although their different optimizer denominators give different regrets. Full eligibility removes future-unlock uncertainty,')
p.write_text(s);(O/'paper_template.tex').write_text(s)
print('Frontiers repaired; selections',[(r,d['minimal'],d['knee'],d['compact']) for r,d in selected.items()])
