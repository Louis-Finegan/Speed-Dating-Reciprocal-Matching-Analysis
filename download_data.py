"""Compatibility entry point; prefer python -m scripts.download_data."""
from scripts.download_data import download_data
from scripts.download_data import main

if __name__ == "__main__":
    raise SystemExit(main())
