"""
Automated tests for the HbS solubility project.

Run with:
    python -m pytest -v
"""

import csv
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest


PROJECT_DIR = Path(__file__).resolve().parent


def test_required_project_files_exist():
    """Check that the main project files exist."""

    required_files = [
        "complete_solubility_model.py",
        "experimental_comparison.py",
        "figure3_approximate_data.csv",
        "README.md",
    ]

    for filename in required_files:
        assert (PROJECT_DIR / filename).is_file(), (
            f"Missing project file: {filename}"
        )


def test_experimental_csv_has_expected_columns():
    """Check the structure of the approximate experimental dataset."""

    csv_path = PROJECT_DIR / "figure3_approximate_data.csv"

    with csv_path.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        assert reader.fieldnames is not None
        assert "oxygen_saturation_fraction" in reader.fieldnames
        assert "approx_solubility_mg_per_cc" in reader.fieldnames

        rows = list(reader)

    assert len(rows) > 0


def test_experimental_data_values_are_valid():
    """Check that the experimental data contain plausible numeric values."""

    csv_path = PROJECT_DIR / "figure3_approximate_data.csv"

    with csv_path.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        rows = list(csv.DictReader(file))

    saturation = np.array(
        [float(row["oxygen_saturation_fraction"]) for row in rows]
    )

    solubility = np.array(
        [float(row["approx_solubility_mg_per_cc"]) for row in rows]
    )

    assert np.all(np.isfinite(saturation))
    assert np.all(np.isfinite(solubility))
    assert np.all((saturation >= 0) & (saturation <= 1))
    assert np.all(solubility > 0)


def test_model_output_has_expected_structure():
    """Check calculated results if the output CSV already exists."""

    csv_path = PROJECT_DIR / "complete_solubility_results.csv"

    if not csv_path.exists():
        pytest.skip(
            "Run complete_solubility_model.py first to generate model results."
        )

    with csv_path.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        rows = list(reader)

    assert headers is not None
    assert len(rows) > 0

    assert "oxygen_pressure_torr" in headers
    assert "calculated_solubility_g_per_ml" in headers


def test_model_output_values_are_finite():
    """Check that generated solubility results contain valid numbers."""

    csv_path = PROJECT_DIR / "complete_solubility_results.csv"

    if not csv_path.exists():
        pytest.skip(
            "Run complete_solubility_model.py first to generate model results."
        )

    with csv_path.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        rows = list(csv.DictReader(file))

    pressure = np.array(
        [float(row["oxygen_pressure_torr"]) for row in rows]
    )

    solubility = np.array(
        [float(row["calculated_solubility_g_per_ml"]) for row in rows]
    )

    assert np.all(np.isfinite(pressure))
    assert np.all(np.isfinite(solubility))
    assert np.all(pressure >= 0)
    assert np.all(solubility > 0)


def test_comparison_script_compiles():
    """Check the comparison script for Python syntax errors."""

    script_path = PROJECT_DIR / "experimental_comparison.py"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "py_compile",
            str(script_path),
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
    )

    assert result.returncode == 0, result.stderr


def test_comparison_outputs_exist_if_generated():
    """Check comparison outputs when the comparison has been run."""

    graph = PROJECT_DIR / "figure3_experimental_comparison.png"
    csv_path = PROJECT_DIR / "experimental_comparison_results.csv"
    report = PROJECT_DIR / "experimental_comparison_report.txt"

    if not csv_path.exists():
        pytest.skip(
            "Run experimental_comparison.py first to generate comparison outputs."
        )

    assert csv_path.is_file()
    assert graph.is_file()
    assert report.is_file()

    assert csv_path.stat().st_size > 0
    assert graph.stat().st_size > 0
    assert report.stat().st_size > 0