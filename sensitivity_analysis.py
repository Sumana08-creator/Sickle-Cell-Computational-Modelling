import csv
import complete_solubility_model as model

OUTPUT = "sensitivity_analysis_results.csv"
BASELINE = model.REFERENCE_SOLUBILITY

CONCENTRATIONS = [
    BASELINE * 0.90,
    BASELINE,
    BASELINE * 1.10,
]

MODELS = [
    ("Measured fibre binding", model.measured_fibre_saturation),
    ("MWC fibre binding", model.mwc_fibre_saturation),
    ("TTS fibre binding", model.tts_fibre_saturation),
]


def main():
    rows = []

    for name, saturation_function in MODELS:
        baseline_result = None
        model_results = []

        for concentration in CONCENTRATIONS:
            model.REFERENCE_SOLUBILITY = concentration

            pressures, values, status = model.calculate_one_model(
                saturation_function
            )

            final_value = float(values[-1])

            model_results.append({
                "model": name,
                "initial_concentration_g_mL": concentration,
                "final_pressure_torr": float(pressures[-1]),
                "final_solubility_g_mL": final_value,
                "status": status,
            })

            if abs(concentration - BASELINE) < 1e-12:
                baseline_result = final_value

        for row in model_results:
            if baseline_result is not None and baseline_result != 0:
                row["change_from_baseline_percent"] = (
                    row["final_solubility_g_mL"] / baseline_result - 1
                ) * 100
            else:
                row["change_from_baseline_percent"] = ""

            rows.append(row)

            print(
                f'{row["model"]}: '
                f'initial={row["initial_concentration_g_mL"]:.6f}, '
                f'final={row["final_solubility_g_mL"]:.6f} g/mL, '
                f'change={row["change_from_baseline_percent"]:.2f}%'
            )

    # Restore the original setting.
    model.REFERENCE_SOLUBILITY = BASELINE

    with open(OUTPUT, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "model",
            "initial_concentration_g_mL",
            "final_pressure_torr",
            "final_solubility_g_mL",
            "change_from_baseline_percent",
            "status",
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved results to {OUTPUT}")
    print("Sensitivity analysis only; experimental validation is still required.")


if __name__ == "__main__":
    main()