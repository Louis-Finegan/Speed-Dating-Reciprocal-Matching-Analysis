# Data provenance

The study uses the original Columbia Speed Dating Experiment CSV from the
2002–2004 study. The downloader's source is:

https://www.stat.columbia.edu/~gelman/arm/examples/speed.dating/Speed%20Dating%20Data.csv

The README also points to the Kaggle mirror:
https://www.kaggle.com/datasets/annavictoria/speed-dating-experiment .

The downloader validates required columns, consistent field counts and nonempty
input before atomically saving the original bytes. It prints a SHA-256 checksum;
it does not persist a download manifest or establish authenticity from schema alone.
Legacy text is read using Latin-1 when UTF-8 decoding fails. Data are not
redistributed by this repository; review the source's use conditions separately.

These are recorded speed-date decisions, not Tinder activity or deployed
recommendation outcomes. See [research design](theoretical_setup.md) and the
[loader](../dating_research/source.py) for exclusions and assumptions.
