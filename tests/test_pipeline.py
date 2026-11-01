"""Network-free regression checks for the reorganized pipeline."""
import io
from unittest.mock import patch
import numpy as np
import pandas as pd
import unittest
import tempfile
from pathlib import Path
from dating_research.dataset import REQUIRED_COLUMNS
from dating_research.source import load_data
from dating_research.statistics import gini
from dating_research.recommendations import make_recommendations
from scripts.download_data import download_data
from scripts.run_analysis import main


def encounters():
    rows = []
    for wave in range(1, 5):
        for a in range(3):
            for b in range(3):
                yes_a, yes_b = int((a + b) % 2 == 0), int(b != 1)
                common = dict(wave=wave, match=yes_a * yes_b, age=22 + a,
                              age_o=23 + b, samerace=(a + b) % 2,
                              int_corr=0.1 * b, goal=1 + a)
                rows.append(dict(common, iid=wave*100+a, pid=wave*100+10+b,
                                 gender=1, dec=yes_a, dec_o=yes_b))
                rows.append(dict(common, iid=wave*100+10+b, pid=wave*100+a,
                                 gender=0, dec=yes_b, dec_o=yes_a))
    return pd.DataFrame(rows)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.tmp_path = Path(directory.name)

    def test_analysis_pipeline(self):
        tmp_path = self.tmp_path
        source = tmp_path / "input.csv"
        encounters().to_csv(source, index=False)
        output = tmp_path / "results"
        main(["--csv", str(source), "--output", str(output), "--k", "2"])
        result = pd.read_csv(output / "recommendation_results.csv")
        assert list(result.method) == ["random", "reciprocal", "capacity_constrained"]
        assert result.reciprocal_hit_rate.between(0, 1).all()
        assert result.target_coverage.between(0, 1).all()
        assert result.exposure_gini.between(0, 1).all()
        assert result.iloc[2].recommendations <= 6


    def test_loader_removes_duplicate_encounters(self):
        tmp_path = self.tmp_path
        source = tmp_path / "input.csv"
        rows = encounters()
        pd.concat([rows, rows.iloc[:1]]).to_csv(source, index=False)
        assert len(load_data(source)) == len(rows)


    def test_capacity_policy_and_gini(self):
        pairs = pd.DataFrame(dict(wave=[1]*4, iid=[1, 1, 2, 2], pid=[3, 4, 3, 4],
                                  score=[0.9, 0.8, 0.7, 0.6], match=[1, 0, 0, 1]))
        result = make_recommendations(pairs, 2, "capacity_constrained", cap=1)
        assert result["recommendations"] == 2
        assert result["target_coverage"] == 1
        assert result["exposure_gini"] == 0
        assert gini([0, 0]) == 0
        assert np.isclose(gini([0, 1]), 0.5)


    def test_download_validation_and_existing_file(self):
        tmp_path = self.tmp_path
        destination = tmp_path / "data.csv"
        payload = encounters().to_csv(index=False).encode()
        with patch("scripts.download_data.urlopen", return_value=io.BytesIO(payload)):
            count, digest = download_data(destination)
        assert count == len(encounters())
        assert len(digest) == 64
        assert destination.read_bytes() == payload
        with self.assertRaises(FileExistsError):
            download_data(destination)


    def test_invalid_download_is_not_saved(self):
        tmp_path = self.tmp_path
        destination = tmp_path / "data.csv"
        with patch("scripts.download_data.urlopen", return_value=io.BytesIO(b"oops\n1\n")):
            with self.assertRaisesRegex(ValueError, "missing columns"):
                download_data(destination)
        assert not destination.exists()
