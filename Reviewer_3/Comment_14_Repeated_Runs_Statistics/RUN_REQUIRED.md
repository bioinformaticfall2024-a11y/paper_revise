# Reviewer 3, Comment 14 — status and optional future analyses

**Current status (2026-09-20):** The response and manuscript-edit instructions in `RESPONSE_AND_MANUSCRIPT_CHANGES.txt` reflect the author's stated computational limitations. The five-seed experiments and repeated cold-target splits have **not** been carried out. No new bootstrap confidence interval is reported. The existing single-run FGgraphDTA cold-target summary and previously reported paired t-test remain the only quantitative evidence described in the response.

The notebook `repeated_runs_statistics.ipynb` is an **unexecuted template**, not evidence that five-seed results exist.

## What would be needed to fully meet the reviewer's request in future

- Five independently trained seeds per principal model/dataset configuration, using a clearly documented evaluation protocol. Report mean and sample SD without mixing literature-reported results and in-house matched runs.
- Several independent protein-disjoint train/test splits, or a genuine target-level bootstrap of **actual paired protein-level observations** from the existing held-out proteins. A bootstrap from one split cannot establish split-to-split or training-seed robustness.
- Multiplicity handling or an explicit exploratory/unadjusted label for multiple tests.
- Retained split identifiers, training seeds, per-protein prediction/error records, and reproducible scripts.

**Do not describe any of these analyses as completed or insert hypothetical confidence intervals.** A computational resource explanation is a transparent partial response, not an empirical substitute for the requested runs.
