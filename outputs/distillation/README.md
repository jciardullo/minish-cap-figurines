# Memorable Figurine Gallery strategies

Read the complete [player rules](player_strategy.md) first, or open the [one-page-per-region cards](player_cards.html). The recommended **compact rules** take **122.04 minutes PAL / 115.29 minutes NTSC-U** on the conditional reference route, with worst-tested regret **8.14% / 7.56%**. The **memorized knee options** take **130.11 / 122.53 minutes**, with worst regret **22.78% / 21.10%**. Neither meets 5%; no human candidate assessed by deterministic forward evaluation does. The official knee selections are unchanged. The supplemental US endpoint changes normalization without changing the selected knee; historical endpoint-only audit records retain their earlier geometry. A targeted supplemental policy changes the PAL C=8 interior frontier; see [endpoint audit](endpoint_audit.md). These are best tested policies under the stated search and complexity budget.

See the [supplemental change log](supplemental/CHANGELOG.md) for the exhaustive-through-C8 audit, bounded extension, knee margins and synthetic-prior comparison. The default compact and memorized recommendations are unchanged; the expanded plot includes a small US improvement that is not adopted.

## Technical deliverables

- [Reproducibility bundle](../figurine_distillation_bundle.zip), [per-file hashes](manifest.json), [evaluation provenance](evaluation_provenance.json).
- [15-section mathematical paper](paper.pdf), [LaTeX source](paper.tex), [bibliography](references.bib).
- [Pareto plot](pareto.svg), [named selections and knee geometry](selections.json), [weight/duplicate stability checks](knee_stability.json).
- [Selected summary](selected_summary.csv), [all 26 selected-policy cases](selected_scenarios.csv), [scenario definitions](scenario_definitions.csv).
- [Simulation distributions](simulation_distributions.csv): 48 separate 20,000-run cells, fresh documented seeds, means/95% CIs/medians/p90/p95/SDs.
- [10,000 candidate definitions](candidates.txt), [candidate metadata](candidates.json), [statuses and simultaneous screening intervals](candidate_statuses.csv), [all exact policy summaries](exact_policy_summary.csv). Exact JSON results are in `exact/`.
- [Search configuration](screening_configuration.json), [deterministic forward occupancy evaluation configuration](exact_evaluation_configuration.json), [final score audit](complexity_audit.json), [publication checks](publication_checks.json).
- [Separate supplemental cash cases](incidental_cash.json), [software-helper benchmark across all 26 cases](software_helper_benchmark.csv).

`exactly_dominated` is a legacy schema label for empirical dominance established using deterministic forward occupancy expectations. `not_retained_after_screening` does not mean dominated. Equal-complexity/equal-regret duplicates may retain evaluated status even though one representative appears on the plotted frontier. The historical generation score is retained; the final score counts the printed clauses and discards inactive implementation parameters.

The complexity check changes the official knee in two of sixteen tests per region. That sensitivity is reported, not used to switch knee criteria. No new scenario families were added after this bounded analysis.

## Reproduction

Run from the extracted project root containing `outputs/` and `work/`. Requires C++17/clang, Python with NumPy and SciPy. Plot rendering additionally needs Matplotlib/Pillow. No ROM, hidden RNG seed knowledge or external player helper is required for the human rule.

```sh
mkdir -p work/distillation
clang++ -std=c++17 -O2 outputs/distillation/exact.cpp -o work/distillation/exact
clang++ -std=c++17 -O2 outputs/distillation/screen.cpp -o work/distillation/screen
clang++ -std=c++17 -O2 outputs/distillation/test_policy.cpp -o work/distillation/test_policy
work/distillation/test_policy
python3 outputs/distillation/test_analysis.py
python3 outputs/distillation/reproduce.py
```

The last command freshly evaluates all eight routes for all six named regional policies, checks the published values within 1e-5 seconds, and writes scratch results to `work/distillation/reproduction/`. `--all` recomputes all 2,816 regional records previously assessed by deterministic forward evaluation; it can take hours. The full ID registry is frozen in `exact_evaluated_ids.json` so reproduction does not silently replace the tested set with a different shortlist.

