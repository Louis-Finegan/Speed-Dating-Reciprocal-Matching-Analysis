"""Compatibility entry point; prefer python -m scripts.run_analysis."""
from dating_research.dataset import FEATURES
from dating_research.source import load_data
from dating_research.statistics import evaluate, gini
from dating_research.recommendations import make_recommendations
from scripts.run_analysis import main

if __name__ == "__main__":
    raise SystemExit(main())
