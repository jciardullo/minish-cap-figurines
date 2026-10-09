"""Continue the bounded, predeclared validation matrix after baseline results exist."""
import concurrent.futures as cf,subprocess,time,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'outputs/funded';W=ROOT/'work/funded';BIN=ROOT/'work/corrected'
variants=['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late','missed_postgame']
profiles=['reference','earlier','missed_postgame','cap_reference','mid_reference','halfmid_reference','halfcap_reference']
def practical(job):
 r,v,p=job;tag=f'{r}_{v}_observable_{p}'
 mode='halfcap' if p.startswith('halfcap_') else 'halfmid' if p.startswith('halfmid_') else 'mid' if p.startswith('mid_') else 'observable';source=p.removeprefix('cap_').removeprefix('mid_').removeprefix('halfmid_').removeprefix('halfcap_')
 spec=f'{mode}:{W}/{r}_{source}_optimal|{W}/{r}_fusion_early_optimal'
 if p.startswith(('cap_','mid_','halfmid_','halfcap_')):spec+=f'|{W}/{r}_missed_postgame_optimal'
 out=O/(tag+'_exact.json');subprocess.run([str(BIN/'evaluate_exact'),str(W/f'{r}_{v}.route'),spec,r,str(out)],check=True)
 d=json.loads(out.read_text());opt=json.loads((O/f'{r}_{v}_optimal_exact.json').read_text())['expected_seconds'];d.update(region=r,route=v,optimum_seconds=opt,regret_seconds=d['expected_seconds']-opt,regret_percent=100*(d['expected_seconds']-opt)/opt);out.write_text(json.dumps(d,indent=2));return d
with cf.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(practical,[(r,v,p) for r in ['PAL','NTSC-U'] for v in variants for p in profiles]))
print('Observable profile evaluations complete.',flush=True)
