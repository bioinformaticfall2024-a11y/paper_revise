# Reviewer Comment 08 — Ligand FG20 SMARTS coverage audit

This folder contains the reproducible code used to address Reviewer 3, Comment 8 concerning ligand-side functional-group coverage in FGgraphDTA.

The script applies the **exact 20 published FG20 SMARTS patterns** at the molecule level to the DAVIS and KIBA ligand sets. It also reproduces the reviewer's six-inhibitor check when the standard DAVIS identifiers are present, and reports diagnostic frequencies for additional kinase-relevant motifs mentioned in the review.

## Main quantities reported

- Number of FG20 patterns observed at least once in each dataset.
- Dataset-wide vocabulary usage: `patterns observed / 20 × 100`.
- Number of active FG20 patterns per ligand (mean, median, IQR, min, max).
- Ligands with zero FG20 matches.
- Per-pattern frequencies.
- Unique FG20 signatures.
- Diagnostic motif frequencies for heteroaromatic N, sulfonamide, aryl-F, aryl-Cl, CF3, urea, morpholine, acrylamide-like warheads, and hydroxamate-like groups.
- Direct reproduction of the six compounds discussed by the reviewer.

## Run

```bash
pip install -r requirements.txt
python audit_smarts_coverage.py \
  --davis /path/to/davis_ligands_file \
  --kiba /path/to/kiba_ligands_file \
  --outdir results
```

Accepted ligand-file formats are:

1. JSON dictionary: `{ "drug_id": "SMILES", ... }`
2. Whitespace-delimited text: one `drug_id SMILES` pair per line.

Use the **exact DAVIS and KIBA ligand files used in the manuscript experiments** when generating the final reviewer-facing numbers.

## Interpretation used in the response

The reviewer's six-compound result measures vocabulary usage within a selected six-drug panel. Dataset-wide vocabulary usage is a different quantity: it asks how many of the 20 FG20 patterns occur at least once anywhere in the complete benchmark ligand set. The two quantities should not be interpreted as the fraction of FG20 bits active in an average molecule.

FG20 is treated as an **auxiliary, non-mutually-exclusive functional-group annotation**, not as a comprehensive kinase-pharmacophore ontology. The original atom-level graph representation remains available to the GNN even when a medicinal-chemistry motif has no dedicated FG20 bit.
