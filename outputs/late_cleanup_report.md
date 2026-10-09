# Historical late-cleanup comparison — downgraded

These results postpone optional shell collection and use an earlier resource ledger. They do not answer the collect-as-you-go completionist question and are retained only as comparisons.

# PAL Minish Cap Figurine Gallery: expected-time optimization

**Retained comparison scenario, downgraded from a recommendation for the requested playthrough.** The computed scenario optimum is **4,464.505 seconds = 74.408 minutes of additional gallery time**, for the explicitly defined late-cleanup route below, a reconstructed **3,471-shell** natural supply, zero outside rupees, and the user's timing model. It consumes approximately 3,471 shells in 212.363 pulls, with 76.363 duplicates. Paid acquisition is numerically negligible from this initial state, although sufficiently unlucky realizations can require it.

**Two retained options within that late-cleanup scenario:**

- **Fastest expected finish — 74.41 minutes:** follow the state-based lookup, which adjusts wagers to figurines owned, available shells, and rupees.
- **Easier to remember — 75.15 minutes:** wager **1 shell while the displayed base chance is above 27%; at 27% or below, wager enough for displayed 100%**. With all 136 figurines unlocked, this means **1 shell until 98 figurines are owned, then guarantee each remaining figurine**. The 100% wager is **101 minus the displayed base percentage**.

These are useful comparison options, but **neither is currently a validated recommendation for the requested collect-as-you-go playthrough**. Within the late-cleanup scenario, the threshold rule gives up only **44.72 seconds of expected time**, about 1%, in exchange for a simple wagering rule. The lookup minimizes modeled time in that scenario; the threshold trades a small amount of modeled time for an easier wagering rule. Both estimates use the same reference itinerary, resource assumptions, and modeled restocking decisions; simplifying purchases or changing pickup timing can change the times.

This is a numerical optimum for a stated stochastic resource model, not a ROM-certified universal optimum for every completionist itinerary. Two qualifications matter: the shell ledger contains four reconstructed fusion rewards whose active PAL binary table was unavailable, and an itinerary that forces earlier shell collection can have a different optimum. The included configurable route solver handles such pickup deadlines; it needs that itinerary's actual unlock counts.

## Why these results were downgraded

The original requirement was to collect guaranteed resources when encountered during normal completionist progression. The earlier calculation instead deliberately postpones most optional shell chests until all figurines are unlocked. A first-time player cannot follow that collection rule without advance knowledge of chest contents, and postponement removes the early-game overflow decisions the requested optimization was supposed to solve.

The **74.41-minute lookup result**, **75.15-minute threshold result**, their benchmark comparisons, and their timing/farming sensitivity remain here as calculations for that explicitly different scenario. They are not corrected whole-game estimates, first-time-playthrough recommendations, or proof that the same threshold is optimal with progressive unlocks. The state-based lookup is for the fully unlocked pool and the stated accessible-resource bank; entering inaccessible future pickups would misuse it.

The corrected analysis must retain a normal reference pickup order, collect sources when encountered, apply the available pool at each milestone, and compare early spending with accepting overflow. It must not improve its answer by deliberately avoiding shell chests. That full chronological optimization remains unfinished, so this report does not supply a replacement completion time or early-game policy yet. Fast text speed and holding B, the audited mechanics, and the general Bellman formulation remain applicable independently of this route correction.

## Timing and progression assumptions

The user’s measured pull and purchasing timings assume **text speed set to Fast and holding B to advance dialogue**. The baseline pull duration is `20 + (s−1)/15` seconds under that setup. Slower text or less aggressive dialogue advancement can lengthen completion time. This does not change unlocks or success probabilities, but it need not add the same total delay to every strategy: they have different numbers of pulls and purchases. The ±5-second sensitivity below tests changes to average base pull duration, not every possible dialogue setting.

**Important scope distinction:** progressive unlocks and the physical 999-shell cap are represented in the general model and configurable progression solver, but the **74.41- and 75.15-minute headline results do not include forced early-game spending at smaller unlocked pools**. Their reference itinerary collects only 331 shells before the full pool is unlocked and deliberately postpones the other 3,140 reconstructed shells until postgame cleanup. Subsequent pickups are interleaved with pulls at U=136 to respect the cap.

