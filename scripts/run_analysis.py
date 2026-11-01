"""Evaluate directional interest and reciprocal recommendation policies."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from dating_research.dataset import DEFAULT_INPUT, DEFAULT_OUTPUT, FEATURES
from dating_research.source import load_data
from dating_research.statistics import evaluate
from dating_research.recommendations import make_recommendations
from dating_research.models import build_model


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", "--input", dest="csv", default=DEFAULT_INPUT, type=Path)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args(argv)
    if args.k < 1:
        raise ValueError("k must be >= 1")
    df = load_data(args.csv)
    # Split entire speed-dating events, keeping both directions and participants
    # of the same event on the same side. Generalises to held-out events, not new eras.
    waves = np.sort(df.wave.unique())
    rng = np.random.default_rng(42)
    waves = rng.permutation(waves)
    n_test = max(1, int(np.ceil(0.25 * len(waves))))
    if len(waves) < 2:
        ap.error("At least two waves are needed for held-out evaluation")
    test_waves = set(waves[:n_test])
    train = df[~df.wave.isin(test_waves)].copy()
    test = df[df.wave.isin(test_waves)].copy()
    model = build_model()
    model.fit(train[FEATURES], train.dec.astype(int))
    test["p_yes"] = model.predict_proba(test[FEATURES])[:, 1]
    print("Held-out event results for directional interest:", evaluate(test.dec, test.p_yes))
    # Take only one side (gender=1) and merge observed opposite-direction predictions.
    # 'match' remains the actual held-out mutual yes/no outcome.
    base = test[test.gender == 1].copy()
    reverse = test[["wave", "iid", "pid", "p_yes"]].rename(
        columns={"iid": "pid", "pid": "iid", "p_yes": "reverse_p"})
    pairs = base.merge(reverse, on=["wave", "iid", "pid"], how="inner", validate="one_to_one")
    pairs["score"] = pairs.p_yes * pairs.reverse_p
    if pairs.empty:
        raise ValueError("No reciprocal pairs found in held-out waves")
    print("Held-out mutual-interest results:", evaluate(pairs.match, pairs.score))
    results = [make_recommendations(pairs, args.k, "random")]
    results.append(make_recommendations(pairs, args.k, "reciprocal"))
    results.append(make_recommendations(pairs, args.k, "capacity_constrained", cap=args.k))
    result_df = pd.DataFrame(results)
    print("\nRecommendation comparison (only observed encounters):")
    print(result_df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    args.output.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(args.output / "recommendation_results.csv", index=False)

if __name__ == "__main__":
    main()
