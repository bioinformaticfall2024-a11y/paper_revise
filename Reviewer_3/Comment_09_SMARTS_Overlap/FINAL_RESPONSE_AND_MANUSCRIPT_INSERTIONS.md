# Reviewer 3 — Comment 9: SMARTS Pattern Overlap

**Status:** Draft response and manuscript insertions. No architecture, training code, SMARTS input features, or reported model results were modified by adding this document. The requested before/after model-performance ablation has **not** been performed.

## 1. Response to Reviewer 3

**Comment 9: SMARTS Pattern Overlap and False-Positive Assignments**

**Response:**

We thank the reviewer for the detailed examination of the SMARTS definitions and for highlighting the overlapping assignments between carboxylic acid and alcohol groups and between ester and ether groups.

To investigate this concern, we performed an additional RDKit-based diagnostic analysis using representative molecules, including acetic acid, aspirin, and ethyl acetate. The analysis confirmed that the original SMARTS definitions permit the hydroxyl group of a carboxylic acid to activate the alcohol indicator and the bridging oxygen of an ester to activate the ether indicator. We also confirmed that the precedence rules applied to the molecule-level functional-group summary do not automatically eliminate these overlaps from the default atom-level FG20 representation. We acknowledge that this distinction was not sufficiently clarified in the original manuscript.

Nevertheless, we would like to emphasize that the proposed functional-group representation is incorporated as an auxiliary feature set alongside the original atom-level descriptors and molecular graph topology, rather than serving as an exclusive chemical classification system. The overlapping SMARTS assignments therefore do not remove the underlying structural information or make the corresponding chemical environments indistinguishable.

For example, a carboxylic acid retains its specific carboxylic-acid indicator in addition to the general alcohol indicator, while an ester retains its ester-specific indicator alongside the ether indicator. Furthermore, the original molecular graph preserves atom identities, bonding patterns, and local chemical environments, allowing the model to distinguish these chemical structures beyond their auxiliary functional-group annotations.

We agree that introducing more restrictive SMARTS definitions or atom-specific precedence rules would improve the chemical specificity of the functional-group representation. However, modifying the feature definitions would change the input representation used in the reported experiments and would require retraining under the same experimental conditions to determine the effect on predictive performance.

In the present revision, we have retained the original model architecture, feature definitions, and reported experimental results to maintain consistency with the evaluated implementation. We do not claim that the overlapping assignments are chemically optimal or that their effect on predictive performance has been excluded. The requested before-and-after performance ablation has therefore not been performed.

Instead, we have revised the manuscript to clarify the distinction between the atom-level functional-group encoding and the molecule-level refinement procedure and to explicitly acknowledge the overlapping SMARTS assignments as a limitation of the current representation. We have also identified atom-specific SMARTS refinement and controlled comparison of the original and corrected feature definitions as directions for future investigation.

The RDKit-based diagnostic analysis and representative molecular examples are provided in the accompanying reproducibility repository.

## 2. What to add to the manuscript and where

### Addition 1 — Methods: Functional-group assignment

**Where:** Proposed Methodology → FGgraphDTA → Functional-group feature extraction. Insert immediately after the existing description of SMARTS-based assignment and phenol–alcohol refinement.

> The functional-group indicators are incorporated as auxiliary atom-level descriptors rather than mutually exclusive chemical classifications. Because the SMARTS patterns are evaluated independently, an atom may receive multiple functional-group annotations. The precedence rules applied to the molecule-level functional-group summary do not automatically modify the atom-level FG20 features used as model inputs. Consequently, the original atom-level representation may contain overlapping assignments between carboxylic acid and alcohol groups or between ester and ether groups.

### Addition 2 — Discussion: Functional-group limitations

**Where:** Discussion → Limitations and Future Directions. Place alongside the existing representation limitations; it may be combined with the discussion responding to Comments 7 and 8.

> A limitation of the current functional-group representation is the occurrence of overlapping SMARTS assignments, particularly between carboxylic acid and alcohol groups and between ester and ether groups. Although the corresponding chemical environments remain distinguishable through their specific functional-group indicators and the underlying molecular graph features, these overlaps reduce the chemical specificity of the auxiliary annotations. The effect of correcting these assignments on predictive performance has not been evaluated. Future work will investigate atom-specific SMARTS refinement and compare the original and corrected representations under matched training and evaluation conditions.

## Evidence and submission notes

- Supporting audit: [audit_ligand_input_path.ipynb](audit_ligand_input_path.ipynb), [audit_overlap_examples.ipynb](audit_overlap_examples.ipynb), and [example_matches.csv](example_matches.csv).
- The audit inspected a reconstructed preprocessing implementation. Confirm the atom-level input path against the original training notebooks or saved model-input tensors before describing this as an inspection of the exact historical trained-run features.
- **Before sending the response letter, insert the two passages into the actual revised manuscript.** “We have revised the manuscript” is appropriate only after doing so.
- The diagnostic before/after SMARTS annotations do not constitute the requested before/after model-performance ablation. Do not claim performance is unaffected or that corrected-input training was conducted.
