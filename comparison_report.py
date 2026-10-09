"""
HbS Solubility Comparison Report
================================

Reference: Henry et al. (2020), PNAS, Figure 3.

IMPORTANT:
The reference values are approximate readings from the published graph,
not the original experimental measurements.

The complete solubility solver has not yet produced valid results.
Therefore, this script reports the reference data without inventing
model predictions or claiming scientific validation.
"""

import csv
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent

INPUT_CSV = BASE_DIR / "figure3_approximate_data.csv"
OUTPUT_CSV = BASE_DIR / "solubility_comparison_report.csv"
OUTPUT_GRAPH = BASE_DIR / "solubility_comparison_report.png"
OUTPUT_TEXT = BASE_DIR / "solubility_comparison_report.txt"


def load_reference_data():
    """Load the approximate reference data."""

    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"Reference CSV not found: {INPUT_CSV}"
        )

    saturation = []
    solubility_mg_cc = []

    with INPUT_CSV.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            saturation.append(
                float(row["oxygen_saturation_fraction"])
            )
            solubility_mg_cc.append(
                float(row["approx_solubility_mg_per_cc"])
            )

    return (
        np.asarray(saturation),
        np.asarray(solubility_mg_cc),
    )


def save_comparison_csv(saturation, solubility):
    """Save the reference data and clearly mark predictions unavailable."""

    with OUTPUT_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "oxygen_saturation_fraction",
            "oxygen_saturation_percent",
            "approx_reference_solubility_mg_per_cc",
            "model_prediction_mg_per_cc",
            "comparison_status",
        ])

        for sat, reference in zip(saturation, solubility):
            writer.writerow([
                f"{sat:.4f}",
                f"{sat * 100:.2f}",
                f"{reference:.2f}",
                "NOT_AVAILABLE",
                "Model solver not validated",
            ])


def save_graph(saturation, solubility):
    """Plot the approximate reference data."""

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        saturation * 100,
        solubility,
        "o-",
        label="Approximate Figure 3 readings",
    )

    ax.set_title(
        "HbS Solubility vs Oxygen Saturation\n"
        "Reference data only — model predictions unavailable"
    )

    ax.set_xlabel("Oxygen saturation (%)")
    ax.set_ylabel("Solubility (mg/cc)")
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    try:
        fig.savefig(
            OUTPUT_GRAPH,
            dpi=300,
            format="png",
        )
    finally:
        plt.close(fig)


def save_text_report(saturation, solubility):
    """Write a concise project report."""

    report = f"""
HbS SOLUBILITY COMPARISON REPORT
================================

Scientific reference:
Henry et al. (2020), PNAS.
Allosteric control of hemoglobin S fiber formation by oxygen
and its relation to the pathophysiology of sickle cell disease.

PURPOSE
-------
Organise approximate solubility values read from Figure 3 for
future comparison with computational model predictions.

REFERENCE DATA
--------------
Number of approximate reference points: {len(saturation)}
Lowest plotted solubility: {np.min(solubility):.2f} mg/cc
Highest plotted solubility: {np.max(solubility):.2f} mg/cc

The approximate values show increasing HbS solubility as oxygen
saturation increases, with a steeper rise at high saturation.

IMPORTANT DATA LIMITATION
-------------------------
These points were estimated visually from the published figure.
They are not the original experimental measurements and should
not be treated as exact observations.

MODEL STATUS
------------
The complete solubility solver has not yet generated a valid
curve across the required pressure range.

No model predictions, prediction errors, goodness-of-fit scores,
or validation claims are reported in this document.

NEXT SCIENTIFIC STEPS
---------------------
1. Confirm the mathematical implementation of Equation 1.
2. Verify the reference solubility and experimental conditions.
3. Obtain or digitise the published reference data more accurately.
4. Generate valid model predictions.
5. Compare predictions with reference data using suitable error
   metrics and clearly documented assumptions.

CONCLUSION
----------
The approximate reference dataset has been organised successfully.
The computational solubility model remains unvalidated. Further
mathematical checks and comparison with published data are needed
before drawing scientific conclusions.
"""

    OUTPUT_TEXT.write_text(
        report.strip() + "\n",
        encoding="utf-8",
    )


def main():
    print("HbS Solubility Comparison Report")
    print("================================")
    print()

    saturation, solubility = load_reference_data()

    save_comparison_csv(saturation, solubility)
    save_graph(saturation, solubility)
    save_text_report(saturation, solubility)

    print("Reference points:", len(saturation))
    print("Minimum reference solubility:", f"{np.min(solubility):.2f} mg/cc")
    print("Maximum reference solubility:", f"{np.max(solubility):.2f} mg/cc")
    print()
    print("Created files:")
    print(OUTPUT_CSV)
    print(OUTPUT_GRAPH)
    print(OUTPUT_TEXT)
    print()
    print("Model predictions were not fabricated.")
    print("Scientific validation remains outstanding.")


if __name__ == "__main__":
    main()