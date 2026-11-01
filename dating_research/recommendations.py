"""Sequential recommendation policies over observed encounters."""
import numpy as np
from .statistics import gini


def make_recommendations(pairs, k, method, seed=42, cap=None):
    rng = np.random.default_rng(seed)
    # Candidate pairs belong to one event and have a designated initiating side (gender=1).
    chosen = []
    exposures = {}
    for (wave, actor), group in pairs.groupby(["wave", "iid"], sort=True):
        if method == "random":
            order = rng.permutation(group.index.to_numpy())
        else:
            order = group.sort_values("score", ascending=False).index.to_numpy()
        count = 0
        for ix in order:
            target = (wave, int(pairs.loc[ix, "pid"]))
            if cap is not None and exposures.get(target, 0) >= cap:
                continue
            chosen.append(ix)
            exposures[target] = exposures.get(target, 0) + 1
            count += 1
            if count >= k:
                break
    out = pairs.loc[chosen]
    all_targets = pairs[["wave", "pid"]].drop_duplicates()
    counts = [exposures.get((row.wave, int(row.pid)), 0)
              for row in all_targets.itertuples(index=False)]
    return {"method": method, "reciprocal_hit_rate": out.match.mean() if len(out) else np.nan,
            "recommendations": len(out), "target_coverage": np.mean(np.asarray(counts) > 0),
            "exposure_gini": gini(counts)}
