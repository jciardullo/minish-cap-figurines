# Supplemental revision change log

All raw decimal values below come from saved floating-point outputs, before display rounding. They are not exact-arithmetic certificates. Original model, routes, thresholds, candidate IDs, 10,000-candidate list and predeclared chord rule are unchanged.

## Task 1 — knee-selection margin

- PAL: historical endpoints `{'C_min': 7, 'C_max': 40, 'R_min': 0.08136229798066436, 'R_max': 1.8436255106008994}`; selected `6457`, actual runner-up `6729`, margin `0.005529024705698438`. All interior normalized coordinates and scores are in `knee_margins.json`.
- Expanded PAL: endpoint values `{'C_min': 7, 'C_max': 40, 'R_max': 1.8436255106008994, 'R_min': 0.08136229798066436}`; knee `6457`, runner-up `6729`, margin `0.005529024705698438`.
- NTSC-U: historical endpoints `{'C_min': 7, 'C_max': 37, 'R_min': 0.0755675174556701, 'R_max': 1.2472173264083333}`; selected `6098`, actual runner-up `6729`, margin `0.013122031146139246`. All interior normalized coordinates and scores are in `knee_margins.json`.
- Expanded NTSC-U: endpoint values `{'C_min': 7, 'C_max': 39, 'R_max': 1.2472173264083333, 'R_min': 0.07473861652355979}`; knee `6098`, runner-up `6729`, margin `0.0145692301470009`.
Both knees remain unchanged. Two of sixteen bounded weight/duplicate perturbations still change each regional knee. Supplemental 10000 is contextual, not the runner-up; its minimum-needed variant differs below evaluation tolerance.

## Task 2 — low-complexity audit

The literal integer parser is unbounded; finite enumeration is over the canonical legal behavioral quotient of the implemented rules. The complete grammar, domains, aliases, extensional deduplication definition and exhaustive partition argument are in `grammar.json`.

Exhaustive coverage: C≤8. Raw canonical templates generated: 214; invalid: 0; behaviorally distinct: 214; regional records evaluated: 428. Partition: C7=4 and C8=210. Raw aliases are removed analytically, so 214 is not a count of every redundant serialized tuple.

A legal C15 subfamily alone has exactly 497503 inventory pairs ×4 early/post action pairs ×2 restock modes =3980024 policies, requiring 7960048 regional records. Full C≤15 evaluation is infeasible within this local revision. It is not replaced with a heuristic. C9..15 results remain non-exhaustive: 217 original PAL and165 original US records through15. The combined low-complexity frontiers are saved separately.

The minimum remains ID500. No original frozen frontier point is newly dominated. Supplemental ID14203 is about6.8e-7 seconds faster than ID10000 in PAL: their apparent floating-point ordering is an unresolved numerical near-tie, not a certified unique optimum.

## Task 3 — bounded higher-complexity extension

Bounds were recorded before evaluation: 12 clauses, intermediate displayed40/60/80 or fixed30, 40 single-row/one-band mutations per regional seed; no adaptive expansion or screening. Generated80, rejected0, after behavioral deduplication62 regional policies, deterministically evaluated62. Winning mutations themselves fit the old Tier4 eight-clause limit; generated rules use at most9 clauses. This is a bounded local extension, not an exhaustive test of all12-clause rules.

- PAL: best supplemental `{'id': 12003, 'complexity': 42, 'features': [4, 4, 4, 1, 8, 1, 0, 2], 'reference_seconds': 7323.133774058953, 'mean_regret': 0.03416814262442895, 'worst_regret': 0.08145581450907413, 'improvement_percentage_points': -0.009351652840977609, 'reference_time_saving_seconds': -0.679186009417208, 'clause_count': 8, 'fits_original_Tier4_limits': True}`.
- NTSC-U: best supplemental `{'id': 13011, 'complexity': 39, 'features': [4, 3, 3, 1, 8, 1, 0, 2], 'reference_seconds': 6909.334438042883, 'mean_regret': 0.03638915981076092, 'worst_regret': 0.07473861652355979, 'improvement_percentage_points': 0.0828900932110313, 'reference_time_saving_seconds': 8.020253872184185, 'clause_count': 8, 'fits_original_Tier4_limits': True}`.
PAL has no improvement. US shows a small descending tail (0.0828900932110313 percentage points), not evidence of global flattening. ID13011 adds a remembered fixed30 wager during Water-to-Wind. It is not adopted: the lower-complexity original compact remains the default recommendation. Original selected IDs and result records are historical and preserved. The expanded US frontier and plot include the new C39 endpoint.

Compute: initial C7/Tier5 batch `{'wall_seconds': 31.054938542001764, 'child_user_seconds': 57.948566, 'child_system_seconds': 2.143313, 'child_peak_rss_bytes': 109248512, 'peak_rss_units': 'bytes on macOS; maximum single child, not aggregate', 'new_policy_region_records': 70, 'route_evaluation_upper_bound': 560, 'environment': {'platform': 'macOS-27.0.1-arm64-arm-64bit-Mach-O', 'machine': 'arm64', 'logical_cpus': 10, 'python': '3.14.0', 'parallel_workers': 2, 'evaluator': 'clang++ C++17 O2, frozen exact.cpp/policy.hpp floating-point forward occupancy'}}`; C8 batch `{'wall_seconds': 71.5301404999991, 'child_user_seconds': 127.414294, 'child_system_seconds': 7.153947, 'child_peak_rss_bytes': 47923200, 'policy_region_records': 420}`. Combined child CPU=194.66012 seconds. Peak is maximum single-child RSS, not aggregate memory. Cache reuse was allowed; counts refer to evaluated records, not necessarily fresh process invocations. The throughput projection of 36.60014878320484 CPU-days for the C15 subfamily is illustrative, not a runtime lower bound.

