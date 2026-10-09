"""
HbS solubility: approximate comparison with Henry et al. (2020).

The points below are approximate values digitised visually from Figure 3.
They are not the authors' raw experimental data.
"""

import csv
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_DIR = Path(__file__).resolve().parent

# Approximate readings from Figure 3.
# Saturation is a fraction; solubility is in mg/cc.
# 1 mg/cc = 0.001 g/mL.
SATURATION = np.array([
    0.00, 0.10, 0.20, 0.35, 0.50,
    0.65, 0.75, 0.85, 0.90, 0.95, 0.98
])

SOLUBILITY_MG_CC = np.array([
    175, 195, 205, 225, 250,
    280, 310, 355, 390, 430, 475
])

SOLUBILITY_G_ML = SOLUBILITY_MG_CC / 1000.0


def main():
    csv_path = OUTPUT_DIR / "figure3_approximate_data.csv"
    graph_path = OUTPUT_DIR / "figure3_experimental_comparison.png"

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "oxygen_saturation_fraction",
            "oxygen_saturation_percent",
            "approx_solubility_mg_per_cc",
            "approx_solubility_g_per_ml",
        ])

        for sat, mgcc, gml in zip(
            SATURATION, SOLUBILITY_MG_CC, SOLUBILITY_G_ML
        ):
            writer.writerow([sat, sat * 100, mgcc, gml])

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        SATURATION * 100,
        SOLUBILITY_MG_CC,
        "o-",
        label="Approximate readings from Figure 3",
    )

    ax.set_title(
        "HbS Solubility vs Oxygen Saturation\n"
        "Approximate digitisation of Henry et al. (2020), Fig. 3"
    )
    ax.set_xlabel("Oxygen saturation (%)")
    ax.set_ylabel("Solubility (mg/cc)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    try:
        fig.savefig(graph_path, dpi=300)
    finally:
        plt.close(fig)

    print("Experimental comparison dataset created.")
    print("IMPORTANT: Values are approximate figure readings.")
    print("They are not raw experimental measurements.")
    print(f"CSV: {csv_path}")
    print(f"Graph: {graph_path}")


if __name__ == "__main__":
    main()