# Minish Cap Figurine Gallery: collect-as-you-go analysis

## Player-facing answer

**Collect completionist rewards normally, spend shells during ordinary town visits when the inventory is getting full, and finish the gallery after the full figurine pool is unlocked. Use a state-dependent wager rather than always betting one shell or always guaranteeing success.**

The [offline helper](gallery_helper.html) supplies the fastest tested fixed observable policy. Select your version and recognizable story milestone, then enter figurines owned, held shells, current rupees, and displayed chance. Follow its wager, purchase, or “continue normal progression” instruction. Update the state after a duplicate or success. It never asks which chest comes next or reads hidden RNG. Select the **fixed** preset for the easier tool-assisted recommendation. The optional balanced preset selects one of three routines once per playthrough; keep that preset afterward.

- Before shells are accumulating toward the 999 cap, saving them is generally useful because later unlocks improve the chance of a new figure. There is no universal optimal “spend exactly the overflow” rule. At normal town visits, check the current-state helper; an early session can be worthwhile before the cap is reached.
- Serious final cleanup belongs after the ending **and** the optional completionist eligibility requirements. Merely defeating Vaati does not independently certify that every figure is eligible.
- After each pull, retain the remaining shells and the duplicate’s capped 5-rupee payout. Recalculate the action. Intermediate bets can be best: with the full pool, 127 figures owned, 100 shells and zero gallery rupees, the reference optimum bets **35 shells in PAL** and **60 in NTSC-U**.
- Buy only when the policy calls for it. Already-funded purchases use the direct shop round trip. A purchase can be worthwhile before natural shells are exhausted; accessible free shells and not-yet-accessible future rewards are different resources.

**The recommendation is empirically route-robust, not universally optimal.** Across eight frozen route variants per version and the specified one-axis timing tests, the fixed lookup’s worst expected-time regret is about **6.45%**. The balanced lookup reduces the worst tested regret to **5.04%**. It narrowly misses the declared 5% screen; that is not a numerical tie. Neither result proves the best possible observable policy among all policy forms.

A small memorable rule matching the lookup’s performance was **not established**. A tested simpler stage rule costs 129.80 minutes on the PAL reference and 119.57 on NTSC-U, with worst route regrets of 16.51% and 11.02%. It keeps 600 shells after the two-element sword/story cutscene, 150 after Fortress of Winds, 700 after the Water Element, 800 after the Royal Crypt; earlier wagers use one shell above 80%, otherwise guarantee. At the first Wind Element visit it uses one above 20%, otherwise guarantee; later Wind visits reserve 900. Final cleanup uses one above 9% PAL / 10% NTSC-U, otherwise guarantee. These are observable but cumbersome, and are a fallback rather than a near-optimal universal recommendation.

Consultation time is excluded from the calculations. On the PAL reference, the fixed lookup’s advantage over that simpler rule is about 10.4 minutes, or roughly 1.8 seconds per lookup if consulted every pull. A player taking longer may prefer the simpler rule. The optional balanced preset’s advantage is smaller. Human usability therefore matters alongside modeled pull time.

## Technical justification and scope

The conditional reference-route mathematical optimum is **119.41 minutes PAL** and **112.78 minutes NTSC-U**. These are expected gallery-attributable times, including pulls and deliberate acquisition, excluding ordinary game completion and normal completionist collection/travel. They are **not certified whole-game minima for an independently verified complete 100% itinerary**.

The reconstructed guaranteed-shell ledger totals **3,591 shells** in both versions. Its event ordering, several optional prerequisite assignments, and four fusion-chest quantities are conditional audited inputs. The frozen ledger resolves shell events and gallery opportunities; it is not an item-by-item proof of every first encounter or complete 100% route. These input limitations are distinct from numerical solver error. The verified core has been solved; additional hypothetical edge cases are not a reason to defer its conditional result.

