# Reviewer 3 - Master status for all 27 comments

This repository separates verified analytical/source checks from experiments that still require real training or original artifacts. No unperformed model result is represented as completed.

| Comment | Status | Folder |
|---:|---|---|
| 1 | Verified source; edit only | `Comment_01_DGraphDTA_KIBA_Baseline/` |
| 2 | Verified source; edit only | `Comment_02_GraphDTA_KIBA_Variant/` |
| 3 | Relabel literature/provenance | `Comment_03_Reproduced_Label_Provenance/` |
| 4 | Rewrite abstract | `Comment_04_Abstract_Claims/` |
| 5 | Arithmetic verified; negative result text | `Comment_05_PV_DAVIS_Negative/` |
| 6 | Protocol/provenance correction | `Comment_06_Baseline_Protocol_Comparability/` |
| 7 | RDKit audit completed | `Comment_07_Protein_FG_Redundancy/` |
| 8 | Completed earlier | `Comment_08_Ligand_SMARTS_Coverage/` |
| 9 | Diagnostic completed; corrected-model retraining still required | `Comment_09_SMARTS_Overlap/` |
| 10 | Recommend remove unsupported K10/K30 table | `Comment_10_K30_Vocabulary/` |
| 11 | Code behavior verified; Methods correction | `Comment_11_Atom_Level_SMARTS_Assignment/` |
| 12 | NEW TRAINING REQUIRED | `Comment_12_Contrastive_Control/` |
| 13 | Implementation verified; equation correction | `Comment_13_InfoNCE_Denominator/` |
| 14 | 5-SEED/SPLIT STATISTICS REQUIRED | `Comment_14_Repeated_Runs_Statistics/` |
| 15 | ORIGINAL COHORT/FILTER ARTIFACTS REQUIRED | `Comment_15_DAVIS_Cohort_Filtering/` |
| 16 | Threshold verified; provenance clarification | `Comment_16_Contact_Threshold_AE_Transductive/` |
| 17 | Formula verified | `Comment_17_pKd_Conversion/` |
| 18 | Parameter audit + replacement Table 7 and response drafted; author confirms ResNet frozen; original run documentation must be reconciled | `Comment_18_Parameter_Counts/` |
| 19 | Resource-limited reviewer response + manuscript limitation drafted; PV cold-target experiment NOT RUN | `Comment_19_PV_Cold_Target/` |
| 20 | ALPHAFOLD COMPARISON RUN REQUIRED | `Comment_20_AlphaFold_Contact_Map/` |
| 21 | Source-checked; disclosure/text edit | `Comment_21_NLB_DTA_Disclosure/` |
| 22 | Editorial correction | `Comment_22_Numbering_Artifacts/` |
| 23 | Reference correction | `Comment_23_Reference_Corrections/` |
| 24 | Copy-edit | `Comment_24_Grammar_Copyedit/` |
| 25 | Disclosure correction; must reflect actual AI use | `Comment_25_AI_Disclosure/` |
| 26 | Normalization definition/code check | `Comment_26_Radar_Normalization/` |
| 27 | Minor edits + real Zenodo DOI required | `Comment_27_Minor_Reproducibility_Items/` |

## Highest-risk items before submission

- Comment 9: corrected SMARTS performance ablation requires retraining if you want to claim before/after performance.
- Comment 12: graph-only + InfoNCE control requires training.
- Comment 14: five-seed main results and stronger cold-target uncertainty analysis require training/results.
- Comment 15: exact cohort/filter provenance must be recovered from the actual run artifacts.
- Comment 18: author confirms frozen ResNet-101 weights; reconcile the conflicting historical fine-tuning note against the original result-producing notebook and verify the exact parameter counts before submission.
- Comment 19: reviewer response and limitation paragraph drafted under stated computational constraints; PVgraphDTA cold-target remains untested and requires a real training run for direct unseen-target claims.
- Comment 20: AlphaFold-derived contact-map comparison requires structures and training.
- Comment 27: a real persistent DOI must be created; do not use a placeholder as if completed.

## Already executed analytical checks

- Comment 5: DAVIS PV ablation arithmetic.
- Comment 7: exact RDKit protein-side FG coverage/discriminability audit.
- Comment 8: full ligand-side SMARTS coverage audit (existing folder in GitHub).
- Comment 9: exact SMARTS overlap/false-positive diagnostics.
- Comment 13: source-code verification of cross-modal InfoNCE implementation.
- Comment 17: pKd conversion check/examples.
- Comment 18: exact analytical parameter counting from recovered layer dimensions.
- Comment 26: unambiguous radar MSE transform utility.
