# Targeted endpoint and publication audit

The frozen candidate list remains 10,000 entries. Supplemental audit ID 10000 is separate and was never generated or screened. Its maximum-bundle restocking rule matches the endpoint convention. No search or model optimum was rerun.

Complexity: (1,0,0,0,3,0,0,1), C=8. Three clauses distinguish early abstention, postgame one-shell pulls, and restocking; ID 500 shares a universal wager clause and has C=7.

| Region | Reference min | Mean regret % | Worst regret % | Frontier | Knee |
|---|---:|---:|---:|---|---:|
| PAL | 173.67357146 | 47.10119209 | 64.21446973 | added at C=8 | 6457 |
| NTSC-U | 173.67357147 | 55.87578936 | 71.64042062 | dominated | 6098 |

Minimum endpoints and endpoint normalization are unchanged. The supplemental PAL point dominates the previous C=8 and C=9 frontier points; both official knees and all named-policy behavior remain unchanged. `endpoint_status_overlay.json` is authoritative for updated dominance; frozen legacy candidate statuses remain available for provenance. `endpoint_audit.json` includes every scenario and old/new knee geometry.

Table 2 one-shell benchmark has full-route-informed progression/restocking. Its same rounded reference time does not imply matched information or policy equivalence. The supplemental observable policy retains 999 of 3591 natural shells, losing 2592 to the cap; extremely rare purchases remain nonzero.

Pinned figurineDevice.c lines 122 and 247 reset shells to 1 at initial and subsequent selection entry. Frozen wallet caps are exactly 300 and 999.

NTSC-U knee missed_late and missed_postgame raw resource/time totals are equal: 7410.173271365031 seconds, retained 2874, overflow 717, purchased 625.937561567703. Their different optimum denominators produce different regret.

Reproduce from project root (NumPy/SciPy; Matplotlib for plots):
```sh
python3 outputs/distillation/run_endpoint_audit.py
python3 outputs/distillation/repair_endpoint.py
```
The original frontier.py reproduces the pre-audit frozen search; run repair_endpoint.py afterward to apply this documented supplemental point.