The earlier approximately 70–75-minute results remain in [the historical report](late_cleanup_report.md). They are downgraded comparisons because delaying most shell pickups to final cleanup does not represent the requested collect-as-you-go normal playthrough. They must not be presented as this project’s practical optimum.

## Verified regional mechanics

Source revision: `6fb6dfb4a7efbe24d0fd1dda5097af6131faacde`. Detailed line references and regional preprocessing evidence are in the [mechanics audit](corrected/mechanics_audit.md).

For eligible pool size U and owned count F<U, the one-shell displayed percentage is `max(1,floor(100(U−F)/U))`. Each added shell adds one displayed point; the maximum legal wager is the smaller of held shells and the amount reaching displayed 100%. Actual nominal success percentage is the maximum of the displayed chance and the hidden floor: **15% below 50 owned; 12% at 50–79; 9% at 80–109; 6% at 110+**. Productive pulls are unavailable when F=U. Success always adds one eligible unowned figure. Selection identities are nonuniform, but the verified nested eligible sets permit a count reduction for these routes. [Figurine-device source](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c).

PAL shells cost **300 R per 30**, NTSC-U **200 R per 30**. A 999 wallet permits three PAL or four NTSC bundles in one visit. Purchases are sequential; each requires affordability and S+30≤999. Duplicates retain `min(5,W−R)` rupees; excess is lost. Shell receipts retain `min(g,999−S)`. [Regional price table](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/itemMetaData.c), [wallet handling](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/gameUtils.c), [shell handling](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/itemUtils.c).

PAL pull duration is `20+(s−1)/15` seconds. NTSC inputs are shortest paths from wager 1 through the actual legal ±1/±10 clamped input graph; duration is `20+minimum_inputs/15`. The path 1→11→21→20 takes three inputs when 21 is legal; if the boundary is 20, clamped 1→11→20 takes two. Equal physical duration for ±10 and ±1 is empirical, not verified timing data.

## Natural resources and frozen routes

The complete ordered regional reference ledgers are [PAL CSV](corrected/PAL_reference.csv) / [JSON](corrected/PAL_reference.json) and [NTSC-U CSV](corrected/NTSC-U_reference.csv) / [JSON](corrected/NTSC-U_reference.json). All other variants and hashes are indexed in the [manifest](corrected/route_manifest.json). Each source appears once; quantity and collection milestone are explicit. Supporting source records are [PAL](corrected/PAL_source_audit.json) and [NTSC-U](corrected/NTSC-U_source_audit.json).

The ledger contains 46 shell sources: 33 ordinary chest records, eight fixed rewards including six Cucco prizes totaling 120 shells, four 200-shell fusion-chest records, and one fixed ground shell. Four fusion amounts depend on source comments rather than available active binary chest data. Random enemy/grass drops are excluded. Consumable-only detours are not automatically required by the 100% definition; whether each listed chest is actually encountered in a chosen full itinerary remains an input audit limitation.

The chosen completionist standard includes every permanent/item upgrade, heart piece, Kinstone fusion and unlocked reward, figurine, Tiger Scroll, Element, and the equippable inventory: swords through Four Sword, bombs/Remote Bombs, bow/Light Arrows, boomerang/Magical Boomerang, shield/Mirror Shield, lantern, Gust Jar, Cane of Pacci, Mole Mitts, Roc’s Cape, Pegasus Boots, Ocarina of Wind, and four bottles. Unused Fire Rod/orb items and transient bottle contents are excluded. Gallery-dependent completion rewards may follow the gallery terminal event at zero ordinary completionist time.

Reference pool sizes at nine modeled ordinary gallery opportunities are PAL `51,55,63,88,101,106,123,130,136`, NTSC-U `48,52,62,88,101,106,123,130,136`. Shell blocks are `70,200,570,391,860,300,200,1000,0`. Wallet capacity is 300 at the first two opportunities, 999 thereafter; intermediate upgrades occur between opportunities. The house farm is unavailable until the Mole Mitts milestone. The final 1000-shell block necessarily causes at least one overflow **in this coarse ledger**, not necessarily in every actual playthrough with more town visits.

