"""
HbS Solubility Computational Model
Reference: Henry et al. (2020), PNAS.

Uses numerical integration of the differential form of the
published solubility equation.

IMPORTANT:
The reference concentration is provisional. Numerical output
does not automatically establish scientific validity.
"""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


# =========================================================
# 1. MODEL PARAMETERS
# =========================================================

L = 60500.0
K_T = 0.016
K_R = 1.47
K_P = 0.0059

POLYMER_CONCENTRATION = 0.69       # g/mL
PARTIAL_SPECIFIC_VOLUME = 0.76     # mL/g
HARD_SPHERE_VOLUME = 0.79          # mL/g

# PROVISIONAL: verify against the original experimental data.
REFERENCE_SOLUBILITY = 0.178375    # g/mL

MAXIMUM_PRESSURE = 100.0           # torr
NUMBER_OF_POINTS = 101

OUTPUT_DIR = Path(__file__).resolve().parent

CSV_PATH = OUTPUT_DIR / "complete_solubility_results.csv"
GRAPH_PATH = OUTPUT_DIR / "complete_solubility_curve.png"

CONCENTRATION_LIMIT = POLYMER_CONCENTRATION * (1 - 1e-5)


# =========================================================
# 2. OXYGEN SATURATION MODELS
# =========================================================

def free_saturation(pressure):
    """MWC saturation of free haemoglobin."""

    p = np.asarray(pressure, dtype=float)

    t = 1.0 + K_T * p
    r = 1.0 + K_R * p

    numerator = (
        L * K_T * p * t**3
        + K_R * p * r**3
    )

    denominator = L * t**4 + r**4

    result = numerator / denominator

    return float(result) if result.ndim == 0 else result


def polymer_saturation(pressure):
    """Oxygen saturation of haemoglobin fibres."""

    p = np.asarray(pressure, dtype=float)

    result = K_P * p / (1.0 + K_P * p)

    return float(result) if result.ndim == 0 else result


# =========================================================
# 3. ACTIVITY COEFFICIENT DERIVATIVE
# =========================================================

def log_activity_derivative(concentration):
    """
    Calculate d[ln(gamma*c)]/dc.

    Derived from the hard-sphere activity-coefficient
    polynomial used in the model.
    """

    c = float(concentration)

    if c <= 0:
        raise ValueError("Concentration must be positive.")

    v = HARD_SPHERE_VOLUME

    return (
        1.0 / c
        + 8.0 * v
        + 30.0 * v**2 * c
        + 73.5 * v**3 * c**2
        + 141.2 * v**4 * c**3
        + 237.0 * v**5 * c**4
        + 395.4 * v**6 * c**5
    )


# =========================================================
# 4. WATER-VOLUME RATIO
# =========================================================

def water_volume_ratio(concentration):
    """Calculate the concentration-dependent volume ratio."""

    numerator = (
        1.0 / POLYMER_CONCENTRATION
        - PARTIAL_SPECIFIC_VOLUME
    )

    denominator = (
        1.0 / concentration
        - PARTIAL_SPECIFIC_VOLUME
    )

    if abs(denominator) < 1e-12:
        raise ValueError(
            "Water-volume denominator approaches zero."
        )

    return numerator / denominator


# =========================================================
# 5. DIFFERENTIAL EQUATION
# =========================================================

def solubility_ode(pressure, state):
    """
    Differential form of the solubility equation:

    d ln(gamma*c)/dp =
        4*(ys - yp) / [p*(1 - volume_ratio)]

    At zero pressure, use the analytical limiting value
    for (ys - yp)/p.
    """

    concentration = float(state[0])

    # Prevent intermediate solver evaluations from reaching
    # the near-singular polymer-concentration boundary.
    concentration = float(
        np.clip(
            concentration,
            1e-10,
            CONCENTRATION_LIMIT
        )
    )

    volume_ratio = water_volume_ratio(concentration)

    denominator = 1.0 - volume_ratio

    if abs(denominator) < 1e-12:
        raise FloatingPointError(
            "The equation denominator approaches zero."
        )

    if pressure < 1e-7:

        # Analytical limit as oxygen pressure approaches zero.
        saturation_difference_per_pressure = (
            (L * K_T + K_R) / (L + 1.0)
            - K_P
        )

    else:

        ys = free_saturation(pressure)
        yp = polymer_saturation(pressure)

        saturation_difference_per_pressure = (
            (ys - yp) / pressure
        )

    derivative = (
        4.0 * saturation_difference_per_pressure
        /
        (
            denominator
            * log_activity_derivative(concentration)
        )
    )

    return [derivative]


# =========================================================
# 6. STOP EVENT
# =========================================================

def concentration_limit_event(pressure, state):
    """Stop before reaching the near-singular boundary."""

    return CONCENTRATION_LIMIT - float(state[0])


concentration_limit_event.terminal = True
concentration_limit_event.direction = -1


# =========================================================
# 7. SOLVE THE MODEL
# =========================================================

