# Reading the regression figure

The [regression figure](../results/speed_dating/figures/regression.png) combines two different questions: what the fitted model predicts when age changes, and how its predictions compare with held-out decisions. Both panels concern **one person's interest in another person**, not mutual interest.

## Left panel: an adjusted slice through the model

The model predicts the probability that the participant says yes to another date:

$$
\widehat p_{ij}=\widehat P(Y_{ij}=1\mid X_{ij}).
$$

The horizontal axis is the age of the person making that decision. The vertical axis is their predicted probability of saying yes. It is not the probability that someone else likes them.

Each line holds the partner's age fixed: 24, 26 or 28.75. These are the training data's 25th, 50th and 75th percentiles. The remaining inputs are fixed at shared-race indicator 0, interest correlation 0.19 and goal code 1. These reference settings come from training medians or modes. Fractional ages arise from percentile calculation; these are model inputs, not particular identified participants.

For example, to read the orange line at participant age 30, imagine a 30-year-old deciding whether to see a 26-year-old again, with the other inputs fixed as above. The line gives the model's estimated probability of that decision being yes.

The upward slope means the fitted model assigns higher probabilities of saying yes to older decision-makers under those fixed conditions. It does not establish that older people receive more interest, that aging causes greater interest, or that the association applies equally to male and female participants. The baseline pools both directions and does not include gender as a predictor.

The curves look nearly straight because the displayed values occupy the middle of a logistic curve. Logistic regression is linear in log odds; its probability curve need not show the full S shape over the plotted range.

This panel is a conditional model illustration, not observed yes rates by age. It has no confidence bands, and unusual age combinations may be weakly supported by the data. It should not be treated as evidence that the age coefficient is statistically reliable.

## Right panel: calibration on held-out encounters

Held-out predictions are divided into up to eight roughly equal-sized groups ordered by predicted probability. Each point shows:

- Horizontal coordinate: the group's mean predicted probability of saying yes.
- Vertical coordinate: the fraction of decisions in that group that were actually yes.

On the dashed diagonal, predictions and observed frequencies agree. Above it, the model underpredicts interest; below it, the model overpredicts interest. Connecting points helps trace bins; it is not another fitted regression curve.

For example, the rightmost point has mean predicted probability about **50.5%**, but observed interest about **38.2%**. The model overpredicts interest in that bin.

The plotted bin means span only about 36%–51%, indicating limited separation between the average scores of these groups. They do not give the minimum and maximum individual prediction. The observed fractions do not increase consistently with the scores, so this figure does not demonstrate strong ranking performance. Ranking metrics and event-level uncertainty are needed to assess that question.

## Connection to recommendations

The left panel illustrates one directional model prediction. Reciprocal recommendations use two predictions, one for each participant, and multiply them:

$$
\widehat q_{ij}=\widehat p_{ij}\widehat p_{ji}.
$$

Neither panel directly evaluates that mutual-interest score. The right panel evaluates directional calibration only. Both panels use data across multiple waves, whereas the default network figure displays only wave 1.

See [the theoretical setup](theoretical_setup.md) for the probability assumptions and [figure documentation](figures.md) for generation commands.