Routes are frozen before optimization. Earlier/later rewards, missed early/late chests, postgame backtracking, and early/late optional figurine eligibility are separate scenarios, never pooled into a clairvoyant blended route. Reference hashes:

- PAL: `6ab75ae3226c2ad68db875ed86fe14904839d2410256ac764190affaa7c06f64`
- NTSC-U: `f4948baf2235381192edd91fb36653bcdfa35ad5f7347d0be8e1ef7cf814c116`

## Mathematical model

Let x=(e,F,S,R,W,L) represent frozen event, owned count, shells, gallery cash, wallet cap, and relevant restocking location. Future pickups are inaccessible until their event. The general set-valued version retains the owned set if eligibility is not nested. The stochastic shortest-path equation is

`V(x)=min_a [ t(x,a) + Σ_y P(y|x,a)V(y) ]`, with V=0 at 136 owned.

A wager s has value `t(s)+pV(e,F+1,S−s,R,W,Carlov)+(1−p)V(e,F,S−s,min(W,R+5),W,Carlov)`. Progression applies each next pickup immediately, recording received, retained and overflow separately. It may deliberately tolerate overflow. No natural-resource-first or exactly-overflow spending heuristic constrains the optimizer.

Farming is literal 20-rupee pickups, R←min(W,R+20), each costing `1200/rate` seconds. Enumerate all reachable pickup counts n up to the wallet cap, including funding beyond the immediate purchase. Sequential purchases subtract regional price and add 30 shells each, with 15 seconds per bundle. From Carlov, travel costs 45 seconds when n>0, **20 seconds when already funded (n=0)**. At a genuine farming-area entry, omit the 20-second outbound leg; an independent synthetic test verifies exactly 20 seconds saved for the selected case. All frozen numerical routes presently start deliberate cycles at Carlov.

The full-information optimizer knows the frozen future route. The observable recommendation cannot query it. No outside natural rupees are credited; only duplicate payouts enter gallery cash. A player with existing spendable cash can require less farming, but discrete pickup and purchase boundaries mean “subtract R/5 seconds” is not universally exact.

Policy iteration evaluates full resource states, with an exact suffix envelope for all farming counts and analytic evaluation of same-count policy cycles. Cash states are losslessly reduced to residues 0 or 4 modulo 5, the exact reachable set from zero under +5 refunds, +20 farming, regional purchase prices, and capped 999 refunds. This is not rounding away cash. Raw off-grid cash entered into the helper is conservatively queried below its value and is outside that exact reachable-state certificate.

## Regional benchmarks

All policies use the same frozen reference resources and optimally selected progression/restocking decisions. The threshold benchmark is **not** by itself an observable complete player policy. Displayed-80% wagers are minimum wagers reaching at least 80%. Fractional trips and counts are expectations.

| Version | Policy | Minutes | Shells used | Pulls | Duplicates | Trips | Farmed R |
|---|---|---|---|---|---|---|---|
| PAL | Always 1 | 173.67 | 521.0 | 521.0 | 385.0 | 0.00 | 0.0 |
| PAL | Displayed 100% | 254.80 | 7533.0 | 136.0 | 0.0 | 45.00 | 40200.0 |
| PAL | Displayed 80% | 218.34 | 6664.0 | 168.3 | 32.3 | 35.30 | 30864.9 |
| PAL | Best 1/guarantee threshold | 130.25 | 2334.7 | 346.5 | 210.5 | 4.42 | 2152.3 |
| PAL | Historical 27% threshold | 178.53 | 5420.6 | 206.2 | 70.2 | 24.00 | 20655.1 |
| PAL | All-integer optimum | 119.41 | 3719.9 | 338.2 | 202.2 | 1.49 | 317.7 |
| NTSC-U | Always 1 | 173.67 | 521.0 | 521.0 | 385.0 | 0.00 | 0.0 |
| NTSC-U | Displayed 100% | 194.56 | 7535.0 | 136.0 | 0.0 | 34.00 | 26800.0 |
| NTSC-U | Displayed 80% | 171.37 | 6667.3 | 168.3 | 32.3 | 26.79 | 20544.0 |
| NTSC-U | Best 1/guarantee threshold | 123.35 | 2428.4 | 333.0 | 197.0 | 4.48 | 1794.2 |
| NTSC-U | Historical 27% threshold | 145.75 | 5420.6 | 206.1 | 70.1 | 18.02 | 13655.6 |
| NTSC-U | All-integer optimum | 112.78 | 3950.9 | 306.7 | 170.7 | 3.10 | 1557.3 |


