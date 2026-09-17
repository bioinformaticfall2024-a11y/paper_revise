# Run required: graph-only + InfoNCE

Train a two-stream ligand/protein graph model with no vision/AE and symmetric ligand-protein InfoNCE (tau=0.07, alpha=0.5). Use the exact persisted split, optimizer, checkpoint rule and seeds used for the graph-only scaffold. Report MSE, CI, Pearson/Spearman. Do not insert forecast values.
