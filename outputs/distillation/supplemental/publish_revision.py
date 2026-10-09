import json,re
from pathlib import Path
D=Path(__file__).resolve().parents[1];S=D/'supplemental';p=D/'paper.tex';s=p.read_text();summary=json.loads((S/'summary.json').read_text());margins=json.loads((S/'knee_margins.json').read_text());counts=json.loads((S/'enumeration_counts.json').read_text());matched=json.loads((S/'restricted_information_benchmark.json').read_text());A=json.loads((D/'endpoint_audit.json').read_text());guide=json.loads((S/'guide_comparisons.json').read_text())
def table(headers,rows,fmt,caption,label):
 return '\\begin{table}[H]\\centering\\small\n\\begin{tabular}{'+fmt+'}\\toprule\n'+' & '.join(headers)+'\\\\\\midrule\n'+'\n'.join(' & '.join(map(str,row))+'\\\\' for row in rows)+'\n\\bottomrule\\end{tabular}\n\\caption{'+caption+'}\\label{'+label+'}\\end{table}\n'
# Add baseline beside original named selections.
for r in ['PAL','NTSC-U']:
 d=A['regions'][r];e=d['evaluation'];old=f'{r} & compact & '+('8911 & 40 & 122.04 & 3.41 & 8.14' if r=='PAL' else '8560 & 37 & 115.29 & 3.72 & 7.56')+'\\\\'
 new=old+'\n'+f'{r} & audit baseline & 10000 & 8 & {d["reference_minutes"]:.2f} & {100*e["mean_regret"]:.2f} & {100*e["worst_regret"]:.2f}'+'\\\\'
 s=s.replace(old,new,1)
 old=f'{r} & compact & '+('(4, 4, 4, 0, 8, 1, 0, 2)' if r=='PAL' else '(4, 3, 3, 0, 8, 1, 0, 2)')+'\\\\'
 s=s.replace(old,old+'\n'+f'{r} & audit baseline & (1, 0, 0, 0, 3, 0, 0, 1)'+'\\\\',1)
s=s.replace('The official knee criterion and selections are unchanged;', 'The official knee criterion and memorized selections are unchanged;')
s=s.replace('It adds the PAL $C=8$ frontier point and dominates the former $C=8$ and $C=9$ points; it is dominated in US.', 'It added the PAL $C=8$ frontier point and dominated the former $C=8$ and $C=9$ points; it is dominated in US. The subsequent exhaustive $C\\le8$ audit finds minimum-needed restocking (ID 14203) about $6.8\\times10^{-7}$ seconds faster in PAL. This sub-microsecond floating-point difference is below the evaluation tolerance and is not a certified or practically meaningful dominance claim; both are retained as an unresolved numerical near-tie.')
# Latest expanded frontier shown, with historical compact still highlighted.
old='(36,8.085787) (37,7.556752)';new=old+' (39,7.473862)';assert s.count(old)==2;s=s.replace(old,new)
s=s.replace('NTSC-U empirical frontier, including the minimal-policy endpoint.', 'NTSC-U empirical frontier with the supplemental $C=39$ endpoint; the original compact at $C=37$ is retained.')
s=s.replace('Endpoint normalization still uses the full frontier, not this cropped view.', 'Endpoint normalization uses the full frontier, not this cropped view. The supplemental US $C=39$ point is included; the red triangle remains the recommended historical compact.')
block='''\n% BEGIN SUPPLEMENTAL REVISION
\\subsection{Knee-selection margins}
The historical frontier (including audit ID 10000) uses PAL endpoints $(C_{\\min},C_{\\max},R_{\\max},R_{\\min})=(7,40,1.8436255106008994,0.08136229798066436)$ and US $(7,37,1.2472173264083333,0.0755675174556701)$. Regrets here are fractions. The actual runner-up in both regions is ID 6729, not ID 10000. Full unrounded machine outputs accompany this paper.
'''
rows=[]
for r in ['PAL','NTSC-U']:
 for q in margins[r]['ranked_interior'][:3]+([next(q for q in margins[r]['ranked_interior'] if q['id']==10000)] if r=='PAL' else []):
  rows.append([r,q['id'],q['complexity'],f'{q["normalized_C"]:.9f}',f'{q["normalized_R"]:.9f}',f'{q["signed_score"]:.9f}'])