The best threshold is **9% PAL / 10% NTSC-U**, using one shell above it and guaranteeing at or below it. All 0–100 threshold candidates were considered: potentially competitive ones were solved in full state; others were certified dominated by optimistic lower bounds relaxing inventory/resource timing constraints. [Scan](funded/threshold_scan.csv), [scan implementation](funded/scan_thresholds.py). The old 27% recommendation is not carried forward.

The one-shell policy retains enough free resources on typical paths, so expected purchases are numerically negligible; that is not a guarantee against its unbounded duplicate tail. Guaranteeing success avoids duplicates but consumes many shells and forfeits their refunds.


## Representative full-pool decisions

These are selected representatives for the full 136-figure pool, with gallery cash stated explicitly. They are not universal rules at the same displayed chance earlier in the game; some purchase-timing actions have tied pull alternatives.

| Owned | Base % | Shells | Rupees | PAL | NTSC-U |
|---|---|---|---|---|---|
| 27 | 80 | 999 | 0 | 1 shells | 1 shells |
| 68 | 50 | 999 | 0 | 1 shells | 1 shells |
| 108 | 20 | 900 | 0 | 1 shells | 1 shells |
| 127 | 6 | 100 | 0 | 35 shells | 60 shells |
| 127 | 6 | 100 | 50 | 42 shells | 60 shells |
| 128 | 5 | 100 | 0 | 77 shells | 35 shells |
| 135 | 1 | 100 | 0 | 100 shells | 100 shells |
| 135 | 1 | 30 | 0 | 30 shells | 30 shells |
| 135 | 1 | 30 | 300 | buy 1 bundles, 0 farm pickups | buy 2 bundles, 5 farm pickups |

## Reference resource and time breakdown

| Expected quantity | PAL | NTSC-U |
|---|---|---|
| Natural shells received | 3591.000 | 3591.000 |
| Natural shells retained | 3590.000 | 3589.911 |
| Natural overflow | 1.000 | 1.089 |
| Shells consumed | 3719.888 | 3950.932 |
| Shells purchased | 129.900 | 361.021 |
| Pulls | 338.220 | 306.736 |
| Duplicates | 202.220 | 170.736 |
| Duplicate rupees retained | 1011.095 | 853.678 |
| Refund rupees lost to wallet cap | 0.005 | 0.000 |
| Farming pickups | 15.884 | 77.866 |
| Farmed rupees retained | 317.674 | 1557.322 |
| Farming seconds | 63.535 | 311.464 |
| Trips | 1.487 | 3.104 |
| Already-funded shop trips | 0.830 | 1.025 |
| Ending shells | 0.012 | 0.000 |
| Ending gallery rupees | 29.772 | 4.195 |


PAL purchase spending is about 1,299 R: retained refunds contribute about 1,011 R, deliberate farming about 318 R, with roughly 30 R remaining. NTSC purchase spending is about 2,407 R: about 854 R from refunds and 1,557 R farmed, leaving about 4 R. Receipt/consumption and cash balances are independently checked, including overflow.

PAL time comprises about 112.74 minutes of base pull dialogue, 3.76 minutes of extra wager entry, 1.06 minutes farming, and 1.85 minutes travel/purchasing. NTSC has fewer expected pulls and cheaper purchases; its wager-entry advantage is not obtained by rescaling PAL results.

