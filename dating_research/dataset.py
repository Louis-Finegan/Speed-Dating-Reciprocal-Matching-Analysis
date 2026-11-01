"""Shared dataset and output locations, relative to the repository."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "speed_dating_data.csv"
DEFAULT_OUTPUT = ROOT / "results" / "speed_dating"
DEFAULT_URL = (
    "https://www.stat.columbia.edu/~gelman/arm/examples/speed.dating/"
    "Speed%20Dating%20Data.csv"
)
FEATURES = ["age", "age_o", "samerace", "int_corr", "goal"]
REQUIRED_COLUMNS = set(FEATURES + ["wave", "iid", "pid", "gender", "dec", "dec_o", "match"])
