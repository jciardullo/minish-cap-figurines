# Final wording-only corrections

- Replaced the broken final Limitations discussion with clean prose and removed duplicate claims.
- Removed the unsupported inference attributing much of compact regret to information mismatch from Section 11.4, Conclusion, and the player guide.
- Retained the algebraic decomposition and correct lower-bound inequality; clarified that the true matched-information decomposition is unknown.
- Added the one-wager neighborhood qualification and complexity comparisons: 42 versus 40 PAL, 39 versus 37 NTSC-U.
- Revised the guide’s synthetic-prior paragraph, preserving 0.152%, 0.052%, 6.72%, and 6.20%, the averaging distinction, and unmeasured consultation time.
- Split the baseline definition and numerical comparison into two paragraphs without changing its behavior.

No optimization, search, simulation, enumeration, or policy evaluation was performed. The candidate list, policy IDs, knee criterion, numerical results, player thresholds, reserves, wagers and restocking rules remain unchanged. The final text no longer attributes an unidentified share of regret to information loss.

Both compilers succeeded. The Limitations and Conclusion pages were visually inspected, with no clipping or overflow. Existing numerical and policy files retain their hashes. See wording_verification.json and manifest.json for traceability.
