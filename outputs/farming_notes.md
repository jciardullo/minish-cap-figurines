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

## Current modeling treatment

The collect-as-you-go solver uses literal 20-rupee farming pickups: four seconds each at 300 rupees/minute, 4.8 seconds at 250, and approximately 3.429 seconds at 350. Duplicate refunds and any excess cash are carried forward; wallet overflow is discarded.

A trip requiring farming costs 45 seconds travel when starting at Carlov. An already-funded direct shop round trip costs the user's subsequently confirmed 20 seconds. Purchasing costs 15 seconds per bundle. PAL permits three bundles at 300 rupees each; NTSC-U permits four at 200 each. A true farm-entry cycle omits the Carlov outbound leg.

The older farming_analysis.md numerical tables are historical late-cleanup comparisons and retain their former continuous-farming approximation. They do not establish the collect-as-you-go completion time or prove the house method globally fastest.
