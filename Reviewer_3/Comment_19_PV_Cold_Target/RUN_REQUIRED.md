# PVgraphDTA cold-target run required

Use the same persisted protein-disjoint split as DGraphDTA/FGgraphDTA. Train AE only on training-target contact maps for a strictly inductive PV run, then freeze it before validation/test embeddings. Prefer seeds 11,22,33,44,55. Report MSE, CI, Spearman and Pearson. No forecast numbers.
