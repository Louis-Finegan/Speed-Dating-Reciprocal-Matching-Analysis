"""Generate regression and observed-network figures from the speed-dating CSV."""

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve

from .dataset import FEATURES
from .source import load_data
from .models import build_model


def save_figure(fig, directory, name):
    for extension in ("png", "pdf"):
        fig.savefig(directory / f"{name}.{extension}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def regression_figure(train, test, directory):
    """Use the baseline pipeline; vary age while fixing other predictors."""
    model = build_model()
    model.fit(train[FEATURES], train.dec.astype(int))
    reference = train[FEATURES].median()
    reference["goal"] = train.goal.mode().iloc[0]
    reference["samerace"] = train.samerace.mode().iloc[0]
    ages = np.linspace(train.age.min(), train.age.max(), 200)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout="constrained")
    curves = []
    for quantile in (0.25, 0.5, 0.75):
        partner_age = float(train.age_o.quantile(quantile))
        grid = pd.DataFrame([reference.to_dict()] * len(ages), columns=FEATURES)
        grid["age"] = ages
        grid["age_o"] = partner_age
        probabilities = model.predict_proba(grid)[:, 1]
        axes[0].plot(ages, probabilities, label=f"Partner age {partner_age:g} (Q{int(quantile*100)})")
        curves.append(pd.DataFrame({"age": ages, "partner_age": partner_age,
                                    "predicted_probability": probabilities}))
    axes[0].set(xlabel="Participant age", ylabel="Predicted directional interest",
                ylim=(0, 1), title="Adjusted logistic regression curves")
    axes[0].legend(fontsize=8)
    predicted = model.predict_proba(test[FEATURES])[:, 1]
    observed, mean_prediction = calibration_curve(test.dec, predicted, n_bins=8, strategy="quantile")
    axes[1].plot([0, 1], [0, 1], "--", color="0.6", label="Perfect calibration")
    axes[1].plot(mean_prediction, observed, "o-", label="Held-out encounters")
    axes[1].set(xlabel="Mean predicted probability", ylabel="Observed positive fraction",
                xlim=(0, 1), ylim=(0, 1), title="Held-out directional calibration")
    axes[1].legend(fontsize=8)
    for ax in axes:
        ax.grid(alpha=0.2)
    save_figure(fig, directory, "regression")
    pd.concat(curves, ignore_index=True).to_csv(directory / "regression_curves.csv", index=False)
    pd.DataFrame({"mean_prediction": mean_prediction, "observed_fraction": observed}).to_csv(
        directory / "calibration_bins.csv", index=False)
    test[["wave", "iid", "pid", "dec"]].assign(predicted_probability=predicted).to_csv(
        directory / "held_out_predictions.csv", index=False)
    mutual_interest_figure(model, train, test, reference, directory)
    return {key: float(value) for key, value in reference.items()}


