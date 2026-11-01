# Network structure

We work with a **bipartite network of recorded speed-dating encounters**, with directional attraction information attached to each encounter.

## Participants and encounters

For event (wave) $w$, let $A_w$ and $B_w$ be its two participant groups. These reflect the dataset's binary event format. In the current code, recommendations originate from participants coded `gender=1` toward the opposite group.

The event network is

$$
G_w=(A_w\cup B_w,E_w),
\qquad E_w\subseteq A_w\times B_w.
$$

Each node represents a participant. An edge $(i,j)\in E_w$ represents an eligible recorded encounter. The current reciprocal evaluation retains encounters with records in both directions after filtering. There are no within-group edges in this model.

An absent edge means there is no eligible recorded encounter. It does **not** mean the participants rejected one another. Completeness and consistency of the bipartite structure still require a dataset audit.

## Directional attraction

An encounter contains two directional decisions:

$$
i\xrightarrow{Y_{ij}}j,
\qquad j\xrightarrow{Y_{ji}}i.
$$

Here $Y_{ij}=1$ means that $i$ wanted to see $j$ again. Attraction can be asymmetric. The intended observed mutual-interest outcome is

$$
M_{ij}=Y_{ij}Y_{ji}.
$$

The model estimates directional probabilities $\widehat p_{ij}$ and $\widehat p_{ji}$ and combines them into a symmetric reciprocal score:

$$
\widehat q_{ij}=\widehat p_{ij}\widehat p_{ji}.
$$

Interpreting this product as a probability requires the assumptions described in [the theoretical setup](theoretical_setup.md).

| Network view | Edge meaning |
|---|---|
| Encounter network | An eligible recorded meeting |
| Observed attraction network | A directed positive decision on an encountered pair |
| Predicted attraction network | A directed probability estimate on an encountered pair |

## Recommendation subnetwork

Each algorithm selects a subset of encounter edges:

$$
R_w\subseteq E_w.
$$

Selected edges are oriented from group A to group B. An initiator's **out-degree** counts the candidates recommended to them. A recipient's **in-degree** counts how many initiators are recommended that recipient; this is the exposure used in the results.

Reciprocal ranking can concentrate edges on a small number of recipients. Recipient capacity constraints limit that concentration.

The current recommendation network is many-to-many: an initiator can select up to $k$ candidates, and the constrained method also caps recipient exposure at $k$. A one-to-one matching would restrict every node to at most one selected edge.

## Events and interpretation

Recommendations never cross event boundaries. We therefore analyze separate event networks. Participant recurrence across waves must still be checked before describing those events as participant-disjoint.

This is a network of encounters and expressed interest. Selected edges do not establish friendships, exclusive couples or long-term relationships.

See [the results discussion](results_discussion.md) for how exposure and mutual-interest outcomes differ across the current algorithms.
