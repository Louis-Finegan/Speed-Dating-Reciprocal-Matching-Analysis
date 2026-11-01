"""Load and clean the original Columbia encounter CSV."""
import numpy as np
import pandas as pd
from .dataset import FEATURES


def load_data(filename):
    try:
        df = pd.read_csv(filename, low_memory=False, encoding="utf-8-sig")
    except UnicodeDecodeError:
        # The original dataset contains legacy-encoded questionnaire text.
        df = pd.read_csv(filename, low_memory=False, encoding="latin-1")
    required = FEATURES + ["wave", "iid", "pid", "gender", "dec", "dec_o", "match"]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing columns: {missing}. Use the original Kaggle CSV.")
    for name in required:
        df[name] = pd.to_numeric(df[name], errors="coerce")
    df = df.dropna(subset=["wave", "iid", "pid", "gender", "dec", "dec_o", "match"])
    df = df[df.gender.isin([0, 1]) & df.dec.isin([0, 1])]
    # Generate unordered pair keys; each encounter is represented in both directions.
    df["lo"] = np.minimum(df.iid, df.pid).astype(int)
    df["hi"] = np.maximum(df.iid, df.pid).astype(int)
    df = df.drop_duplicates(["wave", "iid", "pid"])
    return df
