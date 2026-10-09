# Current collect-as-you-go numerical results

Use [the report](../report.md) for conclusions and limitations. This directory is the current model: 45 seconds travel for farming cycles, 20 for already-funded shop cycles, 15 per bundle, discrete 20-R farming, three PAL / four NTSC bundles, and no farming before Mole Mitts. Frozen ledgers and current C++ source are in `../corrected/`; older numeric files there retain superseded travel assumptions.

## Reproduction

Requirements: a C++17 compiler, Python 3 with NumPy/SciPy for the reduced verification and minimax profile fit, and the source-only zeldaret/tmc checkout at revision `6fb6dfb4a7efbe24d0fd1dda5097af6131faacde`. No ROM is distributed. Large exact arrays/raw policies require several GB of RAM/disk; postgame caches are exact arrays, not approximations.

From the project root:

```sh
mkdir -p work/corrected work/funded
clang++ -O3 -std=c++17 outputs/corrected/full_solver.cpp -o work/corrected/full_solver
clang++ -O3 -std=c++17 outputs/corrected/evaluate_exact.cpp -o work/corrected/evaluate_exact
clang++ -O3 -std=c++17 outputs/corrected/simulate.cpp -o work/corrected/simulate
clang++ -O3 -std=c++17 outputs/corrected/test_core.cpp -o work/corrected/test_core
work/corrected/test_core
python3 outputs/corrected/validate_reduced.py
python3 outputs/funded/run_scenarios.py
python3 outputs/funded/run_scenarios.py sensitivity
python3 outputs/funded/scan_thresholds.py
python3 outputs/funded/evaluate_profiles.py
python3 outputs/funded/evaluate_simple_rules.py
python3 outputs/funded/minimax_profiles.py
python3 outputs/funded/evaluate_selected.py
python3 outputs/funded/analyze_routes.py
python3 outputs/funded/verify_farming_availability.py
python3 outputs/package_policies.py
python3 outputs/build_helper.py
```

Freeze/rebuild route inputs before solving with `python3 outputs/corrected/freeze_routes.py work/tmc`; compare every `.sha256` and `route_manifest.json`. This is an explicit conditional reference sweep, not an automated proof of every 100% first encounter. Do not alter or reorder route JSON to improve gallery results.

Route text grammar is `U wallet pickup_count quantities... start_at_farm can_farm`. The runner derives `can_farm=0` for opportunities before the completed-Fortress/Mole Mitts milestone, 1 afterward. Frozen JSON hashes are unchanged. The optional flags default to false/true respectively for backward-compatible synthetic tests. Set both explicitly for new tests. `start_at_farm` activates a separately optimized one-off entry decision; subsequent cycles begin at Carlov.

The scenario runner records route hash, region, timing parameters, bundle limit and travel parameters. For a fresh recomputation remove the chosen `work/funded/PREFIX.json` and policies or use a fresh prefix. Completed-policy reuse is intended for resumability, not automatic detection of arbitrary source changes. The pinned-input cache key includes region, timing, threshold family and tolerance; caches are used only at final full-pool states with farming permitted.

## Numerical evidence

- `regional_route_results.csv`: each route/version, resources, farming and ending balances.
- `route_convergence.csv` / `route_sensitivity.json`: matched-state convergence and whole-run spans.
- `*_solve.json`, `*_exact.json`, `*_simulation.json`: Bellman solver, independent occupancy evaluator, Monte Carlo respectively.
- `threshold_scan.csv`, `best_threshold.json`: all threshold candidates considered; certified-dominated entries are not fake solved values.
- `tolerance_validation.json`: 1e-6 vs 1e-7; representative action tables unchanged, some sampled tied sets narrow.
- `farming_availability_validation.json`: 38 initial-policy legality/value checks. Selected policies feasible under the restricted farm availability achieve the relaxed lower bound within 1e-5 seconds. Reference and packaged practical source tables were also re-solved under that restriction.
- `selected_balanced_regret.csv`, `simple_rules_regret.csv`, `observable_timing_sensitivity.csv`: practical-policy performance. The balanced 5.0393% worst regret misses the declared 5% screen.

The threshold-pruning bound relaxes inventory, resource accessibility, discrete funding and route availability. It prices shells at an optimistic linear shadow cost and credits failures/refunds with an optimistic saving. Thus it can exclude an inferior threshold when even its lower bound exceeds a feasible incumbent, without excluding a genuinely faster threshold. See `scan_thresholds.py` for the precise finite grid of bound parameters and full-state calls. Newly prohibiting pre-Mitts farming can only strengthen that relaxed bound.

Monte Carlo seeds and distributions are stored in each result. Selected policies have 20,000 samples per route. Balanced quantiles come from actual 20,000 mixture samples, not averages of component quantiles. All simulation results include mean, 95% CI for the mean, median, p90, p95 and standard deviation.

PRNG programs include supplied-state machine transitions and explicitly assumed entry-state distributions. Uniform boot-orbit phases are reproducible with `prng_initial_states.cpp`; they do not represent a known casual-play distribution. The one-off farm-entry tests omit exactly the outbound 20 seconds and are separate from the all-Carlov-start frozen matrix.

## Limits of certification

Initial-route values are conditional optima under verified nominal probabilities and frozen, partly conditional resource inputs. They are not full-game PRNG-level or movement-route global optima. The delivered gzip files contain exact selected action representatives; sampled tied sets do not cover all full-state ties. Lookup consultation time is additional. Numerical tolerances do not imply microsecond-accurate human timings.
