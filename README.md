# Paper revision reproducibility repository

This repository organizes analyses used to address reviewer comments for the manuscript revision. Each reviewer comment has its own numbered folder containing the proposed reviewer response, exact manuscript changes, and supporting calculations or experiments where needed.

## Notebook convention

Analyses that require code are stored as **Jupyter notebooks (`.ipynb`)** rather than standalone Python scripts so that the code and captured outputs can be inspected together on GitHub.

- When an analysis has actually been executed, the notebook contains the saved output produced by that run.
- When a reviewer request requires a new training experiment or unavailable exact experimental assets, the notebook is explicitly marked **NOT RUN / RUN REQUIRED** and contains no fabricated performance result.
- Supporting CSV/JSON result files are retained when useful for reproducibility.

Examples include the DGraphDTA KIBA correction, DAVIS ablation arithmetic, protein- and ligand-side SMARTS audits, SMARTS-overlap examples, InfoNCE implementation verification, pKd conversion, parameter-count reconciliation, and radar normalization.

`Reviewer_3/MASTER_STATUS.md` provides the comment-by-comment revision status.
