"""Fresh 20,000-run distributions, plus separately labeled incidental-cash checks."""
import concurrent.futures as cf,json,subprocess
from search import *
s=json.loads((OUT/'selections.json').read_text());candidates=json.loads((OUT/'candidates.json').read_text());(OUT/'validation').mkdir(exist_ok=True);(OUT/'selected_policies').mkdir(exist_ok=True)
for region,sel in s.items():
 for role in ['minimal','knee','compact']:textrows([candidates[sel[role]]],OUT/'selected_policies'/f'{region}_{role}.txt')
def sim(job):
 region,role,variant,seed=job;policyfile=OUT/'selected_policies'/f'{region}_{role}.txt';file=OUT/'validation'/f'{region}_{role}_{variant}.jsonl';subprocess.run([str(BIN/'screen'),str(policyfile),str(F/'route_inputs'/f'{region}_{variant}.route'),region,str(file),'20000',str(seed)],check=True);d=json.loads(file.read_text());exact=json.loads((OUT/'exact'/f'{region}_{s[region][role]}.json').read_text());target=next(x['seconds'] for x in exact['cases'] if x['scenario']==f'{region}:route:{variant}');d.update(region=region,role=role,route=variant,exact_seconds=target,ci_contains_exact=d['ci95_mean_low']<=target<=d['ci95_mean_high']);file.with_suffix('.json').write_text(json.dumps(d,indent=2));return d
jobs=[(r,role,v,20261120+regionix*100+roleix*10+routeix) for regionix,r in enumerate(['PAL','NTSC-U']) for roleix,role in enumerate(['minimal','knee','compact']) for routeix,v in enumerate(VARIANTS)]
with cf.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(sim,jobs))
(OUT/'validation_summary.json').write_text(json.dumps(rows,indent=2));print('48 fresh 20,000-run distributions complete',flush=True)
extras=[]
for region in ['PAL','NTSC-U']:
 for role in ['knee','compact']:
  baseline=json.loads((OUT/'exact'/f'{region}_{s[region][role]}.json').read_text())['cases'][0]['seconds']
  for cash in [300,600,900]:
   file=OUT/'validation'/f'{region}_{role}_outside_cash{cash}.json';subprocess.run([str(BIN/'exact'),str(OUT/'selected_policies'/f'{region}_{role}.txt'),str(F/'route_inputs'/f'{region}_reference.route'),region,str(file),str(cash)],check=True);d=json.loads(file.read_text());d.update(region=region,role=role,cash_offer=cash,baseline_seconds=baseline,savings_seconds=baseline-d['expected_seconds'],comparison='Same fixed policy, supplemental cash; no regret against unequal zero-cash resources.');extras.append(d)
(OUT/'incidental_cash.json').write_text(json.dumps(extras,indent=2));print('Supplemental cash checks complete',flush=True)
