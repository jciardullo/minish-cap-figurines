# Preserved 45-second-trip comparison; current source code uses the confirmed travel correction

Current numerical results are in ../funded. The source files here now support 20-second already-funded shop trips and optional farm-entry decisions; older result files in this directory retain 45 seconds for every trip. Do not mix those scenarios.

# Corrected collect-as-you-go analysis

This directory supersedes the late-cleanup itinerary as the working model. Calculations are **conditional on frozen route assumptions**, not a certified reconstruction of every legal first-visit opportunity. The route builder never reads gallery performance and the optimizer cannot reorder its events.

## Completionist definition and route evidence

The equippable-item category means all obtainable permanent inventory equipment and upgrades: the obtainable sword progression through the Four Sword; bombs and Remote Bombs; bow and Light Arrows; boomerang and Magical Boomerang; shield and Mirror Shield; Flame Lantern; Gust Jar; Cane of Pacci; Mole Mitts; Roc’s Cape; Pegasus Boots; Ocarina of Wind; and all four bottle slots. Upgrades replacing earlier equipment count as obtaining that progression, not retaining mutually exclusive versions simultaneously. Unused Fire Rod/orb/sword entries and transient bottle contents are excluded. This interprets the game's [activatable-item enumeration](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/include/item.h#L32).

The other completionist categories retain the specification's definition: permanent/item upgrades, all Pieces of Heart, all Kinstone fusions and rewards, all figurines, all Tiger Scrolls, and four Elements. Consumable-only detours are not automatically required.

The reference follows the story spine of the [Kirby021591 walkthrough](https://gamefaqs.gamespot.com/gba/920670-the-legend-of-zelda-the-minish-cap/faqs/34833), with fixed regional reward sweeps. The ledger presently resolves shell receipts and ordinary gallery opportunities; it is **not a complete item-by-item proof of the 100% route**. Optional fusion timing and some first-encounter assignments are explicit conditional inputs. Wallet upgrades occurring between opportunities are collapsed to the capacity at the next town visit; no gallery actions are allowed between those opportunities.

Source audits reconstruct 3,591 shells, including 120 from six Cucco prizes. Four 200-shell fusion chest amounts rely on flag comments because the active regional binary chest data are unavailable in the source checkout. Do not equate a numerical Bellman optimum with certification of those route/input assumptions. Unrelated consumable chests must be retained in the final ledger only if actually encountered on the fixed completionist route; inclusion remains subject to this encounter audit.

Each JSON ledger has a `.sha256` content hash, corresponding CSV, and manifest entry. Existing reference hashes remain unchanged when new variants are added. `fusion_early` and `fusion_late` change optional eligibility timing separately from shell pickup timing.

## Model and independent evaluation

`full_solver.cpp` solves `(phase, owned count, shells, gallery rupees)` with all legal integer wagers, exact discrete 20-rupee farming, capped refunds, and purchases of one to three PAL or one to four NTSC-U 30-shell bundles. Count reduction is conditional on the verified nested eligible sets in the frozen ledger. Figure selection is nonuniform, but successful pulls always add one eligible unowned figure; therefore identities do not affect nominal count transitions for nested eligibility.

The Bellman candidates are:

- Advance: value after sequential next-event pickups, each individually capped.
- Pull s: pull time plus p times the success value plus (1−p) times the duplicate value, preserving resources.
- Restock B,n: 45+15B+1200n/farming-rate seconds plus the value after n capped 20-rupee pickups and B sequential paid bundles.

The farming suffix envelope evaluates every reachable pickup count, including excess rupees carried forward. It stops at the wallet cap. The compound restock action is equivalent to sequential transactions because each transaction is affordable and capacity-safe whenever the selected aggregate transaction is; there is no intervening farm action at the shop. The current frozen routes start deliberate cycles at Carlov, so all charge the 20-second outbound leg. The current solver supports an optional trailing farm-entry flag after each route line's pickup quantities. A flagged opportunity has one explicit 25-second travel restocking decision before ordinary Carlov decisions; its .entry policy is evaluated independently. The stored start_at_farm=false keeps that action out of the present frozen routes.

Starting with zero gallery rupees, reachable cash residues are 0 or 4 modulo 5 (the latter from the 999 cap). The 400-entry cash grid represents these exactly, including earlier wallet caps. It does not support arbitrary outside-gameplay cash inputs; such rupees are excluded from the conservative analysis.

`evaluate_exact.cpp` independently computes exact forward state occupancies and accumulated resources for the selected policy. It checks completion probability and shell/rupee conservation. `simulate.cpp` independently simulates 20,000 completions and reports the specified distribution statistics.

The new representative CSV export includes all action codes within solver tolerance at sampled states; it does not claim full-state tie coverage. Actions 1–100 are wagers, 0 is progression, and restock codes are `101+(B−1)+max_bundles*n`. Raw policy files remain intermediate artifacts until compression/lookup delivery. Initial files generated before the tie-export revision have no tie column.

## PRNG validation assumptions

The supplied-state simulation reproduces the [machine's rejection draw and second selection draw](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L621) and the game's rotate/multiply PRNG transition. It compares nominal independent draws with isolated-machine advancement and a deliberately assumed 1,200-call gap after each pull. Initial nonzero 32-bit states are sampled by seeded MT19937-64; this is an assumed distribution, not established normal-play gallery-entry behavior. Selection consumes its draw but the simulator tracks count rather than rendering individual selected figures. Other game RNG calls are not reconstructed. These tests cannot certify full-playthrough PRNG realism or universal independence.

## Reproduction

Compile with `clang++ -O3 -std=c++17`. First run `python3 freeze_routes.py PATH_TO_TMC`, verify ledger hashes, and convert ledger phases to lines `unlocked wallet pickup_count quantities...`. Then run:

```sh
full_solver route.txt prefix PAL optimal 27 0.000001 20 300 15
evaluate_exact route.txt prefix PAL exact.json
simulate route.txt prefix PAL simulation.json 20000 20261007
```

The corresponding NTSC-U invocation changes the region argument, price, eligibility ledger, and legal-input shortest paths. It is not a PAL time rescaling. Fast text speed and holding B apply. The equal-time ±10 input assumption remains empirical.

The working practical-policy search tests only observable chance/inventory rules; its results are not certified until exact evaluation, route regrets, and timing sensitivities are complete. See the parent optimization specification for stopping criteria and limitations.
