"""Download the Columbia Speed Dating CSV without additional dependencies.

Usage:
    python -m scripts.download_data
    python -m scripts.download_data --output data/speed_dating.csv

The default source is Columbia's public dataset archive. Use --url to specify
an alternative CSV source explicitly if that archive is unavailable.
"""

import argparse
import csv
import hashlib
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


from dating_research.dataset import DEFAULT_URL, DEFAULT_INPUT, REQUIRED_COLUMNS


def download_data(output, url=DEFAULT_URL, timeout=60):
    """Validate a temporary download, then save it without overwriting files.

    Validation checks CSV structure and the columns required by the analysis;
    it does not establish dataset authenticity or validate encounter outcomes.
    Original downloaded bytes are preserved, including their encoding.
    """
    output = Path(output)
    if output.exists():
        raise FileExistsError(f"Output already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": "speed-dating-research/1.0"})
    with tempfile.TemporaryDirectory(dir=output.parent) as directory:
        temporary = Path(directory) / "download.csv"
        with urlopen(request, timeout=timeout) as response:
            with temporary.open("wb") as destination:
                shutil.copyfileobj(response, destination)

        # Latin-1 accepts the legacy text encoding without changing the file.
        with temporary.open(encoding="latin-1", newline="") as source:
            reader = csv.reader(source)
            header = next(reader, [])
            if header:
                header[0] = header[0].removeprefix("ï»¿")
            missing = REQUIRED_COLUMNS - set(header)
            if missing:
                raise ValueError(
                    "Download is not the expected CSV; missing columns: "
                    + ", ".join(sorted(missing))
                )
            rows = 0
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue
                if len(row) != len(header):
                    raise ValueError(f"Inconsistent CSV field count at line {line_number}")
                rows += 1
            if not rows:
                raise ValueError("Downloaded CSV has no data rows")

        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
        # Linking a completed file is atomic and fails if output already exists.
        output.hardlink_to(temporary)
    return rows, digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--url", default=DEFAULT_URL, help="Direct CSV download URL")
    parser.add_argument("--timeout", type=float, default=60, help="Network timeout in seconds")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    try:
        rows, digest = download_data(args.output, args.url, args.timeout)
    except (OSError, URLError, ValueError, csv.Error) as error:
        print(f"Download failed: {error}", file=sys.stderr)
        return 1
    print(f"Source: {args.url}")
    print(f"Saved {rows} rows to {args.output}")
    print(f"SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
