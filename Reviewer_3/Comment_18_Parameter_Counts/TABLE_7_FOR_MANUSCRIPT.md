# Replacement Table 7 — Reviewer 3, Comment 18

**Status:** Draft for transfer into the manuscript. Counts are calculated from the recovered/reconstructed layer dimensions; confirm against the exact models that produced the reported experimental results before submission. The author confirmed that the ResNet-101 backbone weights were frozen during DTA training. Earlier historical implementation notes conflict with that confirmation and require checking against the original training notebook.

**Table 7.** Parameter counts of the DGraphDTA-style baseline, FGgraphDTA and PVgraphDTA, distinguishing trainable predictor parameters, frozen visual-backbone parameters and separately trained auxiliary parameters.

| Model | Trainable DTA parameters | Frozen ResNet-101 | Separately trained AE | DTA model total | All components |
|:--|--:|--:|--:|--:|--:|
| DGraphDTA-style baseline | 1,693,525 | — | — | 1,693,525 | 1,693,525 |
| FGgraphDTA | 1,924,525 | — | — | 1,924,525 | 1,924,525 |
| PVgraphDTA | 2,136,405 | 42,500,160 | 17,627,698 | 44,636,565 | 62,264,263 |

**Table note:** "DTA model total" includes trainable DTA predictor parameters and frozen ResNet parameters required to extract image features during online DTA prediction. "All components" additionally includes the independently trained AE, whose precomputed 128-dimensional protein features are fixed during DTA training and which is not part of the online prediction forward pass when stored AE features are used. The ResNet-101 classifier is replaced with an identity layer: 44,549,160 − (2048 × 1000 + 1000) = 42,500,160 backbone parameters. Do not label the old predictor-plus-AE subtotal (19,764,103) as "full pipeline"; it omits the visual backbone. The "All components" count is an architectural inventory, not a count of simultaneously trainable parameters or a measurement of wall-clock training cost.

**Placement:** Replace the old computational complexity Table 7 in Experimental Setup. The exact replacement paragraph and the complete reviewer response are in [RESPONSE_AND_MANUSCRIPT_CHANGES.txt](RESPONSE_AND_MANUSCRIPT_CHANGES.txt). Calculations are archived in [count_parameters_analytical.ipynb](count_parameters_analytical.ipynb) and [parameter_counts.json](parameter_counts.json). No affinity-prediction model was trained to produce these counts.
