"""Automated tests for the HbS solubility project."""

import csv
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT_DIR = Path(__file__).resolve().parent


def test_required_project_files_exist():
    required_files = [
        "complete_solubility_model.py",
        "README.md",
        "test_solubility_model.py",
    ]
    for filename in required_files:
        assert (PROJECT_DIR / filename).is_file(), (
            f"Missing project file: {filename}"
        )


def test_model_script_compiles():
    script = PROJECT_DIR / "complete_solubility_model.py"
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(script)],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
    )
    assert result.returncode == 0, result.stderr


def test_model_output_has_expected_structure():
    csv_path = PROJECT_DIR / "solubility_model_comparison.csv"
    if not csv_path.exists():
        pytest.skip("Run complete_solubility_model.py first.")

    with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        rows = list(reader)

    assert headers is not None
    assert rows
    assert "model" in headers
    assert "oxygen_pressure_torr" in headers
    assert "calculated_solubility_g_per_ml" in headers


def test_model_output_values_are_finite():
    csv_path = PROJECT_DIR / "solubility_model_comparison.csv"
    if not csv_path.exists():
        pytest.skip("Run complete_solubility_model.py first.")

    with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
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


def test_three_models_are_present():
    csv_path = PROJECT_DIR / "solubility_model_comparison.csv"
    if not csv_path.exists():
        pytest.skip("Run complete_solubility_model.py first.")

    with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    models = {row["model"] for row in rows}
    assert len(models) == 3


def test_comparison_graph_exists_if_generated():
    graph = PROJECT_DIR / "solubility_model_comparison.png"
    csv_path = PROJECT_DIR / "solubility_model_comparison.csv"

    if not csv_path.exists():
        pytest.skip("Run complete_solubility_model.py first.")

    assert graph.is_file()
    assert graph.stat().st_size > 0


def test_reference_solubility_is_marked_provisional():
    script = PROJECT_DIR / "complete_solubility_model.py"
    source = script.read_text(encoding="utf-8")

    assert "REFERENCE_SOLUBILITY" in source
    assert "PROVISIONAL" in source