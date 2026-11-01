# Participant counts: one event versus the full dataset

The network figure defaults to **wave 1**, which contains **20 participants**: 10 coded `gender=1` and 10 coded `gender=0`.

These two groups yield $10\times10=100$ possible cross-group encounters. The plotting input checks confirm 100 eligible reciprocal encounters in this wave. Each encounter can appear as two directional rows, one per participant, so row counts should not be interpreted as participant counts.

The full dataset returned by the current `load_data` function contains **551 distinct participant IDs across 21 waves**. No participant ID in this loaded data appears in more than one wave.

Thus, 20 is the participant count for the displayed event, not the full study. The regression script uses training waves from across the dataset and evaluates predictions on held-out waves; it is not fitted only to the 20 people displayed in the default network figure.

These counts were checked against the local `data/speed_dating_data.csv` using the current loader. They describe the data retained by that loader, whose exclusions still require a full audit.
