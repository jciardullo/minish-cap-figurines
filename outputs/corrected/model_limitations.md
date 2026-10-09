# Limitations and stopping standard

Human execution is represented by measured average timings. Individual mistakes, pauses, menu hesitation, routing errors, and execution variance are not modeled directly except through timing-sensitivity analysis. Fast text speed and holding B are assumed. Different pull counts mean a common change in dialogue duration does not cancel between strategies.

Random overworld Mysterious Shell and rupee drops are excluded. A real player may therefore require less deliberate farming than the conservative model predicts.

Naturally encountered rupees are not credited. Reported farming represents the conservative case in which purchase funding beyond retained duplicate payouts must be deliberately earned. Existing rupees can reduce farming, but discrete pickups, wallet caps, and purchase boundaries prevent an exact universal continuous-time subtraction rule.

Route robustness is empirical, not universal. Several plausible routes and missed-pickup/backtracking variants demonstrate performance only across the tested cases. A frozen shell-event ledger does not prove every first encounter of a complete item-by-item 100% itinerary. Four chest amounts and several optional availability assignments remain conditional source inputs.

NTSC ±10 wager-entry timing remains an empirical assumption until directly measured. Conclusions materially depending on it are timing-model dependent.

PRNG validation distinguishes verified machine calls/transitions from the unknown ordinary-play entry-state distribution. Uniform nonzero initial states and the optional 1,200-call inter-pull gap are explicit simulation assumptions. They do not reproduce a full casual playthrough. The nominal IID Bellman solution is an optimum under its reduced stochastic model; supplied-state PRNG simulation checks whether that reduction appears practically adequate under the stated distributions.

All presently frozen deliberate acquisition cycles begin at Carlov. A genuine farm-entry opportunity would omit the outbound 20-second leg; it requires an explicit additional input event and is not silently assumed in numerical results.

Numerical residuals of 10^-6 and 10^-7 seconds measure solver error, not model accuracy. Whole-second timing measurements cannot become microsecond-accurate through optimization. Numerically tied actions must not be presented as uniquely optimal; sampled tie exports do not constitute full-state tied-action coverage.

The practical-policy screening criterion is 5% expected-time regret against each corresponding nominal route/version optimum. Report absolute seconds as well. A strict numerical miss remains a miss, even when physically insignificant. Once the specified scenario families and timing axes have been evaluated, stop adding speculative cases. If no memorable rule meets the screen, report that result and distinguish the best tested simpler rule from a more complex lookup. Do not declare universal optimality among all possible observable policies.
