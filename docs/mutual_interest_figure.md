# Mutual-interest regression figure

Generate the [figure](../results/speed_dating/figures/mutual_interest_regression.png) with:

```bash
python -m scripts.plot_figures
```

PNG and PDF versions are saved in `results/speed_dating/figures/` as `mutual_interest_regression`.

## What is modeled?

The figure uses the same reciprocal score as the recommendation algorithm:

$$
\widehat q_{ij}=\widehat p_{ij}\widehat p_{ji}.
$$

Each directional probability comes from the existing logistic regression. This is **not a separately fitted logistic regression with mutual interest as its target**. Interpreting the product as a joint probability requires the conditional-independence approximation explained in [the theoretical setup](theoretical_setup.md).

## Left: adjusted mutual-interest curves

The horizontal axis varies one participant's age. Each line fixes their partner's age at a training-data percentile. The vertical axis estimates the probability that **both say yes**.

For the reverse prediction, the two ages are exchanged. Both participants are assigned the training modal goal (code 1). Shared-race status is fixed at 0 and interest correlation at 0.19 for the current dataset and split. These are hypothetical reference encounters, not individual observed pairs. Exact reference settings are saved in `figure_metadata.json`.

The curves illustrate the fitted model under fixed inputs. They do not show causal age effects, observed age-specific match rates, or confidence intervals. Sparse or unusual combinations of ages may have weak empirical support. The model pools male and female decisions without a gender predictor, so these curves are not sex-specific estimates.

## Right: held-out mutual calibration

Each held-out encounter is counted once, with its two actual directional feature records used for prediction. Predicted mutual probabilities are grouped into up to eight quantile bins.

- Horizontal coordinate: average predicted mutual probability in a bin.
- Vertical coordinate: fraction of encounters in that bin with recorded mutual interest.

The diagonal represents agreement. Points above it indicate underprediction; points below it indicate overprediction. This assesses the product score directly, unlike the earlier directional calibration plot. No uncertainty intervals are shown.

Mutual labels are checked against the paired directional decisions before plotting. The split and model match the existing directional figure. Calibration uses multiple held-out waves, not only the event displayed in the network diagrams.

## Saved numerical data

- `mutual_interest_curves.csv`: adjusted probability curves.
- `mutual_calibration_bins.csv`: plotted calibration values.
- `held_out_mutual_predictions.csv`: recorded mutual outcomes, both directional predictions and their product.

These are model predictions evaluated against recorded encounters, not evidence that recommendations cause new mutual matches.
