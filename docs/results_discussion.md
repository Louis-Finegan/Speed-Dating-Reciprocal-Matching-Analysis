# Discussion of preliminary recommendation results

Source: [recommendation_results.csv](../results/speed_dating/recommendation_results.csv).

The saved results show a trade-off between selecting mutually interested pairs and distributing exposure. These findings describe one offline evaluation run.

## Results

| Method | Observed mutual-interest rate | Recommendations | Mutual-positive pairs selected | Recipient coverage | Exposure Gini ↓ |
|---|---:|---:|---:|---:|---:|
| Random | 15.4% | 279 | 43 | 95.4% | 0.265 |
| Reciprocal ranking | 17.2% | 279 | 48 | 73.6% | 0.571 |
| Capacity constrained | 16.8% | 256 | 43 | 100% | 0.019 |

Mutual-positive pair counts are calculated from the saved rates and recommendation counts. They represent selected encounters with recorded mutual interest, not newly created matches.

## Reciprocal ranking increases yield and concentrates exposure

Reciprocal ranking selects five more mutual-positive encounters than random using the same 279 recommendations. Its observed mutual-interest rate improves by approximately **1.8 percentage points**, or **11.6% relative to random**.

However, recipient coverage falls from 95.4% to 73.6%, and exposure inequality more than doubles by the Gini measure. The model repeatedly favors a smaller set of recipients.

## Recipient caps spread exposure evenly

The capacity-constrained method gives every eligible recipient at least one recommendation. Its exposure Gini is close to zero, indicating a nearly equal distribution of recipient exposure.

Its observed mutual-interest rate is slightly higher than random's, but it makes 23 fewer recommendations. Consequently, both methods select **43 mutual-positive encounters**. This illustrates why total yield should be reported alongside success rate.

The lower recommendation count also exposes a limitation of the current greedy algorithm: processing actors sequentially can leave later actors without available recipients. Event capacities and candidate edges need to be inspected to determine how much of the shortfall was avoidable.

## Limits of the evidence

These results are suggestive, not evidence of a reliable improvement yet. They come from one event split and one random recommendation draw. Five additional mutual-positive encounters could reflect sampling variation. Repeated random baselines and paired event-level uncertainty estimates are needed before claiming that reciprocal ranking outperforms random.

Coverage and Gini describe **recipient exposure among eligible held-out candidates**, not coverage of every participant in the dataset.

These methods are recommendation heuristics. Maximum-weight matching, Gale–Shapley and stability measurements have not been implemented, so this table cannot establish which matching algorithm performs best.

The analysis is an offline replay of recorded encounters. It cannot establish how recommendations would change behavior or outcomes on a dating platform.

## Observed, predicted and simulated quantities

- **Observed outcomes:** the dataset's recorded decisions and mutual-interest labels.
- **Predictions:** estimated directional attraction probabilities and their product, used to rank candidate pairs.
- **Simulated allocation:** the recommendation edges selected by each algorithm from recorded encounters.

The mutual-interest rates in the table use observed labels on selected edges. They are not averages of predicted probabilities or outcomes from a deployed recommender.

## Preliminary conclusion

In this run, reciprocal ranking selected more observed mutual-interest pairs while concentrating exposure. Recipient caps greatly improved exposure equality, with reduced recommendation volume.

The directional and mutual prediction metrics printed in the terminal are not saved in the results CSV. Those metrics are needed for a separate discussion of how well the model predicts attraction.
