"""Baseline directional logistic model."""
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build_model():
    return make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                         StandardScaler(), LogisticRegression(max_iter=2000))
