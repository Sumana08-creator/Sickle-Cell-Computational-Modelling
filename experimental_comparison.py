"""
HbS Experimental Comparison
Reference: Henry et al. (2020), PNAS.

Compares approximate experimental data with calculated model results.
Generates a comparison graph, CSV file, and text report.

Important:
Experimental values are approximate digitised estimates.
The comparison does not independently validate the scientific model.
"""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


# =========================================================
# 1. FILE PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

EXPERIMENTAL_FILE = BASE_DIR / "figure3_approximate_data.csv"
MODEL_FILE = BASE_DIR / "complete_solubility_results.csv"

GRAPH_FILE = BASE_DIR / "figure3_experimental_comparison.png"
CSV_FILE = BASE_DIR / "experimental_comparison_results.csv"
REPORT_FILE = BASE_DIR / "experimental_comparison_report.txt"


# =========================================================
# 2. CSV READER
# =========================================================

def read_csv_file(file_path):
    """Read a CSV file and return its column names and rows."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file does not exist: {file_path.name}"
        )

    with file_path.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)
        headers = reader.fieldnames
        rows = list(reader)

    if not headers or not rows:
        raise ValueError(
            f"{file_path.name} contains no usable data."
        )

    return headers, rows


def find_column(headers, possible_names, filename):
    """Find a column without depending on capitalisation."""

    columns = {
        name.strip().lower(): name
        for name in headers
    }

    for candidate in possible_names:
        if candidate.lower() in columns:
            return columns[candidate.lower()]

    raise ValueError(
        f"Required column not found in {filename}.\n"
        f"Available columns: {headers}\n"
        f"Expected one of: {possible_names}"
    )


def read_numeric_column(rows, column, filename):
    """Convert a CSV column to numerical values."""

    values = []

    for row_number, row in enumerate(rows, start=2):
        try:
            value = float(row[column])
        except (ValueError, TypeError, KeyError):
            raise ValueError(
                f"Invalid number in {filename}, "
                f"column {column}, row {row_number}."
            )

        if not np.isfinite(value):
            raise ValueError(
                f"Non-finite value in {filename}, "
                f"column {column}, row {row_number}."
            )

        values.append(value)

    return np.asarray(values, dtype=float)


# =========================================================
# 3. LOAD APPROXIMATE EXPERIMENTAL DATA
# =========================================================

def load_experimental_data():
    """Read the approximate Figure 3 data."""

    headers, rows = read_csv_file(EXPERIMENTAL_FILE)

    saturation_column = find_column(
        headers,
        [
            "oxygen_saturation_fraction",
            "oxygen_saturation_percent",
        ],
        EXPERIMENTAL_FILE.name,
    )

    solubility_column = find_column(
        headers,
        [
            "approx_solubility_mg_per_cc",
            "approx_solubility_mg_per_ml",
            "approx_solubility_g_per_ml",
        ],
        EXPERIMENTAL_FILE.name,
    )

    saturation = read_numeric_column(
        rows,
        saturation_column,
        EXPERIMENTAL_FILE.name,
    )

    solubility = read_numeric_column(
        rows,
        solubility_column,
        EXPERIMENTAL_FILE.name,
    )

    # Convert percentages to fractions when necessary.
    if np.max(saturation) > 1.0:
        saturation = saturation / 100.0

    # Convert g/mL to mg/mL when that is the selected column.
    if "g_per_ml" in solubility_column.lower():
        solubility = solubility * 1000.0

    if np.any((saturation < 0) | (saturation > 1)):
        raise ValueError(
            "Oxygen saturation must be between 0 and 1."
        )

    if np.any(solubility <= 0):
        raise ValueError(
            "Experimental solubility must be positive."
        )

    order = np.argsort(saturation)

    return saturation[order], solubility[order]


# =========================================================
# 4. LOAD CALCULATED MODEL RESULTS
# =========================================================

def load_model_data():
    """Read the calculated solubility results."""

    headers, rows = read_csv_file(MODEL_FILE)

    saturation_column = find_column(
        headers,
        [
            "free_hbs_saturation_fraction",
            "free_hbs_saturation",
        ],
        MODEL_FILE.name,
    )

    solubility_column = find_column(
        headers,
        [
            "calculated_solubility_g_per_ml",
        ],
        MODEL_FILE.name,
    )

    saturation = read_numeric_column(
        rows,
        saturation_column,
        MODEL_FILE.name,
    )

    solubility_g_ml = read_numeric_column(
        rows,
        solubility_column,
        MODEL_FILE.name,
    )

    # Convert g/mL to mg/mL.
    solubility_mg_ml = solubility_g_ml * 1000.0

    if np.any((saturation < 0) | (saturation > 1)):
        raise ValueError(
            "Model saturation values must be between 0 and 1."
        )

    if np.any(solubility_mg_ml <= 0):
        raise ValueError(
            "Model solubility values must be positive."
        )

    order = np.argsort(saturation)

    return saturation[order], solubility_mg_ml[order]


# =========================================================
# 5. COMPARE THE TWO DATASETS
# =========================================================

def compare_datasets(
    experimental_saturation,
    experimental_solubility,
    model_saturation,
    model_solubility,
):
    """Compare at matching oxygen saturation values."""

    # Only compare experimental points inside the model's range.
    valid = (
        (experimental_saturation >= np.min(model_saturation))
        & (experimental_saturation <= np.max(model_saturation))
    )

    saturation = experimental_saturation[valid]
    experimental = experimental_solubility[valid]

    if len(saturation) == 0:
        raise ValueError(
            "The experimental and model saturation ranges do not overlap."
        )

    # Interpolate model predictions at experimental saturation values.
    predicted = np.interp(
        saturation,
        model_saturation,
        model_solubility,
    )

    difference = predicted - experimental
    absolute_error = np.abs(difference)

    percentage_error = (
        absolute_error / np.abs(experimental)
    ) * 100.0

    mae = float(np.mean(absolute_error))
    rmse = float(np.sqrt(np.mean(difference**2)))
    mean_percentage_error = float(np.mean(percentage_error))

    return {
        "saturation": saturation,
        "experimental": experimental,
        "predicted": predicted,
        "difference": difference,
        "absolute_error": absolute_error,
        "percentage_error": percentage_error,
        "mae": mae,
        "rmse": rmse,
        "mean_percentage_error": mean_percentage_error,
    }


# =========================================================
# 6. SAVE COMPARISON CSV
# =========================================================

def save_comparison_csv(results):
    """Save experimental and predicted values."""

    with CSV_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "oxygen_saturation_fraction",
            "approx_experimental_solubility_mg_per_ml",
            "model_prediction_mg_per_ml",
            "model_minus_experiment_mg_per_ml",
            "absolute_error_mg_per_ml",
            "absolute_percentage_error",
        ])

        for index in range(len(results["saturation"])):

            writer.writerow([
                f'{results["saturation"][index]:.6f}',
                f'{results["experimental"][index]:.4f}',
                f'{results["predicted"][index]:.4f}',
                f'{results["difference"][index]:.4f}',
                f'{results["absolute_error"][index]:.4f}',
                f'{results["percentage_error"][index]:.4f}',
            ])


# =========================================================
# 7. GENERATE COMPARISON GRAPH
# =========================================================

def save_comparison_graph(results):
    """Plot approximate experimental data against model predictions."""

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        results["saturation"],
        results["experimental"],
        label="Approximate experimental data",
    )

    ax.plot(
        results["saturation"],
        results["predicted"],
        marker="o",
        label="Model predictions",
    )

    ax.set_xlabel("Oxygen saturation fraction")
    ax.set_ylabel("HbS solubility (mg/mL)")

    ax.set_title(
        "HbS Solubility: Model vs Approximate Experimental Data"
    )

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    try:
        fig.savefig(
            str(GRAPH_FILE),
            dpi=300,
            format="png",
        )
    finally:
        plt.close(fig)


# =========================================================
# 8. GENERATE TEXT REPORT
# =========================================================

def save_report(results):
    """Write comparison metrics and scientific limitations."""

    with REPORT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("HbS Experimental Comparison Report\n")
        file.write("=" * 40 + "\n\n")

        file.write(
            "Reference: Henry et al. (2020), PNAS\n\n"
        )

        file.write(
            "Experimental values are approximate digitised estimates, "
            "not verified raw measurements.\n"
        )

        file.write(
            "The model's zero-oxygen reference concentration is provisional.\n\n"
        )

        file.write(
            f"Number of compared points: "
            f"{len(results['saturation'])}\n"
        )

        file.write(
            f"Mean absolute error: "
            f"{results['mae']:.4f} mg/mL\n"
        )

        file.write(
            f"Root mean square error: "
            f"{results['rmse']:.4f} mg/mL\n"
        )

        file.write(
            f"Mean absolute percentage error: "
            f"{results['mean_percentage_error']:.2f}%\n\n"
        )

        file.write(
            "INTERPRETATION\n"
            "These metrics measure agreement with the approximate "
            "digitised values only. They do not prove that the model "
            "is scientifically validated.\n"
        )


# =========================================================
# 9. MAIN PROGRAM
# =========================================================

def main():

    print("=" * 48)
    print("HbS EXPERIMENTAL COMPARISON")
    print("=" * 48)

    try:

        experimental_saturation, experimental_solubility = (
            load_experimental_data()
        )

        model_saturation, model_solubility = load_model_data()

        results = compare_datasets(
            experimental_saturation,
            experimental_solubility,
            model_saturation,
            model_solubility,
        )

        save_comparison_csv(results)
        save_comparison_graph(results)
        save_report(results)

    except (OSError, ValueError, RuntimeError) as error:

        print("\nCOMPARISON FAILED")
        print(f"Reason: {error}")
        return

    print("\nCOMPARISON COMPLETED")
    print("-" * 48)

    print(
        f"Experimental points loaded: "
        f"{len(experimental_saturation)}"
    )

    print(
        f"Model points loaded: "
        f"{len(model_saturation)}"
    )

    print(
        f"Points compared: "
        f"{len(results['saturation'])}"
    )

    print(
        f"Mean absolute error: "
        f"{results['mae']:.4f} mg/mL"
    )

    print(
        f"Root mean square error: "
        f"{results['rmse']:.4f} mg/mL"
    )

    print("\nFiles generated:")

    print(f"Graph: {GRAPH_FILE}")
    print(f"CSV: {CSV_FILE}")
    print(f"Report: {REPORT_FILE}")

    print(
        "\nNOTE: Experimental values are approximate. "
        "Scientific validation is still required."
    )


if __name__ == "__main__":
    main()