In the reference optimal PAL simulation, the first meaningful session is after the two-element sword and the relevant West Hyrule story cutscene, with about 840 shells. Sessions create room for later receipts, but “prevent every overflow” is not a constraint. The guaranteed strategy deliberately loses about 78 natural shells on its own optimal path. Selected representatives of numerical ties can change purchase timing and resource statistics without material time changes.

## Route sensitivity, convergence and practical regret

| Version | Route | Optimal min | Natural retained | Overflow | Bought shells | Farmed R | Fixed lookup regret s / % | Balanced regret s / % |
|---|---|---|---|---|---|---|---|---|
| PAL | reference | 119.41 | 3590.0 | 1.0 | 129.9 | 317.7 | 0.0 / 0.00% | 255.8 / 3.57% |
| PAL | earlier | 121.27 | 3591.0 | 0.0 | 147.5 | 468.4 | 468.7 / 6.44% | 366.7 / 5.04% |
| PAL | later | 119.25 | 3529.0 | 62.0 | 129.6 | 316.3 | 33.1 / 0.46% | 288.5 / 4.03% |
| PAL | missed_early | 119.29 | 3509.0 | 82.0 | 129.8 | 316.7 | 29.5 / 0.41% | 284.9 / 3.98% |
| PAL | missed_late | 120.10 | 3390.0 | 201.0 | 132.1 | 327.4 | 9.2 / 0.13% | 265.4 / 3.68% |
| PAL | fusion_early | 105.76 | 3590.0 | 1.0 | 73.2 | 15.7 | 0.0 / 0.00% | 92.9 / 1.46% |
| PAL | fusion_late | 119.41 | 3590.0 | 1.0 | 129.9 | 317.7 | 0.0 / 0.00% | 264.4 / 3.69% |
| PAL | missed_postgame | 113.92 | 3590.0 | 1.0 | 105.4 | 147.8 | 405.2 / 5.93% | 344.4 / 5.04% |
| NTSC-U | reference | 112.78 | 3589.9 | 1.1 | 361.0 | 1557.3 | 0.0 / 0.00% | 189.0 / 2.79% |
| NTSC-U | earlier | 114.33 | 3590.9 | 0.1 | 386.8 | 1720.4 | 346.6 / 5.05% | 271.1 / 3.95% |
| NTSC-U | later | 112.68 | 3528.9 | 62.1 | 360.7 | 1556.3 | 41.6 / 0.62% | 230.5 / 3.41% |
| NTSC-U | missed_early | 112.73 | 3508.9 | 82.1 | 360.7 | 1555.6 | 36.7 / 0.54% | 225.5 / 3.33% |
| NTSC-U | missed_late | 113.64 | 3389.9 | 201.1 | 362.1 | 1551.0 | 9.6 / 0.14% | 198.9 / 2.92% |
| NTSC-U | fusion_early | 101.18 | 3589.9 | 1.1 | 164.1 | 339.9 | 0.0 / 0.00% | 85.9 / 1.41% |
| NTSC-U | fusion_late | 112.78 | 3589.9 | 1.1 | 361.0 | 1557.3 | 0.0 / 0.00% | 195.8 / 2.89% |
| NTSC-U | missed_postgame | 108.01 | 3589.9 | 1.1 | 282.9 | 1068.4 | 377.6 / 5.83% | 323.5 / 4.99% |


Across all eight variants, optimal time spans **15.51 minutes PAL (12.99% of reference)** and **13.14 minutes NTSC-U (11.65%)**. These spans include optional figurine-unlock timing changes; they must not be attributed solely to chest order. Earlier optional eligibility gives the largest improvement. Pure pickup-order differences also affect overflow, farming, and the best early decisions.

At matched resource states, most variants’ value functions converge once their remaining pickup schedules and eligibility agree. Postgame-backtracking variants remain different at the last pre-ending opportunity because resources are still inaccessible. Once the full pool is available and no pickups remain, the state-conditioned postgame problem is identical across routes: sampled value/action differences are zero. Accumulated time and inventory distributions do not thereby become identical. [Convergence measurements](funded/route_convergence.csv), [full resource table](funded/regional_route_results.csv).

