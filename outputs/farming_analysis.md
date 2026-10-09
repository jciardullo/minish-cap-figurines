# Rupee farming follow-up

Your measured 300 rupees/minute is consistent with collecting a 20-rupee pickup every four seconds. I verified that the house method is documented, but have not independently timed your PAL gameplay or established a global fastest input sequence. It remains a sound measured baseline, not a certified fastest farm.

## Alternatives and evidence

- **Link's house:** dig immediately left of the door, enter and leave the house, repeat. No consumable expense. A firsthand tip in [Kirby021591's guide](https://gamefaqs.gamespot.com/gba/920670-the-legend-of-zelda-the-minish-cap/faqs/34833) describes this method and says its reset is quicker than the Mount Crenel cave. The guide also suggests other yard pickups, but does not give a timed repeatable route through them.
- **Mount Crenel pots:** the same guide describes a repeatable red rupee in the cave with a bomb-operated bridge. No measured evidence establishes an advantage over the house, and the changed gallery/shop travel must be included.
- **Yellow Picolyte + Great Spin in southwest Trilby Highlands:** the guide describes cutting the dense grass field, using a cave to reset it. Reported gross harvests are 340–500 rupees in that guide; [another firsthand report](https://gamefaqs.gamespot.com/boards/920670-the-legend-of-zelda-the-minish-cap/57839459) says about 400. These are reports, not measured expected yields. The [PAL item-price table](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/itemMetaData.c#L170-L176) verifies **200 rupees per Yellow Picolyte**. Net gains are therefore much smaller than gross drops, and random outcomes require repeated trials. This is the most promising alternative to time, but the available evidence does not establish a faster net rate.
- **Anju after completion:** [code](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/cuccoMinigame.c) clamps the level to 9. Its final setup contains one white and two gold Cuccos, worth 110 rupees total, and waits out a 55-second timer before results. Even excluding dialogue, that is at most 120 rupees/minute. Earlier completion rewards are normal-play income, not indefinitely repeatable farming at those levels.

For Yellow Picolyte, compare **net spendable rupees over a complete repeatable cycle**, including buying the dose, travel, cutting, collecting, and resetting. Keep start/end bottle stock and location consistent; account for wallet overflow.

| Gross rupees per dose | Net after 200-rupee dose | Cycle must be shorter than this to beat 300 R/min |
|---:|---:|---:|
| 400 | 200 | 40 seconds |
| 500 | 300 | 60 seconds |
| 600 | 400 | 80 seconds |
| 800 | 600 | 120 seconds |

These are break-even conditions, not verified harvests or speeds. For random cycles, long-run rate is total net income / total elapsed time, not an average of individual cycle ratios.

## Effect on the gallery

The reference route and reconstructed natural-shell total remain conditional as documented in report.md. With 3,471 accessible natural shells, F=0, R=0, and the original travel/purchase assumptions:

| Wager policy | 300 R/min | Hypothetical 600 R/min |
|---|---:|---:|
| Always one shell | 173.67 min | 173.67 min |
| Always displayed 100% | 227.16 min | 169.16 min |
| Always at least displayed 80% | 169.53 min | 133.70 min |
| Existing 27% one-shell/guarantee threshold | 75.15 min | 75.13 min |
| Fully optimized | 74.41 min | 74.41 min |

The benchmark columns rescale the **existing wager and restocking policies**: T_new = T_old - farmed_rupees/5 + farmed_rupees/new_rate. They are feasible expected times, not claims of independently reoptimized restocking or threshold selection at the new rate.

For the optimized row, I additionally **resolved all states with an effectively zero farming cost** (rate 1e30 rupees/sec), allowing the previously documented cash-cap purchase relaxation. Its initial value is **4464.5050125871 seconds**, equal to the original value at reported precision. Maximum reported Bellman residual is 1.41199e-10 seconds, below the 1e-8-second tolerance. Monotonicity brackets every faster farming rate between these equal initial values. Thus a faster rupee rate alone does not materially improve this particular full-natural-supply result. This does not certify all possible farm locations, altered purchase overheads, direct shell farming, or other completionist pickup orders.

Farming matters if fewer natural shells remain. I independently reoptimized the F=0, S=999, R=0, no-future-pickups case at 600 R/min:

| Metric | 300 R/min | 600 R/min |
|---|---:|---:|
| Expected completion time | 136.0614 min | 129.9393 min |
| Shells consumed | 1327.9299 | 1649.9126 |
| Purchased shells | 328.9299 | 650.9126 |
| Pulls | 367.2025 | 325.0363 |
| Duplicates | 231.2025 | 189.0363 |
| Farmed rupees | 2133.2860 | 5563.9450 |
| Farming time | 7.11095 min | 9.27324 min |
| Restocking trips | 3.65478 | 7.23236 |

The faster farm causes the optimizer to buy and wager more shells, so it spends more total time farming while finishing sooner. Reported Bellman residual at 600 R/min is zero at logging precision. This sensitivity calculation was not independently Monte Carlo simulated; it uses the previously validated solver with only the farming-rate cost changed.

## Practical validation

The strongest comparison is a complete **Carlov → farm → buy 90 shells → Carlov** cycle, starting and ending with the same rupee balance. Your current zero-cash baseline is 270 seconds. Repeat the alternative several times and compare total net shells gained per total time. This captures its different travel and consumable costs, rather than carrying over the house's 45-second travel estimate automatically.

For the house alone, 900 rupees requires 45 red pickups, or 180 seconds at your measured four-second cycle. An extra repeatable yard pickup is worthwhile only if its incremental net rupees / incremental time exceeds five rupees/second; an extra red rupee must add less than four seconds.

The previous solver uses continuous farming at a measured average rate. A literal house farm instead produces 20-rupee increments: for cash shortfall d, it needs ceil(d/20) digs and should retain any excess cash. For example, a shortfall of 895 needs 900 rupees of pickups, taking 180 rather than 179 seconds at the assumed cycle speed, and leaving five rupees. The sensitivity figures above preserve the original continuous-rate approximation; they are not an exact discrete-pickup optimization.

## Reproduction

`rate_solver.cpp` is a separate copy of the original solver with an optional rupees/second parameter. It leaves the original lookup and results unchanged.

```sh
clang++ -O3 -std=c++17 rate_solver.cpp -o rate_solver
./rate_solver 999 optimal rate10 0 default 10
./rate_solver 3471 optimal farming_free 0 relax 1e30
```

`farming_sensitivity.csv` contains unrounded same-policy comparisons; `farming_validation.json` contains the two new numerical runs' initial metrics and maximum logged residuals. Source commit: 6fb6dfb4a7efbe24d0fd1dda5097af6131faacde.
