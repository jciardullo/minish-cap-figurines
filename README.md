# Minish Cap figurines

For a normal completionist playthrough, use the **compact player strategy** at ordinary town visits, collect rewards normally, and begin serious gallery cleanup once all figurines are eligible. It is the recommended practical rule; the simpler memorized knee trades speed for fewer rules.

**[Read the complete player strategy](player_strategy.md)** · **[Read the mathematical paper](paper.pdf)**

## Compact strategy summary

Before full eligibility, enter a session only with at least **700 shells PAL / 800 NTSC-U**, default one-shell chance **at least 20%**, and shells **strictly above** the current reserve. Once started, follow the phase row even if chance drops below 20%; stop at or below reserve. All chance cutoffs below are strict: at equality, choose displayed 100%.

| Recognizable phase | PAL reserve / wager | NTSC-U reserve / wager |
|---|---|---|
| Before Fortress of Winds complete | 600 / one shell above 80%, otherwise displayed 100% | Same |
| Fortress complete, before Water Element | 150 / displayed 100% | 100 / displayed 100% |
| Water Element, before Wind Element | 800 / displayed 100% | Same |
| Wind Element, before full eligibility | 0 / one shell above 15%, otherwise displayed 100% | 0 / one shell above 20%, otherwise displayed 100% |
| All figurines eligible | 0 / one shell above 8%, otherwise displayed 100% | 0 / one shell above 9%, otherwise displayed 100% |

If short of the prescribed wager, spend all held shells. Never farm during early sessions. After full eligibility, restock when empty: buy the maximum already-funded batch, up to three PAL / four NTSC-U bundles. If none are funded, farm only missing money for 900 R PAL / 800 R NTSC-U, then buy 90 / 120 shells. Respect inventory caps. Full eligibility includes completionist side content that unlocks figurines, excluding gallery-dependent rewards. See the complete guide for the full actionable rule and caveats.

## Key modeled results

| Version | Conditional optimum | Recommended compact | Worst-tested compact regret | Memorized knee |
|---|---:|---:|---:|---:|
| PAL / European | 119.41 min | 122.04 min | 8.14% | 130.11 min |
| NTSC-U | 112.78 min | 115.29 min | 7.56% | 122.53 min |

The do-nothing-clever baseline—wait for full eligibility, then always wager one shell with maximum-batch restocking—takes about **173.67 minutes** on the reference route in either version.

## What the paper optimizes

Expected gallery-attributable real-world time to obtain all 136 figurines, including arbitrary legal wagers, progressive unlocks, guaranteed natural shells, capped inventory and duplicate cash, discrete purchases, and measured deliberate farming/restocking costs. Frozen completionist routes provide conditional benchmarks; human rules use observable information.

## Important limitations

Inputs and resource reconstruction are conditional. This is a bounded human-policy search, not an unconditional whole-game optimum. Displayed digits have no directed-rounding proof. The true matched-information optimum is unsolved; **5% is a future-informed diagnostic, not a fair matched-information threshold**. Fast text/B-held measured timings and conservative deliberate farming are assumed. Random drops and natural rupees are excluded. Route robustness is tested, not universal. NTSC adjustment timing is empirical. The paper supplies the complete limitations.

## Repository contents

- `paper.pdf`, `player_strategy.md`: byte-identical frozen Version 1.0 reader copies.
- `outputs/distillation/`: original layout, LaTeX, policy/evaluation code, candidate list, results, and supplemental audits.
- `outputs/corrected/`, `outputs/funded/`, `outputs/policy_lookup/`: frozen inputs, mechanics/resource audits, solver artifacts, and policy data.
- `reproducibility/`: distribution notes and asset checksums.
- `SHA256SUMS`: actual repository payload filenames and hashes (excluding itself and Git metadata).
- `LICENSE-CODE`, `LICENSE-CONTENT`, `CITATION.cff`: publication metadata.

The existing internal layout is preserved to keep reproduction paths valid. No ROM is distributed.

## Reproduction

Run from the repository root. Requires C++17/clang and Python with NumPy/SciPy; plots also require Matplotlib/Pillow.

```sh
mkdir -p work/distillation
clang++ -std=c++17 -O2 outputs/distillation/exact.cpp -o work/distillation/exact
clang++ -std=c++17 -O2 outputs/distillation/screen.cpp -o work/distillation/screen
clang++ -std=c++17 -O2 outputs/distillation/test_policy.cpp -o work/distillation/test_policy
work/distillation/test_policy
python3 outputs/distillation/test_analysis.py
```

Detailed optional computational reproduction is documented in [the original research README](outputs/distillation/README.md). Reproduction jobs were **not rerun** during packaging. Historical paper-generation scripts may overwrite editorial revisions; use a disposable checkout for reproduction. The frozen manuscript source is authoritative. To compile the existing source without regenerating research content:

```sh
tectonic --keep-logs --outdir outputs/distillation outputs/distillation/paper.tex
```

## Version and release status

Manuscript **Version 1.0**, dated **8 October 2026**. This is the first public repository release, tagged `v1.0`. No DOI or archive identifier has been assigned. Publication does not revise the frozen paper's original unassigned-identifier statement.

## Attribution and AI contribution

This project was directed, curated, and published by **jciardullo**. OpenAI ChatGPT was used extensively for mathematical modeling, code and solver development, computational analysis, policy search, interpretation, drafting, LaTeX preparation, and editorial revision.

This is a **human-directed, AI-assisted computational research project**. OpenAI ChatGPT was the only AI collaborator. GPT 6.1 Sol (OpenAI ChatGPT) is credited in the publication commit as AI assistance, not as a human GitHub collaborator account. Responsibility for publication and remaining errors rests with the human project lead. No other human collaborator is added.

## Licensing

Original project source code is licensed under **MIT** ([LICENSE-CODE](LICENSE-CODE)). The paper, player guide, original documentation, original data tables, generated results, and project-created supplemental material are licensed under **CC BY 4.0** ([LICENSE-CONTENT](LICENSE-CONTENT)).

Third-party material remains under its original terms and is not relicensed here. These grants do not imply ownership of upstream decompilation code, walkthrough text, game assets, ROM material, or other third-party works. Nintendo names and marks are not licensed by this repository.