The same fixed practical routine was evaluated unchanged on every route. Its observable Wind Element routine is chosen using owned count on entry, rather than an opaque walkthrough event; tiny classifier mismatch probabilities are exported and bounded. The balanced routine mixes fixed reference, earlier, and half-cap presets with probabilities approximately **4.66%, 21.77%, 73.57%**, once per playthrough. It minimizes worst expected percentage regret **within these seven tested presets**, not within all imaginable policies. Regret is `Tpractical−Toptimum`; percentage is `100(Tpractical−Toptimum)/Toptimum`.

The 5% acceptance threshold was set before final screening. The balanced maximum **5.0393%** fails it by roughly 2.9 seconds beyond the 5%-allowed regret in its binding case. That miss is tiny compared with measured-input uncertainty, but is not hidden by rounding or relabeled as an exact numerical tie. The easier fixed lookup remains the default tool-assisted recommendation; neither is claimed to be a newly discovered universal small-number threshold rule. [Balanced regrets](funded/selected_balanced_regret.csv), [simpler-rule regrets](funded/simple_rules_regret.csv).

## Timing sensitivity and stopping

| Version | Base pull s | Farm R/min | Inputs/s | Reoptimized min |
|---|---|---|---|---|
| PAL | 15 | 300 | 15 | 90.93 |
| PAL | 20 | 250 | 15 | 119.52 |
| PAL | 20 | 300 | 12 | 120.35 |
| PAL | 20 | 300 | 18 | 118.78 |
| PAL | 20 | 350 | 15 | 119.19 |
| PAL | 25 | 300 | 15 | 146.67 |
| NTSC-U | 15 | 300 | 15 | 86.30 |
| NTSC-U | 20 | 250 | 15 | 113.64 |
| NTSC-U | 20 | 350 | 15 | 111.90 |
| NTSC-U | 25 | 300 | 15 | 137.24 |


Baseline rows are 20 seconds / 300 R per minute / 15 inputs per second. The practical presets were held fixed and re-costed against these reoptimized optima. This is the declared route matrix at baseline plus reference one-axis timing variations, **not a full Cartesian combination of every route and timing**. Different pull counts mean a common dialogue-speed change does not cancel across policies. A ±5-second change materially changes absolute totals and can change mathematical wagers; the tested observable lookup remains relatively close across these axes.

The bounded matrix is complete. No further speculative scenarios are added without a specific new mechanic suggesting a material change. The strict 5% screen did not pass, so report conditional performance rather than force a universal claim.

## Simulation and numerical verification

Each selected policy/route has at least 20,000 completion simulations with documented seeds. Reference distribution summaries below are in minutes. Monte Carlo validates expectations and variance; it is not proof of optimality.

| Version | Policy | Mean min | 95% CI mean | Median | 90th %ile | 95th %ile | SD min |
|---|---|---|---|---|---|---|---|
| PAL | Route optimum | 119.49 | [119.31, 119.67] | 118.46 | 136.21 | 142.07 | 12.96 |
| PAL | Fixed observable lookup | 119.48 | [119.30, 119.66] | 118.46 | 136.21 | 142.26 | 12.98 |
| PAL | Balanced observable lookup | 123.67 | [123.48, 123.85] | 123.14 | 140.81 | 147.01 | 13.24 |
| NTSC-U | Route optimum | 112.94 | [112.79, 113.09] | 112.13 | 127.02 | 131.76 | 10.72 |
| NTSC-U | Fixed observable lookup | 112.77 | [112.62, 112.92] | 111.80 | 126.99 | 131.45 | 10.63 |
| NTSC-U | Balanced observable lookup | 115.90 | [115.75, 116.05] | 114.96 | 130.19 | 134.27 | 10.72 |


