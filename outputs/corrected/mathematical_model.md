# Mathematical model and scope

For a frozen route, let j be the next ordinary gallery opportunity, U_j its nested eligible set, W_j the wallet capacity, and g_j the ordered intervening pickups. The optimizer may know the entire frozen sequence. The player-facing policy cannot query it.

In the nominal, marginalized-RNG model, the state is x=(j,F,S,R,L), where L records a deliberate restocking location when relevant. A count F suffices only when previously eligible sets remain eligible: every success adds one currently eligible unowned figurine, and future success chances depend on F rather than its identities. Otherwise retain the owned set. A hidden-state model would additionally retain an RNG-state distribution, not reveal the state to the practical policy.

For F<U_j, b=max(1,floor(100(U_j−F)/U_j)), h(F)=15,12,9,6 at owned-count boundaries 50,80,110. Legal wagers satisfy 1≤s≤min(S,101−b), and nominal p=max(h(F),b+s−1)/100. Pool exhaustion forbids further productive pulls. V(136,S,R,j)=0.

The stochastic shortest-path equation is V(x)=min_a[c(x,a)+Σ_y P(y|x,a)V(y)]. At an ordinary Carlov opportunity, pull candidates are

Q_s=t(s)+p V(j,F+1,S−s,R)+(1−p)V(j,F,S−s,min(W_j,R+5)).

Progression costs zero additional gallery time. Apply every next-event pickup separately, using retained=min(g,999−S) and lost=g−retained. Resources scheduled later cannot be spent now. Upgrade the wallet when its frozen event occurs.

Farming actions are unavailable before the Mole Mitts milestone; already-funded shop transactions remain distinct.

A deliberate restocking candidate chooses every reachable n≥0 discrete 20-rupee pickups and an affordable capacity-safe B-bundle shop visit. Each farming pickup costs 1200/rate seconds and caps R at W. Each sequential bundle costs the region's price, adds 30 shells, costs 15 seconds, and is forbidden when S+30>999. PAL permits at most three bundles; NTSC-U at most four.

After the user's final travel clarification, a cycle beginning at Carlov costs 20 seconds travel when n=0 (already funded, direct shop visit) and 45 when n>0 (farm visit). A cycle genuinely beginning at the farming area costs 25 seconds travel, omitting Carlov's outbound 20-second leg. Do not infer a farm starting location merely from having zero cash. The current frozen ledgers place all deliberate acquisition decisions at Carlov; their numerical results do not cover an additional farm-entry opportunity. The general equation supports it through L and the appropriate travel edges.

PAL t(s)=base+(s−1)/entry_rate. NTSC t(s)=base+distance(1,s)/entry_rate, using breadth-first shortest paths over legal clamped ±1 and ±10 transitions, with the state-dependent wager limit. Equal physical adjustment times are empirical.

Policy iteration solves the full represented count/shell/cash/progression state. The cash grid is exact for zero initial gallery cash, duplicate payments, regional purchases, and capped discrete farming; it contains residues 0 and 4 modulo 5. Arbitrary cash brought from unrelated ordinary play is outside this conservative grid. Do not interpret the grid as rounding represented balances.

Independent forward occupancy evaluation accumulates expected rewards under the selected policy, including capped refunds and purchase balances. Monte Carlo measures variability and checks those expectations; it does not prove optimality. Numerical certification concerns this stochastic model and frozen input sequence, not the accuracy of human timing measurements or source reconstruction.
