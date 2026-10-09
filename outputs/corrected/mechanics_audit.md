# Verified figurine mechanics

Audit revision: `6fb6dfb4a7efbe24d0fd1dda5097af6131faacde` of the public European/US decompilation. The source checkout contains conditional regional code, not an independently verified extracted PAL ROM chest database.

| Mechanic | Verified behavior | Evidence |
|---|---|---|
| Displayed base chance | Integer truncation of 100(U−F)/U; productive minimum 1 | [figurineDevice.c, base calculation](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L580) |
| Wager default and limits | Starts at one; held shells and displayed 100% bound adjustments | [menu and adjustment code](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L247) |
| Regional controls | European ±1; US ±1 or held-R ±10; boundary clamping | [regional controls](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L266) |
| Hidden floors | 15% below 50 owned; 12% at 50–79; 9% at 80–109; 6% at 110+ | [floor function](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L678) |
| RNG calls | Rejection-sample Random() low seven bits until below 100, then one selection draw | [draw routine](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L621) |
| Selection | Starting index 1–128; cyclic scan through 1–136 for eligible unowned or owned figure | [selection scan](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L636) |
| Duplicate refund | Five rupees | [payout](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L789) |
| Wallet cap | Refunds capped by upgraded wallet capacity | [ModRupees](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/gameUtils.c#L220) |
| Shell cap | 999 | [ModShells](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/itemUtils.c#L215) |
| Prices | 30 shells for 300 PAL rupees; 200 US rupees | [regional item price](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/itemMetaData.c#L235) |
| Eligibility | Story-stage comparison, local visited/boss flags, specific fusions and composites | [eligibility function](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L499), [regional table](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/fileselect.c#L51) |
| Generator transition | Multiply state by three modulo 2^32, rotate right 13; output state shifted right one | [Random assembly](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/asm/src/code_08000E44.s), [boot initialization](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/main.c#L50) |

The success probability max(hidden floor, displayed chance)/100 is the nominal reduced-model probability. Deterministic PRNG rejection and history correlations are tested separately; do not equate the nominal expression with a proved conditional probability for every hidden game state.

The eligible sets in every frozen route are explicitly tested as nested. Within those sequences, nonuniform figure identity selection does not invalidate a count-based state: every success adds exactly one eligible unowned figure, and previously acquired figures remain eligible. The general formulation must retain an owned set if a different eligibility sequence fails nesting.

Defeating Vaati is an important final story unlock, but full eligibility also depends on optional flags/fusions. A casual player who has not fulfilled those requirements should not assume a pool of 136 solely because the final boss is defeated.

NTSC input counts use the directed, clamped legal-state graph. Target 20 needs three inputs when 21 is legal (1→11→21→20), but only two when the wager cap itself is 20 (1→11→20). Each target is solved directly by breadth-first search. Equal physical durations for ±10 and ±1 are a modeling assumption, not a code fact.

The generator's boot orbit was independently enumerated as 822,119,800 states, returning to 0x1234567. Uniform sampling of all nonzero 32-bit states consequently includes other orbits. Both that distribution and uniform positions on the boot orbit are documented tests, not measured ordinary-play entry distributions. The full game also advances RNG between gallery visits; isolated-machine and fixed-gap tests do not reconstruct those calls.

The stage-2 flag is the West Hyrule story cutscene involving King Daltus, not Boots possession alone. Stage 3 requires Fortress of Winds completion, not merely finding the Mole Mitts. The helper labels those recognizable gameplay milestones explicitly. Frozen route chapter titles abbreviate these prerequisite assumptions.

Natural shell rewards also have completion conditions. Cucco shell prizes are skipped after hasAllFigurines; the general item-get routine substitutes 50 rupees for shells after that flag. The flag is set at 136, not the pre-ending 130-figurine dialogue. All frozen ledgers collect their shell sources before the final gallery completion, so these conditions do not change their recorded quantities. [Cucco reward condition](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/cuccoMinigame.c#L212), [item-get substitution](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/playerItemUtils.c#L34), [136-figurine flag](https://github.com/zeldaret/tmc/blob/6fb6dfb4a7efbe24d0fd1dda5097af6131faacde/src/object/figurineDevice.c#L709).