block+=table(['Region','ID','C','$\\widetilde C$','$\\widetilde R$','$d$'],rows,'llrrrr','Historical-frontier knee scores near the maximum; ID 10000 included for context','tab:knee-margins')
block+=f'Historical margins are {margins["PAL"]["margin"]:.12f} PAL and {margins["NTSC-U"]["margin"]:.12f} US. The expanded US frontier changes its high-complexity endpoint to $(C_{{\\max}},R_{{\\min}})=(39,{summary["NTSC-U"]["expanded_endpoints"]["R_min"]:.17g})$. Its knee/runner-up scores become '+f'{next(q["signed_distance"] for q in summary["NTSC-U"]["expanded_knee_geometry"] if q["id"]==6098):.12f} / {next(q["signed_distance"] for q in summary["NTSC-U"]["expanded_knee_geometry"] if q["id"]==6729):.12f}, margin {summary["NTSC-U"]["expanded_knee_margin"]:.12f}; PAL is unchanged. Both knees remain selected. These nonzero geometric margins coexist with the bounded sensitivity result: two of sixteen weight/duplicate perturbations change each regional knee, also after the supplemental extension. A geometric margin does not remove dependence on the chosen complexity weights.\n'
block+='''\\subsection{Supplemental low-complexity grammar audit}
The machine-readable grammar is the interpreter in \\texttt{policy.hpp}: one early row, a Fortress/Water/Wind split, or four story rows; each row has an inclusive shell/chance entry gate, reserve stop, strict chance threshold and displayed-target or fixed-shell action. Three postgame inventory bands share the same action form. The active flag persists only within a visit. An unaffordable early wager either ends the visit or spends all shells; postgame shortage instead invokes the chosen maximum-batch, minimum-needed, or already-affordable-first restocking rule. Version branches are only the verified price, batch limit and timing. No event, future-resource, owned-count or RNG input is introduced.
The canonical legal domains are shell gates/reserves 1--1000/0--999, chance thresholds 0--100, displayed targets 1--100, fixed wagers 1--100 (negative encoding), and the three restocking modes. Boundary aliases, inactive fields, identical adjacent rows, absent bands, one-shell aliases and probability-cap aliases are quotiented before evaluation. The C++ parser accepts redundant arbitrary integers; this audit concerns canonical legal behavior, not infinitely many serialized aliases. The complete grammar, domains, normalization and scripts are published in \\texttt{supplemental/grammar.json}.
Every minimum-scored representative has $P\\ge1$, $L\\ge2$, $B\\ge1$, hence $C\\ge7$. Through $C=8$, inventory thresholds, intermediate values, extra progression boundaries and session gates cannot fit. The exhaustive partition is four $C=7$ classes; at $C=8$, 198 shared-chance-threshold classes, four different constant early/postgame rules, four no-early rules, two meaningful partial-guarantee rules, and two funded-first universal rules. All 214 canonical templates are valid and distinct; no template is rejected. Their 428 regional records evaluate every applicable route/timing case. Counts exclude redundant raw aliases analytically rather than sampling them.
At $C=15$, even the subfamily $3\\le g\\le999$, $1\\le r\\le g-2$, two early constant wagers, two postgame constants and two restocking modes contains
\\[
 8\\sum_{g=3}^{999}(g-2)=3{,}980{,}024
\\]
distinct policies, each with vector $(1,2,0,0,4,1,0,1)$. Thus full enumeration through 15 is infeasible within this local revision. The highest genuinely exhaustive boundary is 8; results above it remain non-exhaustive. No heuristic search is substituted for the requested exhaustive audit. Original evaluated records through 15 number 217 PAL and 165 US; these supplement, rather than complete, the higher-complexity coverage.
'''
rows=[]
for r in ['PAL','NTSC-U']:
 for q in json.loads((S/(r+'_low_complexity_frontier.json')).read_text()):rows.append([r,q['id'],q['complexity'],f'{100*q["worst_regret"]:.6f}'])
