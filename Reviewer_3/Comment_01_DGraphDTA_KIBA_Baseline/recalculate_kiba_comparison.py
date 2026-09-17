"""Recalculate descriptive KIBA differences after correcting the published DGraphDTA row.

Important: these are arithmetic differences between reported values from different
experimental protocols. They must not be interpreted as matched head-to-head effects.
"""

baseline = {"model": "DGraphDTA (published)", "MSE": 0.126, "CI": 0.904, "Pearson": 0.903}
models = [
    {"model": "FGgraphDTA", "MSE": 0.145, "CI": 0.865, "Pearson": 0.873},
    {"model": "PVgraphDTA", "MSE": 0.130, "CI": 0.898, "Pearson": 0.877},
]

for m in models:
    mse_pct = (m["MSE"] - baseline["MSE"]) / baseline["MSE"] * 100
    ci_delta = m["CI"] - baseline["CI"]
    pearson_delta = m["Pearson"] - baseline["Pearson"]
    print(
        f'{m["model"]}: MSE={m["MSE"]:.3f}; '
        f'MSE descriptive difference={mse_pct:+.2f}%; '
        f'CI delta={ci_delta:+.3f}; Pearson delta={pearson_delta:+.3f}'
    )
