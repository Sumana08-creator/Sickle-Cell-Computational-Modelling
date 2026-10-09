"""
HbS Solubility Computational Model
==================================

Reference:
Henry et al. (2020), PNAS.
Allosteric control of hemoglobin S fiber formation by oxygen
and its relation to the pathophysiology of sickle cell disease.

Implements the integral form of the published solubility equation.

IMPORTANT:
- The zero-oxygen reference concentration is provisional.
- Numerical output is not automatically scientifically validated.
- Compare results with experimental measurements before interpretation.
"""

import csv
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import brentq

from mwc_binding import mwc_saturation
from fiber_binding import fiber_saturation


# ---------------------------------------------------------
# Published parameters from Henry et al. (2020)
# ---------------------------------------------------------

L = 60500.0
K_T = 0.016
K_R = 1.47
K_P = 0.0059

POLYMER_CONCENTRATION = 0.69       # g/mL
PARTIAL_SPECIFIC_VOLUME = 0.76     # mL/g
HARD_SPHERE_VOLUME = 0.79          # mL/g

# Provisional reference value: source and applicability
# must be verified against the original experimental data.
REFERENCE_SOLUBILITY = 0.178375    # g/mL

MAXIMUM_PRESSURE = 100.0           # torr
NUMBER_OF_POINTS = 101

OUTPUT_DIRECTORY = Path(__file__).resolve().parent

CSV_PATH = OUTPUT_DIRECTORY / "complete_solubility_results.csv"
GRAPH_PATH = OUTPUT_DIRECTORY / "complete_solubility_curve.png"


# ---------------------------------------------------------
# Activity coefficient
# ---------------------------------------------------------

def activity_coefficient(concentration):
    """Calculate the hard-sphere activity coefficient."""

    if not 0 < concentration < 1 / PARTIAL_SPECIFIC_VOLUME:
        raise ValueError("Concentration is outside the valid range.")

    V = HARD_SPHERE_VOLUME
    c = concentration

    exponent = (
        8 * V * c
        + 15 * V**2 * c**2
        + 24.5 * V**3 * c**3
        + 35.3 * V**4 * c**4
        + 47.4 * V**5 * c**5
        + 65.9 * V**6 * c**6
    )

    return float(np.exp(exponent))


def log_activity(concentration):
    """Calculate ln(gamma * concentration)."""

    return float(
        np.log(activity_coefficient(concentration))
        + np.log(concentration)
    )


# ---------------------------------------------------------
# Oxygen saturation models
# ---------------------------------------------------------

def free_saturation(pressure):
    """Fractional oxygen saturation of free HbS tetramers."""

    return float(
        mwc_saturation(pressure, L, K_T, K_R)
    )


def polymer_saturation(pressure):
    """Fractional oxygen saturation of HbS fibres."""

    return float(
        fiber_saturation(pressure, K_P)
    )


# ---------------------------------------------------------
# Published solubility-equation components
# ---------------------------------------------------------

def water_volume_ratio(concentration):
    """Calculate the water-volume ratio in Equation 1."""

    numerator = (
        1.0 / POLYMER_CONCENTRATION
        - PARTIAL_SPECIFIC_VOLUME
    )

    denominator = (
        1.0 / concentration
        - PARTIAL_SPECIFIC_VOLUME
    )

    if abs(denominator) < 1e-12:
        raise ValueError("Water-volume denominator approaches zero.")

    return numerator / denominator


def equation_integrand(pressure, concentration):
    """
    Integrand of the solubility equation.

    Do not divide the saturation difference by pressure.
    """

    ys = free_saturation(pressure)
    yp = polymer_saturation(pressure)

    denominator = 1.0 - water_volume_ratio(concentration)

    if abs(denominator) < 1e-10:
        raise ValueError("Equation denominator approaches zero.")

    return 4.0 * (ys - yp) / denominator


# ---------------------------------------------------------
# Numerical solution
# ---------------------------------------------------------

