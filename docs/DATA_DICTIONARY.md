# Analysis data dictionary

| Column | Role |
|---|---|
| `iid`, `pid` | Participant and encountered partner identifiers |
| `wave` | Speed-dating event used for train/test grouping |
| `gender` | Original binary event-side code; 1 is the recommendation initiator |
| `dec`, `dec_o` | Recorded directional yes/no decisions |
| `match` | Recorded mutual-interest label |
| `age`, `age_o` | Participant and partner ages; predictors |
| `samerace` | Original shared-race indicator; predictor |
| `int_corr` | Original interest-correlation score; predictor |
| `goal` | Original relationship-goal code, treated numerically by the baseline |

Required columns are coerced to numeric. Rows missing event, identifiers, gender
or decision labels are dropped; gender and `dec` must be 0 or 1. Duplicate
`(wave, iid, pid)` rows are removed. Predictor missingness is median-imputed
using training data, with missingness indicators. `lo` and `hi` are derived
unordered participant identifiers. See the source questionnaire for category
meanings and [limitations](../README.md#important-limitations) before interpretation.
