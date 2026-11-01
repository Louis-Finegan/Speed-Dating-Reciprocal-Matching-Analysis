"""Compatibility entry point; prefer python -m scripts.plot_figures."""
from scripts.plot_figures import main

if __name__ == "__main__":
    raise SystemExit(main())
