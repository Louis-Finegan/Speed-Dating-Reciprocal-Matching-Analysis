# Local data

Run `python -m scripts.download_data` from the repository root to download the
original Columbia CSV to `data/speed_dating_data.csv`. Existing files are never
overwritten. A successful download prints its row count and SHA-256 checksum.
A manual original CSV can be placed at that path instead.

Source data remain local and are ignored by Git. See
[provenance](../docs/DATA_PROVENANCE.md) and the [dictionary](../docs/DATA_DICTIONARY.md).
