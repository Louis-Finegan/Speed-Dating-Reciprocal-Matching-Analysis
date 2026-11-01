"""Generate regression and observed-network figures."""
import argparse
import json
from pathlib import Path
import numpy as np
from dating_research.dataset import DEFAULT_INPUT, DEFAULT_OUTPUT, FEATURES
from dating_research.source import load_data
from dating_research.figures import regression_figure, network_figure


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT / "figures")
    parser.add_argument("--wave", type=int, help="Network event; defaults to the earliest wave")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)
    data = load_data(args.csv)
    waves = np.random.default_rng(args.seed).permutation(np.sort(data.wave.unique()))
    if len(waves) < 2:
        parser.error("At least two waves are needed for held-out regression evaluation")
    test_waves = waves[:max(1, int(np.ceil(0.25 * len(waves))))]
    train, test = data[~data.wave.isin(test_waves)], data[data.wave.isin(test_waves)]
    if train.dec.nunique() != 2:
        parser.error("Training data must contain both decision classes")
    if train[FEATURES].isna().all().any():
        parser.error("Each predictor needs at least one observed training value")
    wave = args.wave if args.wave is not None else float(data.wave.min())
    if wave not in set(waves):
        parser.error(f"Unknown wave: {wave}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    reference = regression_figure(train, test, args.output_dir)
    network_figure(data, wave, args.output_dir)
    metadata = {"source": str(args.csv), "seed": args.seed,
                "train_waves": sorted(train.wave.unique().tolist()),
                "test_waves": sorted(test_waves.tolist()), "network_wave": wave,
                "regression_reference_values": reference}
    (args.output_dir / "figure_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Saved PNG/PDF figures, plot data and metadata in {args.output_dir}")


if __name__ == "__main__":
    main()
