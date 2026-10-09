# Figurine Gallery solver deliverables

The current implementation requirements are maintained in [optimization_specification.md](optimization_specification.md), including route robustness, the sensitivity stopping criterion, and explicit modeling limitations. Existing numerical results remain subject to the qualifications below.

**Timing setup:** Fast text speed, holding B to advance dialogue. **Progression limit:** the headline results delay most optional shell pickups until all figurines are unlocked; forced early spending on a collect-as-you-go route has not yet been numerically optimized.

Read `report.md` first: the 74.41-minute result is retained for comparison, but its deliberate late-cleanup itinerary conflicts with the requested normal collect-as-you-go progression. The report explains why both 74–75-minute options were downgraded; no corrected chronological optimum has yet been established. `shell_ledger.csv` marks unavailable PAL binary evidence and unverified earliest fusion timing.

**Retained comparison options, downgraded from recommendations for the requested collect-as-you-go playthrough:** use the state-based lookup for **74.41 minutes**, or use the easier **75.15-minute** wagering rule: **1 shell above a displayed base chance of 27%, guarantee at 27% or below**. With the full pool unlocked, switch at **98 figurines owned**. The threshold costs only **44.72 seconds** in expectation; its reported time retains the benchmark’s modeled restocking decisions.

## Lookup

```sh
python3 policy.py 127 100 0
python3 policy.py 0 331 0 3140
```

Arguments are figurines owned, held shells, gallery rupees, and optional unclaimed free shells. Only use the last argument when the report's free-access postgame-bank conditions hold. Inputs with rupees outside residues 0/4 modulo 5 are not covered by this solved zero-outside-rupee run.

`optimal_policy.bin.gz` contains one action byte per state, ordered `(F * 3472 + held + free) * 400 + 2 * floor(R/5) + (R%5==4)`. Actions 1–100 are wagers; 101–103 buy 1–3 bundles. Decompressed length: 188,876,800 bytes.

## Reproduce the calculation

```sh
clang++ -O3 -std=c++17 solver.cpp -o solver
./solver 3471 optimal optimal 2>optimal.log
./solver 3471 one one 2>one.log
./solver 3471 guarantee guarantee 2>guarantee.log
./solver 3471 eighty eighty 2>eighty.log
./solver 3471 threshold threshold27 27 2>threshold27.log
python3 thresholds.py
```

The solver emits raw policy, representative actions/values, metrics, and diagnostics. `evaluate_policy.cpp` independently re-evaluates an existing selected policy at full precision. The delivered metric CSVs contain every initial shell balance 0–3,471, with F=0,R=0.

```sh
clang++ -O3 -std=c++17 evaluate_policy.cpp -o evaluate_policy
./evaluate_policy 3471 optimal optimal
```

## Other progression routes and starting locations

```sh
clang++ -O3 -std=c++17 route_solver.cpp -o route_solver
./route_solver route.csv my_route
```

Each CSV row, without a header, is `unlocked_count,shells_collected_on_entry,wallet_cap,entry_at_farming_area`.

- Counts must be nondecreasing; the final pool must be 136. Derive them from actual story/fusion/local flags. The stage number alone is insufficient.
- Split sources into separate records wherever a Carlov visit is available between them. Grouping sources creates a collection deadline and can cause additional overflow.
- Wallet caps are 100,300,500,999. This run starts with zero gallery rupees.
- Entry-at-farm is 0 or 1. The flag allows one discounted shop trip using 25 seconds fixed travel. Subsequent trips start at Carlov and use 45 seconds.
- Advancing, wagers, and restocking compete on expected time. Advance is encoded as action 104 in phase policies. A separate entry-policy file identifies the discounted initial purchase, if selected.

Example check route:

```csv
1,0,100,0
136,999,999,0
```

It gives 8,163.68601231094 seconds from the initial state. This is a numerical test case, not the game's real unlock itinerary.

The progression solver retains two full phase value arrays in memory, roughly 900 MB plus working arrays. Its policy files support all represented states at each milestone, not a few selected examples. Extra route milestones increase running time and output size.

## Evidence and validation

`audit_sources.py PATH_TO_TMC` regenerates the shell ledger from the pinned EU-preprocessed room text and documented fusion quantities. It does not certify missing ROM-extracted binary assets. `validate.py` uses NumPy/SciPy to check a small MDP against linear programming and independently simulate raw policy files in the task's `work/` directory. `validation.json` preserves the completed 20,000-run checks.

After reproducing the raw policies in the current directory, use `python3 validate.py 20000 .` to run validation there. Python requires NumPy and SciPy. The initial-state early cash-cap check can be reproduced with `./solver 3471 optimal relaxed 0 relax 2>relaxed.log`.

The core uses an independent-uniform draw model, not deterministic PRNG-seed manipulation. New travel shortcuts, repeated shop/farm loops without a Carlov return, externally supplied rupees, or different pull timings require model changes.

Timing uncertainty: `report.md` compares 15-, 20-, and 25-second average base pulls. The 27% threshold remains the best simple rule in this range; `timing_solver.cpp`, `timing_sensitivity.csv`, and `timing_validation.json` contain the sensitivity implementation and evidence. The supplied lookup is still calibrated to 20 seconds.