A completionist route that collects optional shell sources when encountered can exceed the cap before U=136. It must be solved with its actual unlock counts and pickup sequence; the headline times, the 98-owned switch, and the postgame lookup cannot be transferred to that route without further calculation. **An optimized collect-as-you-go progression result has not yet been established.** The progression engine has been implemented and checked on a reduced route, but that is not equivalent to solving and validating the full chronological itinerary requested originally.

For illustration, F=40 with U=50 gives a displayed base of 20%, whereas F=40 with U=136 gives 70%. Earlier successes therefore reduce the displayed base more rapidly. For an early-game threshold rule, compare the current displayed base to the threshold rather than switching unconditionally at 98 owned; whether 27% remains the best threshold for that different itinerary also requires a new solve. Spending before overflow is an optimization choice, not a strict requirement: losing some free shells can sometimes be preferable to extra early pulls. The model must compare both actions.

## Mechanics established from the source

The audit pins zeldaret/tmc revision `6fb6dfb4a7efbe24d0fd1dda5097af6131faacde`, using EU conditional branches. For owned count F and available count U, the displayed base is

\[
b(F,U)=\max\{1,\lfloor100(U-F)/U\rfloor\},\quad F<U.
\]

The legal wager range is 1 through min(S,101−b); the selector stops at displayed 100%. Let h(F) be 15 for F<50, 12 for 50≤F<80, 9 for 80≤F<110, and 6 thereafter. The modeled success chance is

\[
p(F,U,s)=\frac{\max\{h(F),\min(100,b(F,U)+s-1)\}}{100}.
\]

The hidden floor applies **after** adding shells. With base 1% and F≥110, wagers 1–6 all succeed at 6%; wager 7 succeeds at 7%. The draw chooses its success branch by rejecting random values ≥100, then searches cyclically for an eligible owned/unowned figurine. Selection is not uniform across figurine identities. Under nested unlocks, identity does not affect this resource objective: every owned figurine remains available, so F and U suffice for the success chance. Never model pulls with F=U as productive actions. [Machine logic](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c)

Unlocks include twelve conditional entries involving fusions/local flags, in addition to story tiers. Post-credits alone unlocks the six final entries; a completionist run must also satisfy the other conditions to obtain U=136. [Figurine unlock table](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/fileselect.c)

The game uses a deterministic PRNG. This analysis uses the conventional independent-uniform interpretation of its accepted 0–99 draw, not a seed-conditioned prediction of the game's complete frame-by-frame RNG state. No resets, manipulation, or intentional waiting for favorable RNG are included. [PRNG implementation](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/asm/src/code_08000E44.s)

The PAL shop price is 300 rupees for 30 shells. Shells cap at 999; wallet capacities are 100, 300, 500, and 999. [Item prices](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/itemMetaData.c), [inventory caps](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/itemUtils.c)

## Guaranteed shells and the reference itinerary

The reconstructed ledger has 40 included records:

| Sources | Shells | Access gate / timing information |
|---|---:|---|
| Deepwood Shrine, four chests | 50 | First dungeon |
| Eastern Hills bomb cave | 20 | Bombs |
| Stockwell's Minish rafters | 10 | Minish town access |
| Wind Ruins Minish cave | 10 | Ruins access |
| Castor Wilds digging cave | 50 | Mole Mitts |
| Wind Ruins ordinary chest | 50 | Ruins progression |
| Fortress of Winds chest + fixed outer ground item | 81 | Dungeon/Mole Mitts |
| Temple of Droplets frozen chest | 100 | Lantern |
| Town frozen Minish chest | 100 | Flippers and Lantern |
| Town waterfall cave | 200 | Flippers |
| Percy house chest + Percy reward | 200 | Lantern/monster event; reward before gallery completion |
| Castle Garden water chest + two Minish cave chests | 200 | Flippers / Minish access |
| Royal Valley maze secret + Gina grave | 300 | Royal Valley access |
| Lake Hylia north digging cave, two reachable chests | 100 | Roc's Cape and Mole Mitts |
| Lake Hylia beanstalk | 200 | Fusion and Roc's Cape |
| Eastern Hills beanstalk | 200 | Fusion and beanstalk access |
| Veil Falls digging caves, block chest, two cave chests | 300 | Region access; Mitts, bombs, clones/flippers as appropriate |
| Cloud Tops, four chests | 200 | Cloud Tops progression |
| Gregal rescue reward | 100 | Rescue and talk before the normal Cloud Tops visit |
| Magical Boomerang cave shell chest | 200 | Tingle brothers' fusions |
| Four fusion-created chests: Melari path, South Field, North Field, Wind Ruins | 800 | Corresponding fusions and region access |
| **Total reconstructed supply** | **3,471** | |