block+=table(['Region','ID','C','Worst R\\%'],rows,'llrr','Supplemental combined low-complexity frontier; exhaustive only through 8, bounded tested results at 9--15','tab:low-frontier')
block+='''ID 500 remains the minimum endpoint; no original frozen frontier point is newly dominated. ID 10000 and minimum-needed ID 14203 differ below a microsecond and are treated as an uncertified numerical near-tie, even though the mechanical floating-point frontier orders them. The supplemental audit does not change either knee or any historical named selection.
\\subsection{Bounded supplemental Tier-5 extension}
Before evaluation, the extension was limited to 12 printed clauses, four intermediate values (displayed 40/60/80 or fixed 30), and the current observable interface. It generates 40 single-row/one-inventory-band variants of each regional compact seed, without adaptive screening. After inactive-target/behavior normalization, 31 unique policies per region remain; zero are invalid. All 62 regional records receive deterministic evaluation. This is a local bounded extension, not an exhaustive Tier-5 search. Generated rules actually use at most nine clauses; both winning mutations still fit the original eight-clause Tier-4 limit.
'''
rows=[]
for r in ['PAL','NTSC-U']:
 b=summary[r]['tier5_best'];rows.append([r,b['id'],b['complexity'],f'{100*b["worst_regret"]:.6f}',f'{b["improvement_percentage_points"]:.6f}',f'{b["reference_time_saving_seconds"]:.6f}'])
block+=table(['Region','ID','C','Worst R\\%','Gain pp','Ref. saved s'],rows,'llrrrr','Best supplemental mutation versus the original regional compact; negative gain means worse','tab:tier5')
block+='PAL ID 12003 has vector $(4,4,4,1,8,1,0,2)$; US ID 13011 has $(4,3,3,1,8,1,0,2)$. US ID 13011 changes only the Water-to-Wind wager to a fixed 30 shells, clamped at displayed 100\\%; all other compact rules remain the same. The small US reduction is not adopted as a new recommendation: it costs an additional remembered intermediate wager for about eight reference-route seconds. Original compact IDs 8911/8560 and their headline times/regrets remain the recommended and historical selections. The tested local frontier shows no PAL improvement and a slowly declining US tail; this cannot prove global flattening. The compact selections lie at the boundary of the original tested family, and their regrets alone are not evidence of a flattened human-policy frontier.\n'
rc=json.loads((S/'compute_resources.json').read_text());r8=json.loads((S/'C8_compute_resources.json').read_text())
block+=f'The audit ran on macOS arm64 with ten logical CPUs, two evaluator workers, Python 3.14 and Apple clang 21 C++17/O2. The initial $C=7$/Tier-5 batch used {rc["wall_seconds"]:.6f} seconds wall time and {rc["child_user_seconds"]+rc["child_system_seconds"]:.6f} child CPU seconds; the $C=8$ batch used {r8["wall_seconds"]:.6f} / {r8["child_user_seconds"]+r8["child_system_seconds"]:.6f} seconds. Maximum single-child resident memory was {max(rc["child_peak_rss_bytes"],r8["child_peak_rss_bytes"]):,} bytes; it is not aggregate peak memory. Cache reuse is allowed and recorded numerical outputs are delivered. The measured throughput projects about {counts["calibrated_subfamily_cpu_days"]:.2f} CPU-days for the $C=15$ subfamily alone; this is an illustrative projection, not a rigorous runtime lower bound. No new Monte Carlo samples or directed-rounding certificates were generated for these supplemental policies.\n'
block+='''\\subsection{Information matching and restricted ex-ante benchmark}
Hiding route identity does not make $(F,S,R,U,\\text{story flags})$ Markov. At the legal controlled state $(80,500,0,106)$ with Water acquired but Wind not acquired, the reference next receipt is 200 shells while the earlier-sidequest receipt is 400: advancing gives 700 versus 900 shells. The current observation does not determine the future transition. This is a state-space counterexample, not a measured causal-history distribution.
A correct partially observed formulation uses belief $\\beta$ over route, latent event/history and any other unobserved state. With observation likelihood $O$, a finite-prior update would be
\\[
\\beta'(z')\\propto O(o'\\mid z',a)\\sum_z P(z'\\mid z,a)\\beta(z),
\\quad V(\\beta)=\\min_a\\{c(\\beta,a)+\\mathbb E[V(\\beta')]\\}.
\\]
That full belief-state problem is not solved here: observation/history kernels and their memory requirements are not implemented in the current full-information solver. No ordinary Bellman recursion is applied to a non-Markov observation.
Instead, a well-defined restricted ex-ante benchmark selects the lowest prior-mean time among already deterministically evaluated fixed observable rules, including the supplemental rules. Its information is exactly the human interpreter plus its within-visit flag, without $F$, route identity or future receipts. The primary synthetic analysis prior is uniform over eight routes; the sensitivity prior assigns reference probability $1/2$ and $1/14$ to each other route. These are not empirical player-route probabilities. The software helper has extra owned-count information and is reported separately, not added to this restricted class.
'''
rows=[]
for r in ['PAL','NTSC-U']:
 for prior,label in [('uniform','uniform'),('reference_heavy','ref.-heavy')]:
  q=matched[r][prior];rows.append([r,label,q['best_tested_restricted_policy'],f'{q["best_tested_restricted_mean_seconds"]:.6f}',f'{q["future_informed_mean_seconds"]:.6f}'])