## Task 4 — information benchmark

A concrete legal-state observation quotient counterexample is saved in `information_state_counterexample.json`: identical (F80,S500,R0,U106,Water-but-not-Wind) observations lead to700 versus900 shells on progression in two frozen routes. The observation is not Markov when route/history is hidden. No ordinary Bellman recursion on that observation is used.

A belief-state problem is formulated but not solved. Instead, a restricted, well-defined ex-ante fixed-policy benchmark is computed across every deterministically evaluated original/supplemental observable policy. Primary prior is synthetic uniform1/8 over routes; sensitivity prior is synthetic reference1/2 and each other route1/14. Neither is an empirical player-route frequency.

- PAL, uniform: selected fixed-rule benchmark ID12011; B=7311.039265251361s; future-informed mean A=7038.018359502765s.
- PAL, reference_heavy: selected fixed-rule benchmark ID12011; B=7305.746706909252s; future-informed mean A=7092.225035353149s.
- NTSC-U, uniform: selected fixed-rule benchmark ID13011; B=6932.199145935943s; future-informed mean A=6660.938937773736s.
- NTSC-U, reference_heavy: selected fixed-rule benchmark ID13011; B=6922.399985410346s; future-informed mean A=6706.229828396532s.
`restricted_information_benchmark.json` reports knee/compact/helper means, route gaps, and additive second-based components for both priors. B−A combines information and restricted-family/search loss; it is not identified pure value of information. T−B is not pure simplification loss against a full route-blind optimum. The helper has extra owned-count information and can have negative residuals relative to this restricted human class. No percentages with different denominators are added, and5% is not retested as a fair matched-information threshold.

## Task 5 — presentation

ID10000 is added to Tables4/5 as an audit baseline and fully described as waiting for eligibility before one-shell pulls. The guide adds the same baseline, compact entry flow and spoiler-light eligibility checklist.

- PAL: underlying guide comparison `{'baseline_seconds': 10420.414287586897, 'compact_seconds': 7322.454588049536, 'knee_seconds': 7806.504299415238, 'compact_saving_vs_baseline_minutes': 51.632661658956, 'compact_saving_vs_knee_minutes': 8.067495189428367}`.
- NTSC-U: underlying guide comparison `{'baseline_seconds': 10420.414288009877, 'compact_seconds': 6917.354691915068, 'knee_seconds': 7351.998769178564, 'compact_saving_vs_baseline_minutes': 58.384326601580156, 'compact_saving_vs_knee_minutes': 7.2440679543916}`.
Consultation time remains unmeasured. All player thresholds and actions are unchanged.

## Task 6 — boundary and diagnostic target

The paper and guide state that the original compact lies at the original family boundary. The narrow extension does not prove flattening. No original or supplemental evaluated human rule reaches5% under the future-informed denominator; that value remains a predeclared diagnostic, not a matched-information fairness criterion.

## Task 7 — reproducibility/consistency

The supplemental tests check all490 regional records,214 low-complexity definitions, caps/conservation/completion, unchanged timing-policy transitions, feature vectors, both knees, additive gap identities, original headlines and frozen list hash. Existing C++ boundary checks still cover all four selected rules, including800000 compact entry cases. Raw original evaluation data and human-policy implementation are preserved. Tables and new outputs are generated from JSON. No public repository URL, DOI, release or archival ID is assigned.

## Unresolved / not claimed

- Exhaustive C9..15 grammar coverage: infeasible local combinatorial workload; only bounded original results remain.
- Complete12-clause search: not attempted; extension is specifically bounded to80 mutations.
- Full belief-state matched-information optimum and pure value-of-information/simplification decomposition: not computed. Current solver does not implement observation-history belief updates.
- Directed-rounding enclosure and sub-microsecond near-tie resolution: unavailable; floating-point validation does not certify these decimal differences.
- New Monte Carlo validation for supplemental policies: not run; original selected-policy simulation evidence remains preserved.

## Final status

**Knees:** unchanged6457/6098, including expanded-frontier recomputation. **Compact recommendations:** unchanged8911/8560. **Recommended headline times/regrets:** unchanged. **Empirical frontier:** expanded US endpoint ID13011 atC39 and7.473861652355979% worst regret; PAL C8 restock variants are unresolved numerical near-ties. **Frozen original candidate list/hash:** unchanged.

Original candidate SHA256: `edcd4d1118de22cefa0d248020469064b06188cc34cdbea57967e58766163730`.

## Reproducible commands

From the project root with C++17, Python/NumPy/SciPy and Matplotlib installed:
```sh
python3 outputs/distillation/supplemental/run_audits.py
python3 outputs/distillation/supplemental/run_C8.py
python3 outputs/distillation/supplemental/analyze.py
python3 outputs/distillation/supplemental/test_revision.py
python3 outputs/distillation/supplemental/plot.py
```
The publication-edit script is a one-time source patch, not an idempotent analysis step; do not rerun it over already-revised prose. Compile the saved LaTeX source normally.
