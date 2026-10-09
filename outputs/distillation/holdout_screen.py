"""Fresh CRN screening after freezing the adaptively generated candidate list."""
import json,hashlib
from search import *
import search
candidates=json.loads((OUT/'candidates.json').read_text());search.SEED=20261110
print('Frozen-list holdout screen',len(candidates),flush=True);data=screen(candidates,'holdout');rows,critical=scores(candidates,data);protected={r:retain(candidates,rows,r) for r in ['PAL','NTSC-U']}
for p in candidates:
 for r in protected:p['regions'][r]=dict(screen=rows[r,p['id']],status='retained_for_exact' if p['id'] in protected[r] else 'not_retained_after_screening')
(OUT/'holdout_candidates.json').write_text(json.dumps(candidates,indent=2));cfg=json.loads((OUT/'screening_configuration.json').read_text());cfg.update(selection_seed=20261110,selection_list_frozen_before_sampling=True,candidate_list_sha256=hashlib.sha256((OUT/'candidates.txt').read_bytes()).hexdigest(),holdout_protected_counts={r:len(v) for r,v in protected.items()},training_seed=SEED);(OUT/'screening_configuration.json').write_text(json.dumps(cfg,indent=2));print('Holdout retained',cfg['holdout_protected_counts'],flush=True)