block+=table(['Region','Synthetic prior','ID','Restricted B s','Future-informed A s'],rows,'llrrr','Best tested restricted ex-ante rule; not a route-blind POMDP optimum','tab:synthetic-benchmark')
rows=[]
for r in ['PAL','NTSC-U']:
 for name in ['knee','compact','software_helper']:
  q=matched[r]['uniform']['policies'][name];rows.append([r,name.replace('_',' '),f'{q["prior_mean_seconds"]:.3f}',f'{q["equal_weight_mean_route_gap_seconds"]:.3f}',f'{q["worst_route_gap_seconds"]:.3f}',f'{q["restricted_benchmark_minus_future_informed_seconds"]:.3f}',f'{q["policy_minus_restricted_benchmark_seconds"]:.3f}'])
block+=table(['Region','Rule','Mean T s','Mean gap s','Worst gap s','B-A s','T-B s'],rows,'llrrrrr','Uniform synthetic-prior time gaps; the two final columns add to the mean gap','tab:synthetic-gaps')
block+='''The identity $T-A=(B-A)+(T-B)$ is algebraic, with all terms in seconds. Here $B-A$ combines information loss with restricted-family/search loss; it is not identified pure value of information. Likewise $T-B$ is relative to this tested class, not pure simplification loss against a route-blind optimum. Negative helper residuals are expected because the helper has extra information and is outside the class. Full sensitivity-prior means, worst route gaps and additive checks are in the machine-readable output. No percentages with different denominators are added. No fair matched-information 5\\% test is claimed: 5\\% remains the predeclared diagnostic target under the future-informed denominator.
% END SUPPLEMENTAL REVISION
'''
s=s.replace('\\section{Robustness and Sensitivity}',block+'\n\\section{Robustness and Sensitivity}',1)
s=s.replace('A matched-information benchmark is possible future work, not part of this revision.','A full belief-state matched-information optimum remains future work; the supplemental restricted ex-ante comparison does not identify pure value of information.')
s=s.replace('a matched-information benchmark is possible future work, not part of this revision.','a full belief-state matched-information optimum remains future work, while the supplemental restricted ex-ante comparison does not identify pure value of information.')
s=s.replace('The bounded candidate search cannot prove global optimality over all human strategies.', 'The bounded candidate search cannot prove global optimality over all human strategies. Exhaustive supplemental coverage ends at complexity 8; complexity 9--15 and the Tier-5 neighborhood remain incomplete. The 5\\% level is a predeclared diagnostic under the future-informed denominator, not a fair matched-information threshold.')
s=s.replace('Neither compact policy meets the 5\\% target,','The supplemental US rule reaches 7.47\\% worst regret at $C=39$, but the existing compact recommendation is retained for its lower memory burden; neither knee changes. Neither recommended compact policy meets the 5\\% diagnostic target,')
s=s.replace('No human policy assessed by deterministic forward occupancy evaluation in the bounded tested candidate set attained 5\\% worst-tested regret.', 'No human policy assessed by deterministic forward occupancy evaluation in the original bounded set or these supplemental audits attained the future-informed 5\\% diagnostic. The supplemental US endpoint reaches 7.47\\% at $C=39$; the lower-complexity original compact remains recommended.')
p.write_text(s);(D/'paper_template.tex').write_text(s)
# Guide: retain all existing actionable policy rows.
p=D/'player_strategy.md';g=p.read_text()
insert='''\n**Spoiler-light full-eligibility checklist:**

- Ending completed.
- Completionist Kinstone fusions/rewards capable of unlocking figurines completed.
- Remaining optional progression and side content capable of unlocking figurines completed.
- Gallery-dependent rewards excluded from this check.

There is no direct full-pool indicator; this is not an exhaustive walkthrough.
'''
g=g.replace('## Recommended one-page strategy: compact table',insert+'\n## Recommended one-page strategy: compact table',1)
flow='''\n**Entry flow (read at an ordinary visit):**

1. All figurines eligible? **Yes:** use the final row. **No:** continue below.
2. Regional shell threshold met (700 PAL / 800 NTSC-U)? If no, continue progression.
3. Default one-shell chance at least 20%? If no, continue progression.
4. Shells strictly above this phase’s reserve? If no, continue progression.
5. If all three early-entry tests pass, start and follow the current phase row. After each completed pull, stop before another pull once shells are at or below reserve.
'''
g=g.replace('**Table legend:**',flow+'\n**Table legend:**',1)
baseline=f'''\n**Do-nothing-clever baseline:** wait until all figurines are eligible, then always wager 1 shell and restock as needed. Supplemental audit ID 10000 takes **{guide['PAL']['baseline_seconds']/60:.2f} modeled minutes PAL / {guide['NTSC-U']['baseline_seconds']/60:.2f} NTSC-U** on the reference route. The recommended compact saves **{guide['PAL']['compact_saving_vs_baseline_minutes']:.2f} / {guide['NTSC-U']['compact_saving_vs_baseline_minutes']:.2f} minutes**, respectively. This is an observable model baseline, distinct from the future-informed one-shell benchmark. Consultation time is unmeasured.

**Supplemental check:** a bounded extension found an NTSC-U variant at **7.47%** worst-tested regret, remembering one additional fixed wager (complexity 39 versus 37). Its reference gain is only **{summary['NTSC-U']['tier5_best']['reference_time_saving_seconds']:.2f} seconds**, so the simpler compact table above remains recommended. No PAL improvement was found. This small neighborhood does not prove the human-policy frontier has flattened.

The **5%** figure remains a predeclared diagnostic against a future-informed optimum, not a fair matched-information threshold. No policy in the original bounded set or supplemental evaluations met it; this says nothing about every conceivable human rule.
'''
g=g.replace('## What the simplification costs','## What the simplification costs\n'+baseline,1);p.write_text(g)
print('Paper and guide revised from authoritative machine-readable supplemental outputs.')