def mutual_interest_figure(model, train, test, reference, directory):
    """Plot the reciprocal product score, not a separately fitted mutual model."""
    ages = np.linspace(train.age.min(), train.age.max(), 200)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout="constrained")
    curves = []
    for quantile in (0.25, 0.5, 0.75):
        partner_age = float(train.age_o.quantile(quantile))
        forward = pd.DataFrame([reference.to_dict()] * len(ages), columns=FEATURES)
        forward["age"] = ages
        forward["age_o"] = partner_age
        reverse = forward.copy()
        reverse["age"] = partner_age
        reverse["age_o"] = ages
        # Both hypothetical participants have the reference goal; shared pair
        # attributes remain fixed in both directions.
        probability = model.predict_proba(forward)[:, 1] * model.predict_proba(reverse)[:, 1]
        axes[0].plot(ages, probability, label=f"Partner age {partner_age:g} (Q{int(quantile*100)})")
        curves.append(pd.DataFrame({"age": ages, "partner_age": partner_age,
                                    "predicted_mutual_probability": probability}))
    axes[0].set(xlabel="Participant age", ylabel="Predicted mutual-interest probability",
                ylim=(0, 1), title="Adjusted reciprocal probability curves")
    axes[0].legend(fontsize=8)

    scored = test.copy()
    scored["p_yes"] = model.predict_proba(scored[FEATURES])[:, 1]
    reverse = scored[["wave", "iid", "pid", "gender", "dec", "p_yes"]].rename(
        columns={"iid": "pid", "pid": "iid", "gender": "partner_gender",
                 "dec": "reverse_dec", "p_yes": "reverse_probability"})
    pairs = scored[scored.gender == 1].merge(
        reverse, on=["wave", "iid", "pid"], validate="one_to_one")
    pairs = pairs[pairs.partner_gender == 0].copy()
    if pairs.empty:
        raise ValueError("No eligible held-out reciprocal encounters for mutual calibration")
    if not (pairs.match.isin([0, 1]) & (pairs.match == pairs.dec * pairs.reverse_dec)).all():
        raise ValueError("Held-out mutual labels disagree with paired directional decisions")
    pairs["predicted_mutual_probability"] = pairs.p_yes * pairs.reverse_probability
    observed, mean_prediction = calibration_curve(
        pairs.match, pairs.predicted_mutual_probability, n_bins=8, strategy="quantile")
    axes[1].plot([0, 1], [0, 1], "--", color="0.6", label="Perfect calibration")
    axes[1].plot(mean_prediction, observed, "o-", label="Held-out mutual decisions")
    axes[1].set(xlabel="Mean predicted mutual probability", ylabel="Observed mutual-interest fraction",
                xlim=(0, 1), ylim=(0, 1), title="Held-out mutual calibration")
    axes[1].legend(fontsize=8)
    for ax in axes:
        ax.grid(alpha=0.2)
    fig.suptitle("Mutual interest: product of two directional logistic predictions")
    save_figure(fig, directory, "mutual_interest_regression")
    pd.concat(curves, ignore_index=True).to_csv(directory / "mutual_interest_curves.csv", index=False)
    pd.DataFrame({"mean_prediction": mean_prediction, "observed_fraction": observed}).to_csv(
        directory / "mutual_calibration_bins.csv", index=False)
    pairs[["wave", "iid", "pid", "match", "p_yes", "reverse_probability",
           "predicted_mutual_probability"]].to_csv(directory / "held_out_mutual_predictions.csv", index=False)


