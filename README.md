# Mathematics of Online Dating

A reproducible pilot study of directional attraction, reciprocal recommendation and exposure fairness.

See [project explanations](docs/README.md) for the network description, theoretical definitions and results discussion.

## Research question
Can reciprocal recommendations increase observed mutual-interest rates without concentrating exposure on a few participants?

## Data
The downloader uses Columbia’s public archive of the **original** Speed Dating Experiment CSV (`Speed Dating Data.csv`). A manual copy is also available from https://www.kaggle.com/datasets/annavictoria/speed-dating-experiment . Place it at `data/speed_dating_data.csv`. The data are not redistributed here.

## Setup

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m scripts.run_study
```

Results print to the terminal and `results/speed_dating/recommendation_results.csv`.

Generate regression and network figures with `python -m scripts.plot_figures`. PNG/PDF files and numerical plot data are saved in `results/speed_dating/figures/`. See [figure explanations](docs/figures.md) for interpretation and options.

## Repository structure

```text
dating_research/          # Reusable loading, model, metrics, policies and figures
scripts/                 # Download, analysis, figures and combined entry points
tests/                   # Network-free software checks
docs/                    # Theory, provenance, dictionary and interpretation
data/                    # Local source CSV; README tracked
results/                 # Local generated outputs; README tracked
requirements.txt         # Analysis dependencies
requirements-dev.txt     # Analysis dependencies plus pytest
```

Use Python 3.10 or newer and run commands from the repository root. The combined
command reuses existing input and downloads it only when missing. Separate steps:

```bash
python -m scripts.download_data
python -m scripts.run_analysis --k 3
python -m scripts.plot_figures
```

For another local copy or output directory:

```bash
python -m scripts.run_study --input data/speed_dating_data.csv --output results/local_study --k 3
```

Raw data, generated outputs and virtual environments are excluded from Git. The original root scripts remain compatibility entry points.
See [data provenance](docs/DATA_PROVENANCE.md), the
[data dictionary](docs/DATA_DICTIONARY.md) and [output guide](results/README.md).

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The checks can also run without pytest: `python -m unittest discover -s tests -v`.

Tests verify software behavior using synthetic inputs; they are not study findings.

## Methodology
- Train logistic regression to estimate each person's yes/no decision using *pre-date* features: subject age, partner age, same-race indicator, interest correlation, and relationship goal. Entire events are assigned to train or test; participant disjointness across events still requires validation.
- Produce reciprocal probabilities by multiplying estimated directional probabilities (a simplifying conditional-independence approximation).
- For held-out encounters, compare random recommendations, highest reciprocal-probability recommendations, and a capacity-constrained reciprocal ranking. Every initiator has budget `k`, and the constrained procedure caps each recipient at `k` exposures.
- Report observed mutual-interest rate among selected edges, recipient coverage, and Gini inequality of recipient exposure counts.

## Important limitations
This is an **offline replay** of observed speed-date encounters, not an experiment with dating-app users. Participants met their date before making decisions; recommender visibility and exposure would change behavior on a real platform. We can evaluate only encountered pairs, not arbitrary new pairs or counterfactual responses. The algorithms are **sequential heuristics**, not globally optimal matchings. Results are sensitive to event structure, missing data, candidate availability and decision-time. The original dataset is from 2002–2004, is not representative of all daters, and contains a binary male/female event format; this does not cover all genders, sexual orientations or relationship structures. The target measures interest in a second date, not sustained compatibility or relationship quality. Racial variables are used here solely as a dataset demonstrator and should be considered carefully; a full study should test models with and without sensitive attributes and examine disparate impact.

## Next research steps
1. Bootstrap uncertainty by event, not interaction row.
2. Add calibration plots and compare models without sensitive attributes.
3. Implement maximum-weight bipartite matching and deferred acceptance, clearly distinguishing stable preferences from estimated match probabilities.
4. Model exposure and congestion as a dynamic, two-sided market.
5. Seek real dating-platform exposure and communication outcomes for external validation.
