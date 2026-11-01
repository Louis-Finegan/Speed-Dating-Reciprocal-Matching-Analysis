"""Download missing input, run recommendations, and generate figures."""
import argparse
from pathlib import Path
from dating_research.dataset import DEFAULT_INPUT, DEFAULT_OUTPUT
from scripts.download_data import download_data
from scripts.run_analysis import main as run_analysis
from scripts.plot_figures import main as plot_figures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--k", type=int, default=3)
    args = parser.parse_args()
    if args.k < 1:
        parser.error("--k must be at least 1")
    if not args.input.exists():
        if args.input != DEFAULT_INPUT:
            parser.error(f"Input does not exist: {args.input}")
        download_data(args.input)
    run_analysis(["--csv", str(args.input), "--output", str(args.output), "--k", str(args.k)])
    plot_figures(["--csv", str(args.input), "--output-dir", str(args.output / "figures")])


if __name__ == "__main__":
    main()