def network_figure(data, wave, directory):
    """Draw one event's encounter graph and observed mutual-interest subgraph."""
    event = data[data.wave == wave]
    reverse = event[["iid", "pid", "gender", "dec"]].rename(
        columns={"iid": "pid", "pid": "iid", "gender": "partner_gender", "dec": "reverse_dec"})
    pairs = event[event.gender == 1].merge(reverse, on=["iid", "pid"], validate="one_to_one")
    pairs = pairs[pairs.partner_gender == 0].copy()
    if pairs.empty:
        raise ValueError(f"Wave {wave:g} has no eligible reciprocal bipartite encounters")
    for column in ("dec", "reverse_dec", "match"):
        if not pairs[column].isin([0, 1]).all():
            raise ValueError(f"Invalid binary labels in {column}")
    if not (pairs.match == pairs.dec * pairs.reverse_dec).all():
        raise ValueError("Mutual-interest labels disagree with paired directional decisions")
    left, right = sorted(pairs.iid.unique()), sorted(pairs.pid.unique())
    left_pos = {node: (0, y) for node, y in zip(left, np.linspace(0, 1, len(left)))}
    right_pos = {node: (1, y) for node, y in zip(right, np.linspace(0, 1, len(right)))}
    height = max(5, 0.22 * max(len(left), len(right)))
    fig, axes = plt.subplots(1, 2, figsize=(11, height), layout="constrained")
    for ax, mutual_only in zip(axes, (False, True)):
        selected = pairs[pairs.match == 1] if mutual_only else pairs
        segments = [[left_pos[row.iid], right_pos[row.pid]] for row in selected.itertuples()]
        ax.add_collection(LineCollection(segments, colors="#238b45" if mutual_only else "0.6",
                                         linewidths=1.3 if mutual_only else 0.5,
                                         alpha=0.65 if mutual_only else 0.3))
        for positions, color, offset, alignment in (
            (left_pos, "#2166ac", -0.04, "right"),
            (right_pos, "#b35806", 0.04, "left"),
        ):
            points = np.array(list(positions.values()))
            ax.scatter(points[:, 0], points[:, 1], color=color, s=28, zorder=3)
            for node, (x, y) in positions.items():
                ax.text(x + offset, y, f"{node:g}", ha=alignment, va="center", fontsize=7)
        ax.set(xlim=(-0.24, 1.24), ylim=(-0.07, 1.12),
               title=f"{'Observed mutual interest' if mutual_only else 'Recorded encounters'} ({len(selected)} edges)")
        ax.text(0, 1.05, "Group A (gender=1)", ha="center", fontsize=9)
        ax.text(1, 1.05, "Group B (gender=0)", ha="center", fontsize=9)
        ax.axis("off")
    fig.suptitle(f"Observed bipartite network — wave {wave:g}\nLabels are participant IDs; all eligible nodes retained")
    save_figure(fig, directory, "network_structure")
    pairs[["wave", "iid", "pid", "dec", "reverse_dec", "match"]].to_csv(
        directory / "network_edges.csv", index=False)
    directional_interest_figure(pairs, wave, left_pos, right_pos, height, directory)


def directional_interest_figure(pairs, wave, left_pos, right_pos, height, directory):
    """Plot observed positive decisions separately for each direction."""
    fig, axes = plt.subplots(1, 2, figsize=(12, height), layout="constrained")
    edge_tables = []
    for ax, column, title, color in (
        (axes[0], "dec", "Male → female interest", "#2166ac"),
        (axes[1], "reverse_dec", "Female → male interest", "#b35806"),
    ):
        selected = pairs[pairs[column] == 1]
        for row in selected.itertuples():
            start, end = left_pos[row.iid], right_pos[row.pid]
            source, target = row.iid, row.pid
            if column == "reverse_dec":
                start, end = end, start
                source, target = target, source
            ax.annotate("", xy=end, xytext=start,
                        arrowprops={"arrowstyle": "-|>", "color": color,
                                    "alpha": 0.45, "lw": 0.8,
                                    "shrinkA": 5, "shrinkB": 5,
                                    "mutation_scale": 9}, zorder=1)
            edge_tables.append({"wave": wave, "source_iid": source,
                                "target_iid": target, "direction": title})
        for positions, node_color, offset, alignment in (
            (left_pos, "#2166ac", -0.04, "right"),
            (right_pos, "#b35806", 0.04, "left"),
        ):
            points = np.array(list(positions.values()))
            ax.scatter(points[:, 0], points[:, 1], color=node_color, s=32, zorder=3)
            for node, (x, y) in positions.items():
                ax.text(x + offset, y, f"{node:g}", ha=alignment, va="center", fontsize=7)
        ax.set(xlim=(-0.24, 1.24), ylim=(-0.07, 1.12),
               title=f"{title}\n{len(selected)} positive decisions / {len(pairs)} encounters")
        ax.text(0, 1.05, "Male participants (gender=1)", ha="center", fontsize=8)
        ax.text(1, 1.05, "Female participants (gender=0)", ha="center", fontsize=8)
        ax.axis("off")
    fig.suptitle(f"Observed directional interest — wave {wave:g}\nArrows represent recorded yes decisions; all eligible nodes retained")
    save_figure(fig, directory, "directional_interest")
    pd.DataFrame(edge_tables, columns=["wave", "source_iid", "target_iid", "direction"]).to_csv(
        directory / "directional_interest_edges.csv", index=False)
