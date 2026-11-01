"""Prediction metrics and recipient exposure inequality."""
import numpy as np
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score


def gini(values):
    x = np.asarray(values, dtype=float)
    if len(x) == 0 or x.sum() == 0:
        return 0.0
    return np.abs(x[:, None] - x[None, :]).sum() / (2 * len(x) * x.sum())



def evaluate(y, p):
    return {"AP": average_precision_score(y, p),
            "AUC": roc_auc_score(y, p) if len(set(y)) > 1 else float("nan"),
            "Brier": brier_score_loss(y, p)}
