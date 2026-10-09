"""Derived supplemental values; no search or simulation in this analysis."""
import json,sys,csv,math,hashlib
from pathlib import Path
D=Path(__file__).resolve().parents[1];S=D/'supplemental';sys.path.insert(0,str(D))
from frontier import frontier,knee,robustness
from complexity_audit import audit
A=json.loads((D/'endpoint_audit.json').read_text());defs=json.loads((S/'candidate_definitions.json').read_text());C8=json.loads((S/'C8_definitions.json').read_text());catalog={p['id']:p for p in json.loads((D/'candidates.json').read_text())};catalog[10000]=A['policy']
for p in defs['low']+C8:catalog[p['id']]=p
for r,ps in defs['tier5'].items():
 for p in ps:catalog[p['id']]=p
summary={};allrows={};export=[]
for r,compactid in [('PAL',8911),('NTSC-U',8560)]:
 original=[json.loads(p.read_text()) for p in (D/'exact').glob(r+'_*.json') if json.loads(p.read_text()).get('valid',True)];supp=[json.loads(p.read_text()) for p in (S/'evaluations').glob(r+'_*.json')];rows=original+[A['regions'][r]['evaluation']]+supp;allrows[r]=rows
 historical=next(p for p in original if p['id']==compactid);t5=[p for p in supp if 12000<=p['id']<14000];best=min(t5,key=lambda p:(p['worst_regret'],p['complexity'],p['mean_regret'],p['id']));expanded=frontier(rows);(S/(r+'_expanded_frontier.json')).write_text(json.dumps(expanded,indent=2)+'\n')
 low=[p for p in rows if p['complexity']<=15];lf=frontier(low);(S/(r+'_low_complexity_frontier.json')).write_text(json.dumps(lf,indent=2)+'\n');k,geometry,exists=knee(rows)
 geom={p['id']:p for p in geometry};eligible=sorted((p for p in expanded[1:-1] if geom[p['id']]['signed_distance']>0),key=lambda p:-geom[p['id']]['signed_distance']);runner=eligible[1]
 basef=json.loads((D/(r+'_frontier.json')).read_text());dominated=[p['id'] for p in basef if any(q['complexity']<=p['complexity'] and q['worst_regret']<=p['worst_regret']+1e-10 and (q['complexity']<p['complexity'] or q['worst_regret']<p['worst_regret']-1e-10) for q in expanded)]
 ref=lambda p:next(c for c in p['cases'] if c['scenario']==r+':route:reference')
 summary[r]=dict(tier5_best=dict(id=best['id'],complexity=best['complexity'],features=best['features'],reference_seconds=ref(best)['seconds'],mean_regret=best['mean_regret'],worst_regret=best['worst_regret'],improvement_percentage_points=100*(historical['worst_regret']-best['worst_regret']),reference_time_saving_seconds=ref(historical)['seconds']-ref(best)['seconds'],clause_count=best['features'][4],fits_original_Tier4_limits=best['compact']),historical_compact=dict(id=compactid,worst_regret=historical['worst_regret']),expanded_knee=k['id'],expanded_knee_geometry=geometry,expanded_runner_up=runner['id'],expanded_knee_margin=geom[k['id']]['signed_distance']-geom[runner['id']]['signed_distance'],expanded_endpoints=dict(C_min=expanded[0]['complexity'],C_max=expanded[-1]['complexity'],R_max=expanded[0]['worst_regret'],R_min=expanded[-1]['worst_regret']),original_frontier_points_newly_dominated=dominated,original_evaluated_C15_records=sum(p['complexity']<=15 for p in original),low_frontier_ids=[p['id'] for p in lf],extended_stability=robustness(rows,catalog))
 for p in supp:
  rr=ref(p);export.append(dict(region=r,id=p['id'],complexity=p['complexity'],features=json.dumps(p['features']),reference_seconds=rr['seconds'],reference_minutes=rr['seconds']/60,mean_regret=p['mean_regret'],worst_regret=p['worst_regret']))
