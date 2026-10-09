"""Package immutable delivered evidence without ROMs, home caches or old archives."""
import json,csv,hashlib,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'outputs';D=O/'distillation'
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sc=json.loads((D/'scenarios.json').read_text())
for c in sc:
 c['frozen_route_sha256']=(O/'corrected'/f"{c['region']}_{c['route']}.sha256").read_text().strip();c['solver_route_input_sha256']=hashfile(O/'funded/route_inputs'/f"{c['region']}_{c['route']}.route")
(D/'scenarios.json').write_text(json.dumps(sc,indent=2))
with (D/'scenario_definitions.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(sc[0]));w.writeheader();w.writerows(sc)
config=dict(source_revision='6fb6dfb4a7efbe24d0fd1dda5097af6131faacde',candidate_list_sha256=hashfile(D/'candidates.txt'),policy_source_sha256=hashfile(D/'policy.hpp'),exact_evaluator_source_sha256=hashfile(D/'exact.cpp'),simulator_source_sha256=hashfile(D/'screen.cpp'),regions={'PAL':{'price':300,'maximum_bundles':3,'case_count':14},'NTSC-U':{'price':200,'maximum_bundles':4,'case_count':12}},timings={'farming_travel_seconds':45,'already_funded_travel_seconds':20,'bundle_seconds':15,'text':'Fast, B held','NTSC_adjustment_timing':'equal physical +/-1 and +/-10 duration: empirical assumption'},nominal_probabilities='verified formula and hidden floors; IID marginal model conditional on PRNG assumptions',rounding_certificate='not established',selected_policy_hashes={p.name:hashfile(p) for p in (D/'selected_policies').glob('*.txt')},frozen_routes=[dict(scenario=c['id'],ledger_sha256=c['frozen_route_sha256'],input_sha256=c['solver_route_input_sha256']) for c in sc])
(D/'evaluation_provenance.json').write_text(json.dumps(config,indent=2))
v=json.loads((D/'verification.json').read_text());v.update(pdf_visual_qa=v['pdf_visual_qa'],candidate_count=10000,total_scenarios=26,exact_regional_records=2816);(D/'verification.json').write_text(json.dumps(v,indent=2))
files=[]
for directory in ['distillation','corrected','funded','policy_lookup']:
 files.extend(p for p in (O/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.log'] and p.name!='manifest.json')
# Keep search logs intentionally, excluding transient compiler logs.
files.extend(p for p in (D/'search_execution_logs').glob('*.log'))
for name in ['README.md','report.md','gallery_helper.html','gallery_policy.py','build_helper.py','package_policies.py','farming_notes.md','farming_analysis.md','farming_validation.json','late_cleanup_report.md','late_cleanup_README.md','shell_ledger.csv','reference_itinerary.json']:
 p=O/name
 if p.exists():files.append(p)
files=sorted(set(files));manifest=dict(format='sha256',files=[dict(path=str(p.relative_to(R)),sha256=hashfile(p),bytes=p.stat().st_size) for p in files]);(D/'manifest.json').write_text(json.dumps(manifest,indent=2));files.append(D/'manifest.json')
archive=O/'figurine_distillation_bundle.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,p.relative_to(R))
(O/'figurine_distillation_bundle.sha256').write_text(hashfile(archive)+'  '+archive.name+'\n')
print(len(files),'files; bundle bytes',archive.stat().st_size,'sha256',hashfile(archive))
