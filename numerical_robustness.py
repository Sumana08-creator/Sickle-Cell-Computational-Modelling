"""
Numerical robustness analysis for the HbS solubility model.

Compares solver tolerances for all three fibre-binding models.
This tests numerical convergence, not experimental validity.
"""

import csv
from pathlib import Path

import numpy as np
import complete_solubility_model as model


OUTPUT_FILE = Path("numerical_robustness_results.csv")

# Progressively tighter solver tolerances.
TOLERANCES = [
    {"rtol": 1e-6, "atol": 1e-8},
    {"rtol": 1e-8, "atol": 1e-10},
    {"rtol": 1e-10, "atol": 1e-12},
]

MODELS = [
    ("Measured fibre binding", model.measured_fibre_saturation),
    ("MWC fibre binding", model.mwc_fibre_saturation),
    ("TTS fibre binding", model.tts_fibre_saturation),
]


def solve_with_tolerance(saturation_function, rtol, atol):
    """Run the existing ODE with specified solver tolerances."""

    pressures = np.linspace(
        0.0,
        model.MAXIMUM_PRESSURE,
        model.NUMBER_OF_POINTS,
    )

    ode = model.make_solubility_ode(saturation_function)

    solution = model.solve_ivp(
        fun=ode,
        t_span=(0.0, model.MAXIMUM_PRESSURE),
        y0=[model.REFERENCE_SOLUBILITY],
        method="Radau",
        t_eval=pressures,
        events=model.concentration_limit_event,
        rtol=rtol,
        atol=atol,
        max_step=0.1,
    )

    if not solution.success:
        raise RuntimeError(solution.message)

    if solution.t.size == 0:
        raise RuntimeError("Solver returned no results.")

    if solution.t[-1] < model.MAXIMUM_PRESSURE - 1e-8:
        raise RuntimeError(
            f"Integration stopped early at {solution.t[-1]:.6f} torr."
        )

    final_value = float(solution.y[0, -1])

    if not np.isfinite(final_value):
        raise ValueError("Final concentration is not finite.")

    return solution.t, solution.y[0], final_value


def main():
    rows = []
    reference_values = {}

    print("=" * 68)
    print("NUMERICAL ROBUSTNESS ANALYSIS")
    print("=" * 68)
    print(f"Initial concentration: {model.REFERENCE_SOLUBILITY:.6f} g/mL")
    print(f"Maximum pressure: {model.MAXIMUM_PRESSURE:.1f} torr")
    print()

    for model_name, saturation_function in MODELS:
        print(model_name)

        reference_values[model_name] = None

        for settings in TOLERANCES:
            rtol = settings["rtol"]
            atol = settings["atol"]

            try:
                pressures, concentrations, final_value = solve_with_tolerance(
                    saturation_function,
                    rtol,
                    atol,
                )

                if reference_values[model_name] is None:
                    reference_values[model_name] = final_value

                reference = reference_values[model_name]

                difference = abs(final_value - reference)

                relative_difference = (
                    difference / abs(reference) * 100
                    if reference != 0
                    else 0.0
                )

                row = {
                    "model": model_name,
                    "rtol": rtol,
                    "atol": atol,
                    "final_pressure_torr": float(pressures[-1]),
                    "final_solubility_g_mL": final_value,
                    "absolute_difference_from_first_run_g_mL": difference,
                    "relative_difference_from_first_run_percent":
                        relative_difference,
                    "status": "COMPLETED",
                }

                rows.append(row)

                print(
                    f"  rtol={rtol:.0e}, atol={atol:.0e}: "
                    f"{final_value:.8f} g/mL; "
                    f"difference={relative_difference:.6g}%"
                )

            except Exception as error:
                print(f"  FAILED at rtol={rtol:.0e}: {error}")

                rows.append({
                    "model": model_name,
                    "rtol": rtol,
                    "atol": atol,
                    "final_pressure_torr": "",
                    "final_solubility_g_mL": "",
                    "absolute_difference_from_first_run_g_mL": "",
                    "relative_difference_from_first_run_percent": "",
                    "status": f"FAILED: {error}",
                })

        print()

    fieldnames = [
        "model",
        "rtol",
        "atol",
        "final_pressure_torr",
        "final_solubility_g_mL",
        "absolute_difference_from_first_run_g_mL",
        "relative_difference_from_first_run_percent",
        "status",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("=" * 68)
    print(f"Results saved to: {OUTPUT_FILE.resolve()}")
    print("Interpretation:")
    print("- Small differences suggest numerical convergence.")
    print("- Large differences require investigation.")
    print("- Numerical convergence does not establish experimental accuracy.")
    print("=" * 68)


if __name__ == "__main__":
    main()