Excluded: two unused Castle Garden cave rooms (100 each) and the out-of-bounds north Lake Hylia digging-cave chest (50). No random grass, enemy, or pot drops are included. The one fixed outer-Fortress item has an explicit one-time flag and quantity of one.

Most quantities are extracted directly from EU-preprocessed room records. The four 200-shell fusion quantities are reconstructed from documented flags, world-event locations, and commented chest tables. The active region-specific chest table is ROM-extracted binary data, so those four quantities and overall exhaustiveness are not certified against a PAL ROM. Exact earliest fusion milestones are likewise not established for every optional reward. Those limitations are marked in `shell_ledger.csv`. [Room records](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/data/map/entity_headers.s), [documented flags](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/include/flags.h), [fusion world events and chest-table evidence](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/gameData.c)

The retained late-cleanup comparison was calculated for this explicit itinerary; it is not the requested collect-as-you-go route:

1. Collect the four Deepwood chests, rescue/talk to Gregal before Fortress of Winds, collect the Fortress chest and fixed ground item, and collect the Temple of Droplets chest. These provide **331 shells before Vaati**. Make no gallery pulls yet.
2. Complete the main game, wallet upgrades, and all figurine-unlock prerequisites. Visit the remaining optional shell locations during postgame cleanup. Claim Percy's reward before obtaining figurine 136. These provide **3,140 additional shells**.
3. Use the ledger's remaining record order as the cleanup order, with Percy first. Interleave zero-additional-travel Carlov visits between pickups. Do not encounter/open a subsequent source until its pickup fits; use the optimal wagers between sources to make room.

This is a documented reference itinerary, not a claim that a published walkthrough collects every optional chest in this order. Its late optional cleanup is essential to attaining the result. The main-game 331-shell prefix never approaches the cap, and all later collection decisions occur with U=136.

For this itinerary, all remaining free sources are available, every individual pickup is ≤200, and additional travel is assumed free. Define T=S+G, with G the unclaimed supply. T is a **virtual resource balance, not a larger inventory**. Any selected wager is ≤100: if S is insufficient, S<100 and the next ≤200-shell pickup fits; if a pickup does not fit, there are already enough held shells for any legal wager. Thus natural pickup advancement can be interleaved with the policy while retaining the physical 999 cap. Paid acquisition in the delivered feasible policy is allowed once T≤999, so its purchases also fit physical inventory. An additional cash-cap relaxation check tests potentially beneficial earlier purchases.

