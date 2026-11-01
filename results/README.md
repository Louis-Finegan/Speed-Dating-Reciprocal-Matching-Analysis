# Local outputs

`python -m scripts.run_study` writes to `results/speed_dating/` by default:

- `recommendation_results.csv`: selected-edge mutual-interest rate, recommendation
  count, recipient coverage and exposure Gini for all three policies.
- `figures/`: regression, mutual-interest, network and directional-interest PNG/PDF
  figures, plotting CSVs, held-out predictions and figure metadata.

Directional and mutual model metrics print to the terminal. Reusing an output
directory overwrites generated files. Raw encounter identifiers appear in some
plotting CSVs and network figures; outputs stay local and are ignored by Git.
See [figure documentation](../docs/figures.md) and the
[preliminary results discussion](../docs/results_discussion.md).
