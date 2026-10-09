# Release packaging

The verified original release payload is preserved under `outputs/`. Top-level
paper and guide are exact reader copies. No research computation was rerun.

The original verified reproducibility ZIP is included under `outputs/` and also
distributed as a GitHub release asset. Existing README relative links resolve
without extra file copies.

`SHA256SUMS` covers every published Git payload file except itself and `.git/`.
The Git commit fixes the checksum file itself. Verify from repository root with
`shasum -a 256 -c SHA256SUMS`.

Excluded: repository internals, temporary build/runtime files, local caches,
credentials, and ROMs/game assets.
Historical computation/search logs delivered in the verified bundle are retained
as research evidence; no new scratch logs are included.
