# Exact selected-policy data and observable adapters

Each gzip file contains uint16 little-endian action codes in (owned*400000 + shells*400 + cash_index) order. cash_index=2*floor(R/5)+(R%5==4), for represented cash residues 0 or 4 modulo 5. Codes: 0 progress; 1–100 wager; 101+(bundles−1)+max_bundles*farming_pickups restock. max_bundles is three PAL, four NTSC-U. manifest.json records raw content hashes and sizes.

These are exact compressed selected representatives. They do not encode every full-state tied set or establish uniquely optimal actions. Sampled tied sets remain in the solver CSV exports. The observable adapter uses these data without querying future route events; a sampled action tie may have a simpler equivalent representative.

Use ../gallery_policy.py with current owned count, shells, credited gallery cash, displayed base chance, and the most recent recognizable milestone. Set --begin-visit when entering the gallery; the Wind-stage visit routine is selected from owned count on arrival (<80 or ≥80) and retained for that visit. Milestones are Earth Element, Fire Element, the two-Element sword and subsequent West Hyrule story cutscene (Boots held), completed Fortress of Winds (Mole Mitts held), Water Element, Royal Crypt, Wind Element before final cleanup, and all figurine eligibility requirements completed. No chest identity or future resource input is accepted.

The default is the deterministic reference preset. --balanced --reset samples a preset once for the whole playthrough, independently of the game's RNG, using published minimax weights. Do not resample it after duplicates. This randomized preset is the best tested mixture of seven lookup profiles, not a proof of the best conceivable observable strategy.

Off-grid current rupees are rounded down only to choose an action; the actual balance is retained for feasibility and transaction reporting. Those suggestions are outside the numerical cash-grid certificate. The conservative model itself never rounds a reachable balance.

Full cleanup requires all eligibility unlocks, including optional completionist flags, not just defeating the final boss. Additional unscheduled visits, delayed wallet upgrades, and untested progression states are outside the evaluated route matrix. Lookup consultation time is not included in the supplied pull timings; a real player should account for it.
