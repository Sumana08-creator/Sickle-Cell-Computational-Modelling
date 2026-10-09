import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


TEMPERATURE_C = 25.0

OUTPUT_DIRECTORY = Path(__file__).resolve().parent
CSV_PATH = OUTPUT_DIRECTORY / "empirical_solubility_results.csv"
GRAPH_PATH = OUTPUT_DIRECTORY / "empirical_solubility_curve_new.png"

def calculate_solubility(temperature_c, saturation):
    """Calculate estimated HbS solubility in g/mL."""

    saturation = np.asarray(saturation, dtype=float)

    if np.any((saturation < 0) | (saturation > 1)):
        raise ValueError(
            "Oxygen saturation must be between 0 and 1."
        )

    return (
        0.321
        - 0.00883 * temperature_c
        + 0.000125 * temperature_c**2
        + 0.0924 * saturation
        + 0.0980 * saturation**3
        + 0.235 * saturation**15
    )


def main():
    print("Empirical HbS Solubility Model")
    print("==============================")
    print(f"Temperature: {TEMPERATURE_C:.1f} °C")
    print()
    print("WARNING: Verify the equation against its original source.")
    print("Results are calculated estimates, not experimental measurements.")
    print()

    saturations = np.linspace(0, 1, 101)

    solubilities = calculate_solubility(
        TEMPERATURE_C,
        saturations,
    )

    # Save calculated results
    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "temperature_c",
            "oxygen_saturation_fraction",
            "oxygen_saturation_percent",
            "calculated_solubility_g_per_ml",
        ])

        for saturation, solubility in zip(
            saturations,
            solubilities,
        ):
            writer.writerow([
                TEMPERATURE_C,
                f"{saturation:.4f}",
                f"{saturation * 100:.2f}",
                f"{solubility:.6f}",
            ])

    # Create and save graph
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        saturations * 100,
        solubilities,
        label="Empirical equation",
    )

    ax.set_title("Estimated HbS Solubility vs Oxygen Saturation")
    ax.set_xlabel("Oxygen saturation (%)")
    ax.set_ylabel("Calculated solubility (g/mL)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    try:
        fig.savefig(
            str(GRAPH_PATH),
            dpi=300,
            format="png",
        )
    finally:
        plt.close(fig)

    # Display results
    print("First five calculated points")
    print("----------------------------")

    for saturation, solubility in zip(
        saturations[:5],
        solubilities[:5],
    ):
        print(
            f"Saturation: {saturation * 100:6.2f}% | "
            f"Solubility: {solubility:.6f} g/mL"
        )

    print()
    print(f"At 0% saturation:   {solubilities[0]:.6f} g/mL")
    print(f"At 100% saturation: {solubilities[-1]:.6f} g/mL")
    print(f"Calculated points: {len(saturations)}")
    print(f"CSV saved: {CSV_PATH}")
    print(f"Graph saved: {GRAPH_PATH}")
    print()
    print("Calculation completed.")


if __name__ == "__main__":
    main()