Guaranteed rupee rewards are not equated with a spendable gallery balance. A reliable net budget would require the timing of wallet upgrades, compulsory/assumed purchases, minigame costs, rewards, and wallet overflow. The permitted conservative fallback is used: **zero outside/free rupees**, including no credit for the 130-figurine reward room. Only duplicates fund the gallery before deliberate farming. Wallet upgrades are complete before the reference route's first pulls. [Percy's conditional reward](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/npc/percy.c), [Gregal's one-time reward](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/data/scripts/cloudTops/script_GregalSick.inc)

## General Bellman formulation

Let x=(j,F,S,R,L) represent route milestone, collection count, held shells, rupees, and location. The milestone contains current U, wallet cap W, future pickup sequence, and relevant progression flags. If unlocks are not nested, replace F with the owned set. Completion has value zero, and

\[
V(x)=\min_{a\in A(x)}\left[c(x,a)+\sum_yP(y\mid x,a)V(y)\right].
\]

For a legal pull at Carlov:

\[
Q_s=20+\frac{s-1}{15}
+p\,V(j,F+1,S-s,R,C)
+(1-p)V(j,F,S-s,\min(W,R+5),C).
\]

A progress/pickup action moves to the next milestone, refreshes unlocks/capacity, and sets S'=min(999,S+g_next). Its additional gallery cost is zero here. Lost shells are explicitly discarded; they do not remain in G. The next milestone can designate entry at the farming area.

A standard restock with q bundles, q∈{1,2,3}, costs

\[
Q_q=H(L,q)+\frac{\max(0,300q-R)}5
+V(j,F,S+30q,\max(0,R-300q),C),
\]

provided purchases fit and 300q≤W. H(C,q)=45+15q; H(farming area,q)=25+15q. Hence zero-cash cycles from Carlov take 120, 195, and 270 seconds. From an already-reached farming area they take 100, 175, and 250 seconds. No outbound Carlov leg is charged in the latter case.

Farming beyond the current cash shortfall cannot help under these specified cycles: it can be deferred to a later visit at the identical marginal rate, while premature funds can be stranded or capped. This reduction depends on keeping the same travel route even for a fully cash-funded purchase. A direct Carlov→shop shortcut, repeated farm/shop shuttles without returning to Carlov, and q-dependent farming-area travel need new measurements and additional location actions; they are not silently priced here.

An early-visit rule is consequently a value comparison, not “always spend the overflow.” Continue if Q_progress≤min_s Q_s; otherwise take the minimizing action and reassess. Waiting increases or preserves success chances at fixed F, but a fixed route's pickups can invalidate waiting through overflow. Buying, discarding a pickup, taking additional early pulls, and delaying until postgame must compete on total time. The route solver permits advance, every feasible wager, and restocking even before the natural supply is exhausted.

## Retained late-cleanup results and scenario policy

All expectations below start with F=0, T=3,471, R=0. Restocking is optimized separately for each benchmark, and displayed-target wagers are used for the 80%/100% policies.

| Policy | Total minutes | Shells consumed | Pulls | Duplicates | Purchased shells | Farmed rupees | Farming minutes | Trips |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Always 1 shell | 173.67 | 521.02 | 521.02 | 385.02 | ≈0 | ≈0 | ≈0 | ≈0 |
| Always displayed 100% | 227.16 | 6,951.00 | 136.00 | 0 | 3,480.00 | 34,800.00 | 116.00 | 39.00 |
| Always at least displayed 80% | 169.53 | 5,621.39 | 166.39 | 30.39 | 2,164.89 | 21,496.94 | 71.66 | 24.42 |
| Best threshold: 1 shell above 27%, otherwise guarantee | 75.15 | 3,484.83 | 211.83 | 75.83 | 28.59 | 11.31 | 0.0377 | 0.842 |
| Arbitrary-wager optimum | **74.41** | **≈3,471.00** | **212.36** | **76.36** | **≈0** | **≈0** | **≈0** | **≈0** |

The natural shells consumed are ≈521.02 for the one-shell policy and ≈3,471 for the other policies. Purchased quantities exceed purchased shells consumed when a policy finishes with leftover stock. Do not subtract every duplicate's 5 rupees from farmed costs unconditionally: the wallet can cap, or the money can remain unspent. The model carries actual balances. A duplicate saves at most one second of future farming, and often saves none in a naturally funded run.

For the optimum, pull/selection time accounts for essentially all 74.41 minutes. The best simple threshold loses only **44.72 seconds**, about 1.0%, and switches at **98 figurines owned**. All thresholds 0–100 were compared; threshold 27 was then checked in the full MDP with discrete purchases and cash carryover.

Some exact postgame examples with **no future natural shells and zero rupees**:

| Owned | Base | Held shells | Action |
|---:|---:|---:|---|
| 27 | 80% | 999 | Wager 1 |
| 68 | 50% | 700 | Wager 1 |
| 108 | 20% | 900 | Wager 1 |
| 122 | 10% | 500 | Wager 1 |
| 127 | 6% | 100 | **Wager 35** → displayed/actual 40% |
| 135 | 1% | 30 | **Wager 30** → actual 30% |

At F=127,S=100,R=0, a 35-shell pull leaves S=65. Both success and failure next select a 90-shell restock, but the failure's 5 rupees reduce the farming requirement from 900 to 895. At F=135,S=30, changing R from 0 to 900 changes the optimal wager from 30 to **20**. These examples rule out an endpoint-only optimizer and a policy indexed just by base chance.

Use the interactive lookup at Carlov with the full pool unlocked. Enter held shells and only genuinely available, still-unclaimed free shells separately. Subtract the wager after every pull; increment F after success or add the capped refund after a duplicate. Collect the next free source if the selected wager exceeds held stock. For a purchase action, buy the indicated number of bundles, farm only the shortfall, and look up again on returning.

If following a different early-collection itinerary, do not enter inaccessible future shells as an available bank. Use `route_solver.cpp` with actual milestone U, source amounts, wallet capacity, and entry location. The whole-game numerical table does not automatically transfer to that itinerary.

Resource sensitivity with no future pickups: F=0,S=999,R=0 gives **136.061 minutes**, ≈1,327.93 shells used, ≈367.20 pulls, ≈231.20 duplicates, ≈328.93 purchased shells, ≈2,133.29 farmed rupees, and ≈3.655 trips. Starting with no shells gives **186.012 minutes**. Full resource sensitivity is included in the metric CSVs.

## Farming method and rate sensitivity

The measured **300 rupees/minute** corresponds to collecting the repeatable 20-rupee pickup immediately left of Link’s front door once every four seconds, resetting it by entering and leaving the house. This method is documented, but its absolute speed optimality has not been established by independent PAL timing. The same guide describes a repeatable Mount Crenel pot farm and reports that the house resets more quickly. [Farming methods](https://gamefaqs.gamespot.com/gba/920670-the-legend-of-zelda-the-minish-cap/faqs/34833)

The most promising alternative to measure is **Yellow Picolyte plus Great Spin in the dense grass southwest of Trilby Highlands**. Yellow Picolyte costs **200 rupees in PAL**, so compare net spendable income after that expense, including buying the dose, travel, harvesting, collecting, and resetting. A 400-rupee gross harvest must complete that repeatable cycle in under 40 seconds to beat the measured house rate; a 500-rupee harvest must take under 60 seconds. Published harvest reports do not establish a reliably faster net rate. A different farm also needs its own gallery/shop travel measurements. [PAL price table](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/itemMetaData.c#L170-L176)

| Policy | Measured 300 R/min | Hypothetical 600 R/min |
|---|---:|---:|
| Always 1 shell | 173.67 min | 173.67 min |
| Always displayed 100% | 227.16 min | 169.16 min |
| Always at least displayed 80% | 169.53 min | 133.70 min |
| Existing 27% threshold | 75.15 min | 75.13 min |
| Arbitrary-wager optimum | **74.41 min** | **74.41 min** |

The benchmark sensitivity figures retain their existing wager and restocking policies; the threshold was not reselected at the faster rate. For the optimized result, a separate solve with effectively instantaneous rupee farming (10³⁰ rupees/second), unchanged travel/purchasing overhead, and the documented cash-cap purchase relaxation returned **4,464.5050125871 seconds**, equal to the baseline at reported precision. Its maximum logged Bellman residual was 1.412×10⁻¹⁰ seconds. Monotonicity therefore brackets the initial optimum for every faster rate between these equal values: **a faster rupee rate alone does not materially change the 74.41-minute scenario result under the late-cleanup route’s 3,471-natural-shell assumptions**. This conclusion does not cover different pickup orders, direct shell farming, or changed travel/purchasing costs.

With fewer natural shells, faster farming changes the optimal wagers and purchases. Reoptimizing F=0, S=999, R=0 with no future pickups at 600 R/min reduces expected completion time from **136.061 to 129.939 minutes**. Expected purchased shells rise from **328.93 to 650.91**, while pulls fall from **367.20 to 325.04**. These additional sensitivity solves use the previously validated solver; they were not separately Monte Carlo simulated.

A practical comparison should time repeated **Carlov → farm → buy 90 shells → Carlov** cycles with equal starting/ending cash and consumable stock. The house baseline from zero usable cash is **270 seconds**. The existing rate model approximates farming continuously; the actual house pickup is discrete. A cash shortfall of 895 rupees requires 45 red pickups (900 rupees), taking 180 rather than 179 seconds at the measured cycle speed and leaving five rupees. The current policy and sensitivity results retain the continuous-rate approximation.

Further evidence, reproduction commands, and unrounded results are in [farming_analysis.md](farming_analysis.md), [farming_sensitivity.csv](farming_sensitivity.csv), and [farming_validation.json](farming_validation.json). The separate `rate_solver.cpp` supports rate sensitivity; the original policy lookup remains based on 300 R/min.

## Pull timing uncertainty of ±5 seconds

Varying the **average base pull time** from 20 seconds to 15 or 25 seconds, while retaining the extra-shell selection term `(s−1)/15`, gives the following reoptimized reference-route results. Farming, travel, purchases, and natural supplies are unchanged.

| Average base pull time | State-based optimum | Simple 27% threshold | Extra time for the simple rule |
|---:|---:|---:|---:|
| 15 seconds | **56.71 min** | 57.50 min | 47.39 seconds |
| 20 seconds | **74.41 min** | 75.15 min | 44.72 seconds |
| 25 seconds | **92.11 min** | 92.81 min | 42.05 seconds |

**Both retained options remain close within the late-cleanup scenario; this does not validate either for the requested chronological route.** Scanning all threshold percentages retains **27%**, switching at **98 figurines owned with the full pool unlocked**, at both endpoints and the baseline. Threshold expected costs are affine in base pull time, so the same best threshold persists throughout the interval in the benchmark calculation. The optimized initial state still averages approximately **212.36 pulls**; each five-second change in their average duration changes the expected total by approximately **17.70 minutes**. Thus the scenario comparison is robust to this timing variation, while the absolute “74–75 minutes” estimate depends materially on the mean timing.

Individual lookup actions can change, particularly when the remaining shells are insufficient. For example, with **135 owned, 30 held shells, zero rupees, and no future pickups**, the optimum is **wager 26** at 15 seconds, **wager 30** at 20 seconds, and **restock 60 shells** at 25 seconds. The included interactive lookup remains the **20-second** policy; it should not be described as an exact policy for every timing in this interval.

If ±5 seconds describes random pull-to-pull variation with the same 20-second mean, independent of outcomes and otherwise consistent with the modeled wager duration, expected completion times remain at the baseline; variability in realized completion time increases. Systematic uncertainty in the average is what the table tests. Changes to the shell-selection speed are a separate sensitivity question.

The 15- and 25-second cases each solve the full 188,876,800-state model, with zero Bellman residual at logging precision (requested tolerance 10⁻⁸ seconds). Independent simulations of 5,000 completions per endpoint agree with the DP results: the 15-second mean is 3,404.14 ± 5.89 seconds and the 25-second mean is 5,528.35 ± 9.71 seconds (95% confidence intervals for the means). These intervals cover both DP values; see [timing_validation.json](timing_validation.json). See [timing_sensitivity.csv](timing_sensitivity.csv) for unrounded results and `timing_solver.cpp` for reproduction:

```sh
clang++ -O3 -std=c++17 timing_solver.cpp -o timing_solver
./timing_solver 3471 optimal pull15 0 default 5 15
./timing_solver 3471 optimal pull25 0 default 5 25
```

## Numerical validation and reproducibility

Policy iteration enumerates every legal integer wager and every one-, two-, or three-bundle purchase. Each selected action has at most one same-count successor; the success branch uses the already-solved next count. Functional-graph cycles are evaluated analytically, rather than cut off after a limited number of duplicates. The solved bank has 188,876,800 states (136 counts × 3,472 resource balances × 400 reachable wallet balances). Requested Bellman tolerance is 10⁻⁸ seconds; reported residuals are below it.

Zero outside rupees, minimum-shortfall farming, refunds in units of five, and the 999 cap generate balances 0 or 4 modulo 5. All 400 such balances are represented exactly, including 999; the lookup deliberately rejects other residues. Arbitrary outside rupees require a larger wallet grid or a separately solved initial residue, not rounding hidden as an exact result.

An additional solve permits cash-funded purchases while the virtual natural balance exceeds 999, at wallet balances 995/999 where a subsequent refund could be capped. Such early purchases can otherwise be deferred until needed without losing cash or changing marginal farming cost. This relaxation makes additional physical-inventory assumptions in the player's favor; its initial value and the delivered feasible policy's value both round to **4,464.5050125871 seconds**. This is an initial-state check, not a claim that every cash-rich state with pending sources has the same optimal action in the two models.

Independent validation includes boundary/cap/timing checks, a 70-state reduced MDP with all 260 actions checked by a linear program, and 20,000 simulations per policy. The small-model value discrepancy is 7.1×10⁻¹⁵ seconds. The optimized simulation mean is 4,463.884 seconds with a 95% mean interval half-width of 3.893 seconds, containing the DP mean. The threshold simulation likewise agrees with the exact evaluation. Simulation error bars concern sampled means, not uncertainty about the game's mechanics or route.

The configurable progression engine was checked against the bank solution for a route that advances from a small pool/100-rupee wallet to U=136, 999 shells, and the full wallet: both give 8,163.686 seconds. The interactive lookup's decompression, initial state, wager changes, purchase response, and completion response passed a runtime unit check. Browser preview of the local file was blocked by the browser's URL policy, so visual browser inspection was not completed.

See `README.md` for build/run commands. No ROM, extracted copyrighted assets, or copied repository source are distributed in the deliverable package. The mathematical/implementation output is original; citations point to the audited public source.
