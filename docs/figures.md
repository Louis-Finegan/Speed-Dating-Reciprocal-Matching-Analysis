# Regression and network figures

Run from the project directory:

```bash
pip install -r requirements.txt
python -m scripts.plot_figures
```

The default input is `data/speed_dating_data.csv`; outputs go into `results/speed_dating/figures/`. To choose an event:

```bash
python -m scripts.plot_figures --csv data/speed_dating_data.csv --wave 1
```

## Regression figure

`regression.png` and `regression.pdf` contain two panels:

- Adjusted logistic regression curves show predicted directional interest against participant age at the training set's 25th, 50th and 75th percentile partner ages. Other variables are held fixed: interest correlation at its training median, and shared-race status and goal at their training modes. Missingness indicators correspond to observed reference values. These curves describe the fitted multivariable model; they are not causal effects or an unadjusted regression of decisions on age. No confidence bands are estimated.
- Calibration compares predicted probabilities with observed decision frequencies in up to eight quantile bins of held-out encounters. The diagonal represents perfect calibration. Bin values are descriptive and have no uncertainty intervals.

The script reproduces the baseline event split and modeling pipeline from `analysis.py`, using seed 42 by default. Participant-disjointness still requires validation. The model retains the baseline's numeric treatment of goal.

## Network figure

`network_structure.png` and `network_structure.pdf` show the earliest wave by default. Two panels share the same node positions:

- All eligible recorded encounters with reverse records and opposite-group endpoints.
- The subset with observed mutual interest, retaining all eligible nodes so isolated participants remain visible.

Edges are undirected encounter or mutual-interest edges, not directed recommendations. Node labels are dataset participant IDs. The layout is schematic: distance does not encode similarity, attraction or demographics. An absent encounter edge does not establish rejection. A single event is used for legibility; it is not claimed to be representative of all events.

The script checks mutual labels against the two paired directional decisions for the displayed event and raises an error if they disagree.

## Directional interest figure

`directional_interest.png` and `directional_interest.pdf` contain two bipartite graphs of the same event: male-to-female interest and female-to-male interest. Male participants stay on the left and female participants on the right in both panels. Arrows point from the person expressing interest to the person they selected.

Each arrow is an observed positive directional decision, not a prediction or an algorithmic recommendation. All eligible participants remain visible, including those with no positive decisions. Counts use the same reciprocally recorded encounter set as the network figure. An arrow in one panel need not have a corresponding reverse arrow in the other; mutual interest is the intersection of the two positive-decision edge sets after reversing orientation.

The positive directed edges are saved in `directional_interest_edges.csv`.

## Reproducibility files

The output directory also contains:

- `regression_curves.csv`: numerical values of the adjusted curves.
- `calibration_bins.csv`: plotted calibration values.
- `held_out_predictions.csv`: held-out predictions and recorded directional decisions.
- `network_edges.csv`: displayed encounter edges and recorded decisions.
- `figure_metadata.json`: seed, source path, train/test waves, network wave and reference feature values.

Rerunning the script replaces outputs with the same filenames.