Policy iteration uses a 10⁻⁶-second Bellman target and repeat verification at 10⁻⁷. Independent forward occupancy evaluation agrees within the documented tolerance and checks terminal probability and resource conservation. Reduced cases are checked against exhaustive policy evaluation, value iteration, and linear programming. Tests cover hidden floors, legal NTSC shortest paths, nested unlock transitions, exhaustion, caps, partial purchase funding, all farming counts, sequential shell purchases, and farm availability. [Tests](corrected/test_core.cpp), [reduced verification](corrected/reduced_validation.json), [tolerance diagnostics](funded/tolerance_validation.json).

The Mole Mitts availability correction was additionally checked against previously unconstrained solutions: a feasible selected initial policy matching an unconstrained lower bound certifies the same initial optimum under the narrower action set. Reference and player-lookup source policies are re-solved with farming disabled before Mitts. No hidden early farming is needed to achieve the reported reference values.

Selected-policy lookup files are exact compressed uint16 representatives with raw content hashes. The [manifest](policy_lookup/manifest.json) and [CLI](gallery_policy.py) are machine-readable. [Sampled tied sets](policy_lookup/sampled_tied_actions.json) cover 22,974 queried states, not every full-state tie. Ties within numerical tolerance are not uniquely optimal; differences merely small relative to timing uncertainty are a separate category. A tighter solve can narrow unresolved tied sets without changing the recommendation.

## Hidden PRNG validation

The source PRNG transition is `state=ror32(3*state,13)` with return `state>>1`. Carlov uses low-seven-bit rejection of values ≥100 plus a subsequent figure-selection draw. Reproducing this supplied-state subsystem does not establish the state distribution of a normal player entering the gallery. [PRNG assembly](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/asm/src/code_08000E44.s).

Validation uses both uniform nonzero 32-bit states and uniformly sampled phases of the boot seed’s enumerated **822,119,800-state orbit**. These are declared assumptions, not reconstructed casual-play distributions. The boot-orbit isolated-machine experiment uses 200,000 completions; optional 1,200-call inter-pull advancement uses 20,000 and does not emulate full-game progression.

Under boot-orbit isolated calls, PAL mean is about **14 seconds (0.19%)** above the nominal model; NTSC-U about **13 seconds (0.19%)** above. Correlation is detectable, so IID is not asserted literally exact. Alternative advancement experiments change the small discrepancy. These observed effects support using the nominal marginalized model for the practical timing comparison under tested distributions; they do not certify an exact RNG-level optimum or validate every entry-state distribution. Player wagers never condition on RNG state.

## Farming evidence and limitations

The house method’s 20-R pickup every four seconds is the measured baseline. It requires Mole Mitts. Available evidence supports its usefulness but **does not certify it as the globally fastest net farm**. Yellow Picolyte grass farming is random and must subtract its 200-R dose cost; reported gross yields alone do not establish a faster net rate. Repeatable final Cucco play is slower even before dialogue. See [farming evidence and break-even comparisons](farming_notes.md).

Human execution is represented by measured averages with **Fast text and B held**. Mistakes, pauses, menu hesitation, lookup consultation, and routing/execution variance are not directly modeled. Random overworld shells/rupees and naturally encountered rupees are excluded, so real players may need less deliberate farming. Route robustness is empirical. NTSC ±10 input timing is assumed until measured. Ordinary-play RNG-state distribution and several route/resource facts remain uncertain. Microsecond solver precision does not make whole-second measured inputs microsecond-accurate. These are model limitations, not reasons to postpone solving the verified core.

## Files and reproduction

See [reproduction instructions](funded/README.md), [general model](corrected/mathematical_model.md), [source audit](corrected/mechanics_audit.md), [explicit limitations](corrected/model_limitations.md), and [project specification](optimization_specification.md). Source code and scripts are delivered without game ROMs. Freeze ledgers first, verify their hashes, compile, solve, independently evaluate, simulate, then evaluate unchanged practical policies. Do not mix the superseded 45-second-all-trips files with current already-funded-20-second results.
