from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=Path(__file__).resolve().parents[1];S=D/'supplemental'
fig,axs=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for ax,r,kid,cid in zip(axs,['PAL','NTSC-U'],[6457,6098],[8911,8560]):
 f=json.loads((S/(r+'_expanded_frontier.json')).read_text());ax.plot([p['complexity'] for p in f],[100*p['worst_regret'] for p in f],'o-',color='#176f66')
 for id,label,color in [(kid,'Memorized knee','#cd7420'),(cid,'Recommended compact','#ad3131')]:
  p=next(x for x in f if x['id']==id);ax.scatter([p['complexity']],[100*p['worst_regret']],s=70,color=color,label=label,zorder=4)
 if r=='NTSC-U':
  p=next(x for x in f if x['id']==13011);ax.scatter([p['complexity']],[100*p['worst_regret']],s=70,marker='^',color='#773c99',label='Supplemental endpoint',zorder=4)
 ax.axhline(5,color='#777',linestyle=':',label='5% diagnostic');ax.set(xlabel='Per-player complexity',ylabel='Worst tested regret (%)',title=r);ax.grid(alpha=.2);ax.legend(fontsize=7)
fig.savefig(D/'pareto.png',dpi=180);fig.savefig(D/'pareto.svg');plt.close(fig)