def calculate_solubility_at_pressure(pressure):
    """
    Calculate the concentration satisfying the integral equation.

    Raises an informative error if no numerical root is found.
    It never substitutes a fabricated result.
    """

    if pressure < 0:
        raise ValueError("Pressure cannot be negative.")

    if REFERENCE_SOLUBILITY <= 0:
        raise ValueError("Reference solubility must be positive.")

    if pressure == 0:
        return REFERENCE_SOLUBILITY

    initial_log_activity = log_activity(REFERENCE_SOLUBILITY)

    def residual(concentration):
        try:
            integral, _ = quad(
                lambda p: equation_integrand(p, concentration),
                0.0,
                pressure,
                epsabs=1e-8,
                epsrel=1e-8,
                limit=200,
            )

            return (
                log_activity(concentration)
                - initial_log_activity
                - integral
            )

        except (ValueError, OverflowError, FloatingPointError):
            return np.nan

    # Scan for a sign change to identify a candidate root.
    concentrations = np.linspace(
        0.001,
        POLYMER_CONCENTRATION - 0.001,
        300,
    )

    previous_concentration = None
    previous_residual = None

    for concentration in concentrations:
        concentration = float(concentration)
        current_residual = residual(concentration)

        if not np.isfinite(current_residual):
            previous_concentration = None
            previous_residual = None
            continue

        if previous_residual is not None:
            if previous_residual * current_residual < 0:
                try:
                    root = brentq(
                        residual,
                        previous_concentration,
                        concentration,
                        xtol=1e-10,
                        rtol=1e-10,
                        maxiter=200,
                    )

                    return float(root)

                except (ValueError, RuntimeError):
                    pass

        previous_concentration = concentration
        previous_residual = current_residual

    raise RuntimeError(
        f"No valid numerical solution was found at "
        f"{pressure:.2f} torr. Review the equation, reference "
        "concentration, and model assumptions. No prediction "
        "has been fabricated."
    )


def calculate_solubility_curve(
    maximum_pressure=MAXIMUM_PRESSURE,
    number_of_points=NUMBER_OF_POINTS,
):
    """Calculate solubility over a range of oxygen pressures."""

    if maximum_pressure <= 0:
        raise ValueError("Maximum pressure must be positive.")

    if number_of_points < 2:
        raise ValueError("At least two points are required.")

    pressures = np.linspace(
        0.0,
        maximum_pressure,
        number_of_points,
    )

    solubilities = []

    for pressure in pressures:
        solubility = calculate_solubility_at_pressure(
            float(pressure)
        )
        solubilities.append(solubility)

    return pressures, np.asarray(solubilities)


# ---------------------------------------------------------
# Export results
# ---------------------------------------------------------

def save_results(pressures, solubilities):
    """Save calculated results to CSV."""

    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "oxygen_pressure_torr",
            "free_hbs_saturation",
            "polymer_saturation",
            "calculated_solubility_g_per_ml",
            "reference_value_status",
        ])

        for pressure, concentration in zip(
            pressures,
            solubilities,
        ):
            writer.writerow([
                f"{pressure:.6f}",
                f"{free_saturation(pressure):.8f}",
                f"{polymer_saturation(pressure):.8f}",
                f"{concentration:.8f}",
                "provisional",
            ])


def save_graph(pressures, solubilities):
    """Save the calculated solubility curve."""

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        pressures,
        solubilities * 1000,
        label="Calculated solubility",
    )

    ax.set_title("HbS Solubility vs Oxygen Pressure")
    ax.set_xlabel("Oxygen pressure (torr)")
    ax.set_ylabel("Solubility (mg/mL)")
    ax.grid(True, alpha=0.3)
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


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main():
    print("HbS Solubility Computational Model")
    print("==================================")
    print("Reference: Henry et al. (2020), PNAS")
    print(f"Reference solubility: {REFERENCE_SOLUBILITY:.6f} g/mL")
    print("Reference status: PROVISIONAL")
    print()

    try:
        pressures, solubilities = calculate_solubility_curve()

    except (ValueError, RuntimeError, FloatingPointError) as error:
        print("CALCULATION NOT COMPLETED")
        print(f"Reason: {error}")
        print()
        print(
            "The model needs further mathematical or scientific "
            "review. No results have been reported as validated."
        )
        return

    save_results(pressures, solubilities)
    save_graph(pressures, solubilities)

    print("First five calculated points")
    print("----------------------------")

    for pressure, concentration in zip(
        pressures[:5],
        solubilities[:5],
    ):
        print(
            f"Pressure: {pressure:6.2f} torr | "
            f"Solubility: {concentration:.6f} g/mL"
        )

    print()
    print(
        "Final calculated solubility:",
        f"{solubilities[-1]:.6f} g/mL",
    )
    print(f"Calculated points: {len(solubilities)}")
    print(f"CSV saved: {CSV_PATH}")
    print(f"Graph saved: {GRAPH_PATH}")
    print()
    print("Scientific validation against experimental data is required.")


if __name__ == "__main__":
    main()