(S/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
with (S/'evaluation_summary.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(export[0]));w.writeheader();w.writerows(export)
# Restricted ex-ante route-blind policy class, synthetic priors (not real player frequencies).
priors=json.loads((S/'synthetic_prior_definition.json').read_text());helper=list(csv.DictReader((D/'software_helper_benchmark.csv').open()));matched={}
for r,compactid,kneeid in [('PAL',8911,6457),('NTSC-U',8560,6098)]:
 routecases=lambda p:{c['scenario'].split(':route:')[1]:c for c in p['cases'] if ':route:' in c['scenario']}
 results={}
 for label,prior in priors['priors'].items():
  average=lambda p:sum(prior[v]*c['seconds'] for v,c in routecases(p).items())
  best=min(allrows[r],key=lambda p:(average(p),p['complexity'],p['id']));bm=average(best);star=sum(prior[v]*c['optimum_seconds'] for v,c in routecases(best).items());reported={}
  for name,id in [('knee',kneeid),('compact',compactid),('audit_baseline',10000)]:
   p=next(p for p in allrows[r] if p['id']==id);cc=routecases(p);tm=average(p);gaps=[c['seconds']-c['optimum_seconds'] for c in cc.values()]
   reported[name]=dict(id=id,prior_mean_seconds=tm,prior_mean_future_informed_gap_seconds=tm-star,equal_weight_mean_route_gap_seconds=sum(gaps)/8,worst_route_gap_seconds=max(gaps),restricted_benchmark_minus_future_informed_seconds=bm-star,policy_minus_restricted_benchmark_seconds=tm-bm,identity_residual_seconds=(tm-star)-((bm-star)+(tm-bm)))
  hh=[x for x in helper if x['region']==r and ':route:' in x['scenario']];ht=sum(prior[x['scenario'].split(':route:')[1]]*float(x['seconds']) for x in hh);g=[float(x['regret_seconds']) for x in hh]
  reported['software_helper']=dict(prior_mean_seconds=ht,prior_mean_future_informed_gap_seconds=ht-star,equal_weight_mean_route_gap_seconds=sum(g)/8,worst_route_gap_seconds=max(g),restricted_benchmark_minus_future_informed_seconds=bm-star,policy_minus_restricted_benchmark_seconds=ht-bm,identity_residual_seconds=(ht-star)-((bm-star)+(ht-bm)),information='Additional owned-count lookup; outside restricted human rule class')
  results[label]=dict(best_tested_restricted_policy=best['id'],best_tested_restricted_mean_seconds=bm,future_informed_mean_seconds=star,policies=reported)
 matched[r]=results
(S/'restricted_information_benchmark.json').write_text(json.dumps(matched,indent=2)+'\n')
# Exact counts of a legal injective C15 subfamily; calibrated time projections, not actual exhaustive run times.
ng=sum(g-2 for g in range(3,1000));subfamily=ng*4*2
cpu=sum(json.loads((S/p).read_text())['child_user_seconds']+json.loads((S/p).read_text())['child_system_seconds'] for p in ['compute_resources.json','C8_compute_resources.json']);nrecords=70+420
counts=dict(exhaustive_maximum_complexity=8,canonical_definitions_raw_generated=214,rejected_invalid=0,behaviorally_unique=214,regional_evaluations=428,partition={'C7':4,'C8':210},C15_subfamily_inventory_pairs=ng,C15_subfamily_unique_policies=subfamily,C15_subfamily_regional_policy_evaluations=2*subfamily,measured_audit_cpu_seconds=cpu,measured_regional_records=nrecords,calibrated_subfamily_cpu_days=(2*subfamily)*(cpu/nrecords)/86400,projection_qualification='Illustrative projection from measured C7/C8/Tier5 throughput; not a lower bound or guaranteed runtime. Complete C15 space is larger. Serialized alias tuples are analytically quotiented before these raw canonical-template counts. C9..15 results are non-exhaustive original bounded evaluations.',conclusion='Complete C<=15 enumeration is infeasible in this bounded local revision; no heuristic replacement. C<=8 enumerated exhaustively in canonical minimum-scored behavioral grammar.')
(S/'enumeration_counts.json').write_text(json.dumps(counts,indent=2)+'\n')
# Every guide comparison calculated from underlying seconds, not rounded display values.
g={}
for r,compactid,kneeid in [('PAL',8911,6457),('NTSC-U',8560,6098)]:
 ref=lambda id:next(c['seconds'] for p in allrows[r] if p['id']==id for c in p['cases'] if c['scenario']==r+':route:reference')
 g[r]=dict(baseline_seconds=ref(10000),compact_seconds=ref(compactid),knee_seconds=ref(kneeid),compact_saving_vs_baseline_minutes=(ref(10000)-ref(compactid))/60,compact_saving_vs_knee_minutes=(ref(kneeid)-ref(compactid))/60)
(S/'guide_comparisons.json').write_text(json.dumps(g,indent=2)+'\n')
print(json.dumps({'summary':{r:{k:v for k,v in x.items() if k not in ['extended_stability','expanded_knee_geometry']} for r,x in summary.items()},'counts':counts,'guide':g},indent=2))