```sh
python3 outputs/distillation/reproduce.py --all
python3 outputs/distillation/frontier.py
python3 outputs/distillation/repair_endpoint.py
python3 outputs/distillation/supplemental/analyze.py
python3 outputs/distillation/supplemental/plot.py
python3 outputs/distillation/validate_selected.py
```

To redo screening, `holdout_screen.py` replays the frozen list with seed 20261110 and 512 common-random-number completions per regional route. The supplied gzip JSONL files preserve each output's cost means/covariances. These records reconstruct the approximate simultaneous intervals without additional sampling. The protected complexity-band/tier leaders and confidence-compatible pool exceed the nominal beam width. After screening, run `complexity_audit.py`, then `evaluate.py` and `frontier.py`; use a disposable copy if rebuilding published files. Existing exact files preserve earlier genuinely evaluated candidates.

The original bounded generation is documented in `search.py`, `refine_entry.py`, and `refine_compact.py`; `candidates.txt` is the authoritative frozen 10,000-row search output. Audited final feature counts supersede generation-time scores. Do not infer global optimality over all human policies from this bounded search.

Regenerate the tables/paper from published machine-readable results with:

```sh
python3 outputs/distillation/publish.py
python3 outputs/distillation/finish_assets.py
tectonic --keep-logs --outdir outputs/distillation outputs/distillation/paper.tex
```

`paper.tex` is standalone for the desktop built-in compiler; the bibliography is inline and also supplied separately as `.bib`. The exported PDF used Tectonic 0.17.0. On macOS, a project-local `TECTONIC_CACHE_DIR` avoids writing to a home cache. The built-in compiler also accepted the source. PDF pages were rendered and inspected; no clipped tables or overfull boxes remain.

## Conditional inputs and preserved benchmarks

The existing [mechanics/resource audit](../corrected/README.md), [frozen route ledgers](../corrected/route_manifest.json), [regional numerical inputs](../funded/README.md), [prior mathematical-helper report](../report.md), [offline helper](../gallery_helper.html), and [downgraded late-cleanup comparison](../late_cleanup_report.md) are preserved. The helper may use an owned-count lookup and is excluded from the human frontier. Benchmark-only wager restrictions use optimized progression/restocking, so they must not be mistaken for a complete simple early-session policy.

The ledger reconstruction remains conditional rather than an independently certified item-by-item 100% itinerary. Four fusion quantities rely on source comments. Main calculations assume nominal success probabilities; supplied-state PRNG validation does not establish a normal playthrough's entry-state distribution. Bellman residuals/tighter solves/independent evaluations provide numerical evidence, but no directed-rounding value interval was established. The paper gives a conditional residual-to-error theorem without claiming that empirical timings or reported digits have microsecond accuracy.

Human pauses, menu checks, consultation time and execution mistakes are not separately modeled. Fast text/B-held timing is assumed. Random drops and ordinary rupees are excluded, so conservative farming can exceed actual farming. NTSC ±10 timing remains empirical. Route robustness is tested rather than universal, and the knees' large worst regrets must not be called universally near-optimal.

## Evaluation terminology and publication metadata

Forward occupancy expectations are deterministic, non-Monte-Carlo floating-point calculations. They are not exact arithmetic or directed-rounding certificates. Legacy machine paths and status keys remain unchanged for compatibility; [their semantic mapping](evaluation_terminology.json) makes that distinction explicit. The current edited LaTeX source is authoritative; older generators must not overwrite its editorial revisions.

Project lead and curator: **jciardullo**. The paper and guide include the human-directed, AI-assisted contribution statement. No public repository URL, assigned release identifier, DOI, or archival identifier has been supplied or verified.

## Final interpretation pass

See [change log](supplemental/terminology_changelog.md), [derived arithmetic](supplemental/interpretation_traceability.json), and [verification](supplemental/interpretation_verification.json). No new broad search was performed. Legacy `tier5` machine keys refer to the local compact-policy mutation neighborhood, not an exhaustive higher-tier search.
