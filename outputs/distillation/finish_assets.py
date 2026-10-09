import csv,json,sys,hashlib,collections
from pathlib import Path
O=Path('outputs/distillation');W=Path('work/distillation');sys.path.insert(0,str(O))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# Standalone scientific plots.
fig,axs=plt.subplots(1,2,figsize=(10,4),layout='constrained')
s=json.loads((O/'selections.json').read_text())
for ax,r in zip(axs,['PAL','NTSC-U']):
 f=json.loads((O/(r+'_frontier.json')).read_text());ax.plot([p['complexity'] for p in f],[100*p['worst_regret'] for p in f],'o-',color='#176f66')
 k=next(p for p in f if p['id']==s[r]['knee']);ax.scatter([k['complexity']],[100*k['worst_regret']],s=90,color='#cd7420',zorder=5,label='Official knee');ax.axhline(5,color='#777',linestyle=':',label='5% target');ax.set(xlabel='Per-player complexity',ylabel='Worst tested regret (%)',title=r);ax.grid(alpha=.2);ax.legend()
fig.savefig(O/'pareto.png',dpi=180);fig.savefig(O/'pareto.svg');plt.close(fig)
# Helper cases: retain software benchmark, owned-count lookup explicitly outside human policies.
sc=json.loads((O/'scenarios.json').read_text());helpers=[]
for c in sc:
 r=c['region']
 if c['scenario_class']=='route':d=json.loads(Path(f"outputs/funded/{r}_{c['route']}_observable_reference_exact.json").read_text());t=d['expected_seconds']
 else:
  matches=[x for x in csv.DictReader(open('outputs/funded/observable_timing_sensitivity.csv')) if x['region']==r and x['policy']=='reference' and float(x['pull_base_seconds'])==c['base'] and float(x['farming_rupees_per_minute'])==c['rate'] and float(x['entry_inputs_per_second'])==c['entry']];assert len(matches)==1;t=float(matches[0]['practical_seconds'])
 helpers.append(dict(scenario=c['id'],region=r,seconds=t,optimum_seconds=c['optimum_seconds'],regret_seconds=t-c['optimum_seconds'],regret_percent=100*(t-c['optimum_seconds'])/c['optimum_seconds']))
with (O/'software_helper_benchmark.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(helpers[0]));w.writeheader();w.writerows(helpers)
# Extend generated paper with preserved comparisons/convergence.
paper=(O/'paper.tex').read_text()
from publish import table,esc
# publish import regenerated original; restore after.
for r in ['PAL','NTSC-U']:
 a=[h for h in helpers if h['region']==r];paper=paper.replace('The software helper remains outside this frontier.',f"The fixed software-helper benchmark has worst-tested regret {max(h['regret_percent'] for h in a):.2f}\\% for {r}. It uses an owned-count lookup and cannot qualify as a human rule. The software helper remains outside this frontier.",1)
bench=list(csv.DictReader(open('outputs/funded/regional_benchmarks.csv')))
add=table(['Region','Threshold','Minutes','Shells','Pulls','Trips'],[[b['region'],b['policy'].replace('threshold',''),f"{float(b['expected_seconds'])/60:.2f}",f"{float(b['used']):.1f}",f"{float(b['pulls']):.1f}",f"{float(b['trips']):.2f}"] for b in bench if b['policy'] in ['threshold9','threshold10','threshold27']],'llrrrr')
paper=paper.replace('Threshold benchmark progression/restocking',add+'Threshold benchmark progression/restocking')
conv=list(csv.DictReader(open('outputs/funded/route_convergence.csv')));rows=[]
for r in ['PAL','NTSC-U']:
 for phase,label in [(3,'Fortress'),(4,'Water'),(6,'Wind'),(7,'Sidequests'),(8,'Full pool')]:
  a=[x for x in conv if x['region']==r and int(x['phase'])==phase and x['same_available_pool']=='True'];rows.append([r,label,len(a),f"{max(float(x['max_value_difference']) for x in a):.2f}",f"{100*sum(int(x['representative_action_disagreements']) for x in a)/sum(int(x['matched_sample_states']) for x in a):.2f}"])
convtext='''The preserved matched-state convergence audit compares route-specific mathematical selectors on sampled equal-pool states. It does not show monotone convergence before the last milestone: future-resource timing continues to matter. At full eligibility, the common future-free subproblem agrees exactly at matched shells/cash/owned count, while different arrival inventories still change whole-run time. Representative-selector disagreements can include ties; they are not proofs of disjoint optimal action sets.
'''+table(['Region','Milestone','Routes','Max value gap s','Different selectors \\%'],rows,'llrrr')
paper=paper.replace('Exact phase-by-phase optimizer convergence is not independently certified by this distillation stage. Prior phase tables and the present route outcomes identify the remaining resource effects.',convtext)
paper=paper.replace('Remaining records are explicitly marked not retained after screening.','Records never receiving deterministic forward evaluation are explicitly marked not retained after screening; an older receiving deterministic forward evaluation record remains eligible even if a later screening step would remove it.')
paper=paper.replace('The full vector $(P,S,Q,I,L,M,D,B)$ is published.','The full vector $(P,S,Q,I,L,M,D,B)$ is published. Here $P$ counts remembered progression boundaries, $S$ distinct inventory thresholds, $Q$ distinct displayed-chance thresholds, $I$ distinct intermediate wagers/targets, $L$ decision clauses, $M$ persistent session flags, $D$ explicit differences in a combined regional guide, and $B$ distinct restocking branches. Individual scores omit $D$ because a player learns only one version.')
if 'Player Result: recommended one-page strategy' not in (O/'paper.tex').read_text(): (O/'paper.tex').write_text(paper) # Preserve current editorial revisions.
# Bibliography source companion, inline bibliography retained for standalone built-in compiler.
(O/'references.bib').write_text('''@misc{device, author={zeldaret}, title={The Minish Cap decompilation: figurineDevice.c}, year={2026}, url={https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c}, note={Pinned revision 6fb6dfb4a7efbe24d0fd1dda5097af6131faacde}}
@misc{eligibility, author={zeldaret}, title={The Minish Cap decompilation: fileselect.c}, url={https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/fileselect.c}}
@misc{prices, author={zeldaret}, title={The Minish Cap decompilation: itemMetaData.c}, url={https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/itemMetaData.c}}
@misc{caps, author={zeldaret}, title={The Minish Cap decompilation: itemUtils.c and gameUtils.c}, url={https://github.com/zeldaret/tmc/tree/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src}}
@misc{route, author={Kirby021591}, title={The Minish Cap walkthrough}, url={https://gamefaqs.gamespot.com/gba/920670-the-legend-of-zelda-the-minish-cap/faqs/34833}}
''')
ids={r:sorted(json.loads(p.read_text())['id'] for p in (O/'exact').glob(r+'_*.json')) for r in ['PAL','NTSC-U']};(O/'exact_evaluated_ids.json').write_text(json.dumps(ids,indent=2))
print('Assets complete')
