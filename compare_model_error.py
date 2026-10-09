"""
Exploratory HbS solubility model comparison.

Reference: Henry et al. (2020), PNAS.

IMPORTANT:
figure3_approximate_data.csv contains approximate values,
not verified raw experimental measurements.

The resulting MAE and RMSE are exploratory only.
They must not be reported as validated experimental errors.
"""

import csv
from pathlib import Path

import numpy as np

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "figure3_approximate_data.csv"
MODEL_FILE = BASE_DIR / "solubility_model_comparison.csv"
OUTPUT_FILE = BASE_DIR / "exploratory_model_errors.csv"


def load_csv(path):
    with path.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        return list(csv.DictReader(file))


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(DATA_FILE)

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"{MODEL_FILE} not found. "
            "Run complete_solubility_model.py first."
        )

    measurements = load_csv(DATA_FILE)
    predictions = load_csv(MODEL_FILE)

    if not measurements or not predictions:
        raise ValueError("An input CSV is empty.")

    # These are approximate points, not verified measurements.
    x_data = np.array([
        float(row["oxygen_saturation_fraction"])
        for row in measurements
    ])

    y_data = np.array([
        float(row["approx_solubility_mg_per_cc"])
        for row in measurements
    ])

    if (
        not np.all(np.isfinite(x_data))
        or not np.all(np.isfinite(y_data))
    ):
        raise ValueError("Input data contain invalid values.")

    results = []

    model_names = sorted({
        row["model"] for row in predictions
    })

    for model_name in model_names:
        model_rows = [
            row for row in predictions
            if row["model"] == model_name
        ]

        x_model = np.array([
            float(row["free_hbs_saturation_fraction"])
            for row in model_rows
        ])

        y_model = np.array([
            float(row["calculated_solubility_mg_per_ml"])
            for row in model_rows
        ])

        # Sort by saturation before interpolation.
        order = np.argsort(x_model)
        x_model = x_model[order]
        y_model = y_model[order]

        # Compare only within the model's available range.
        valid = (
            (x_data >= x_model.min())
            & (x_data <= x_model.max())
        )

        if valid.sum() < 2:
            print(
                f"Skipping {model_name}: "
                "not enough overlapping points."
            )
            continue

        observed_approx = y_data[valid]

        predicted = np.interp(
            x_data[valid],
            x_model,
            y_model,
        )

        errors = predicted - observed_approx

        mae = float(np.mean(np.abs(errors)))
        rmse = float(np.sqrt(np.mean(errors**2)))

        results.append({
            "model": model_name,
            "comparison_points": int(valid.sum()),
            "MAE_mg_per_ml": mae,
            "RMSE_mg_per_ml": rmse,
            "data_status": "APPROXIMATE_DIGITISATION_UNVERIFIED",
            "interpretation": "EXPLORATORY_ONLY_NOT_VALIDATION",
        })

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "model",
                "comparison_points",
                "MAE_mg_per_ml",
                "RMSE_mg_per_ml",
                "data_status",
                "interpretation",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    print("\nEXPLORATORY MODEL COMPARISON")
    print("=" * 65)
    print("Reference: Henry et al. (2020), PNAS")
    print("Input points: approximate, not verified measurements")
    print("These metrics do NOT establish scientific validity.\n")

    for result in results:
        print(result["model"])
        print(
            f"  Comparison points: "
            f"{result['comparison_points']}"
        )
        print(
            f"  MAE:  "
            f"{result['MAE_mg_per_ml']:.3f} mg/mL"
        )
        print(
            f"  RMSE: "
            f"{result['RMSE_mg_per_ml']:.3f} mg/mL"
        )
        print()

    print("Results saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()