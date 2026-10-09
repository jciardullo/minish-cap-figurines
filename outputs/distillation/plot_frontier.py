from pathlib import Path
import json
O=Path("outputs/distillation")
selected=json.loads((O/"selections.json").read_text())
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for ax,r in zip(axs,['PAL','NTSC-U']):
 f=json.loads((O/(r+'_frontier.json')).read_text());ax.plot([p['complexity'] for p in f],[100*p['worst_regret'] for p in f],'o-',color='#176f66');k=next(p for p in f if p['id']==selected[r]['knee']);ax.scatter([k['complexity']],[100*k['worst_regret']],s=90,color='#cd7420',zorder=5,label='Official knee');ax.axhline(5,color='#777',linestyle=':',label='5% target');ax.set(xlabel='Per-player complexity',ylabel='Worst tested regret (%)',title=r);ax.grid(alpha=.2);ax.legend()
fig.savefig(O/'pareto.png',dpi=180);fig.savefig(O/'pareto.svg');plt.close(fig)