def calculate_solubility_curve(
    maximum_pressure=MAXIMUM_PRESSURE,
    number_of_points=NUMBER_OF_POINTS,
):
    """Numerically integrate the solubility differential equation."""

    if maximum_pressure <= 0:
        raise ValueError(
            "Maximum pressure must be positive."
        )

    if number_of_points < 2:
        raise ValueError(
            "At least two output points are required."
        )

    if not (
        0 < REFERENCE_SOLUBILITY < POLYMER_CONCENTRATION
    ):
        raise ValueError(
            "Reference concentration must be positive "
            "and below polymer concentration."
        )

    evaluation_pressures = np.linspace(
        0.0,
        maximum_pressure,
        number_of_points,
    )

    solution = solve_ivp(
        fun=solubility_ode,
        t_span=(0.0, maximum_pressure),
        y0=[REFERENCE_SOLUBILITY],
        method="Radau",
        t_eval=evaluation_pressures,
        events=concentration_limit_event,
        rtol=1e-8,
        atol=1e-10,
        max_step=0.1,
    )

    if not solution.success:
        raise RuntimeError(
            f"Numerical solver failed: {solution.message}"
        )

    if solution.t.size == 0:
        raise RuntimeError(
            "The solver returned no usable results."
        )

    reached_limit = bool(solution.t_events[0].size)

    if reached_limit:
        status = (
            "PARTIAL: calculation stopped because concentration "
            "approached the model boundary."
        )

    elif solution.t[-1] < maximum_pressure - 1e-8:
        status = (
            "PARTIAL: calculation stopped before maximum pressure."
        )
        reached_limit = True

    else:
        status = (
            "COMPLETED: numerical integration finished; "
            "experimental validation is still required."
        )

    return (
        solution.t,
        solution.y[0],
        status,
        reached_limit,
    )


# =========================================================
# 8. EXPORT CSV
# =========================================================

def save_results(pressures, concentrations, status):
    """Save calculated results to CSV."""

    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "oxygen_pressure_torr",
            "free_hbs_saturation_fraction",
            "polymer_saturation_fraction",
            "calculated_solubility_g_per_ml",
            "reference_status",
            "calculation_status",
        ])

        for pressure, concentration in zip(
            pressures,
            concentrations,
        ):

            writer.writerow([
                f"{pressure:.6f}",
                f"{free_saturation(pressure):.8f}",
                f"{polymer_saturation(pressure):.8f}",
                f"{concentration:.8f}",
                "PROVISIONAL",
                status,
            ])


# =========================================================
# 9. CREATE GRAPH
# =========================================================

def save_graph(
    pressures,
    concentrations,
    reached_limit,
):
    """Save the calculated solubility curve."""

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        pressures,
        concentrations * 1000.0,
        label="Numerical model",
    )

    ax.set_title(
        "HbS Solubility vs Oxygen Pressure"
    )

    ax.set_xlabel("Oxygen pressure (torr)")
    ax.set_ylabel("Solubility (mg/mL)")

    ax.grid(True, alpha=0.3)

    if reached_limit:

        ax.set_title(
            "HbS Solubility vs Oxygen Pressure "
            "(Calculation Stopped Early)"
        )

        ax.text(
            0.02,
            0.97,
            "Partial calculation: model boundary approached",
            transform=ax.transAxes,
            va="top",
        )

    ax.legend()
    fig.tight_layout()

    try:
        fig.savefig(
            GRAPH_PATH,
            dpi=300,
            format="png",
        )

    finally:
        plt.close(fig)


# =========================================================
# 10. MAIN PROGRAM
# =========================================================

def main():

    print("=" * 48)
    print("HbS SOLUBILITY COMPUTATIONAL MODEL")
    print("=" * 48)

    print("Reference: Henry et al. (2020), PNAS")
    print(
        "Reference concentration:",
        f"{REFERENCE_SOLUBILITY:.6f} g/mL",
    )
    print("Reference status: PROVISIONAL")
    print("Solver: SciPy Radau")
    print()

    try:

        pressures, concentrations, status, reached_limit = (
            calculate_solubility_curve()
        )

    except (
        ValueError,
        RuntimeError,
        FloatingPointError,
    ) as error:

        print("CALCULATION FAILED")
        print(f"Reason: {error}")
        print(
            "No validated result has been produced."
        )

        return

    save_results(
        pressures,
        concentrations,
        status,
    )

    save_graph(
        pressures,
        concentrations,
        reached_limit,
    )

    print("FIRST FIVE RESULTS")
    print("-" * 48)

    for pressure, concentration in zip(
        pressures[:5],
        concentrations[:5],
    ):

        print(
            f"{pressure:7.2f} torr | "
            f"{concentration:.6f} g/mL | "
            f"{concentration * 1000:.2f} mg/mL"
        )

    print()
    print(f"Last pressure calculated: {pressures[-1]:.2f} torr")

    print(
        "Last calculated solubility:",
        f"{concentrations[-1]:.6f} g/mL",
    )

    print(
        f"Points calculated: {len(pressures)} "
        f"of {NUMBER_OF_POINTS}"
    )

    print(f"CSV saved: {CSV_PATH}")
    print(f"Graph saved: {GRAPH_PATH}")

    print()
    print("STATUS:")
    print(status)

    print()
    print(
        "IMPORTANT: Verify the reference concentration and "
        "compare the model against experimental data before "
        "drawing scientific conclusions."
    )


if __name__ == "__main__":
    main()