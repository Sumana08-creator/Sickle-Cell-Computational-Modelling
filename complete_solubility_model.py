import numpy as np
from scipy.integrate import solve_ivp

from mwc_binding import mwc_saturation
from fiber_binding import fiber_saturation


# Parameters reported by Henry et al. (2020)
L = 60500
K_T = 0.016
K_R = 1.47
K_P = 0.0059

# Concentration parameters
# Concentration: g/mL
# Partial specific volume: mL/g
POLYMER_CONCENTRATION = 0.69
PARTIAL_SPECIFIC_VOLUME = 0.76

# PROVISIONAL reference solubility.
# Verify its source and applicability before interpreting
# the results as scientifically validated predictions.
REFERENCE_SOLUBILITY = 0.178375


def activity_log_derivative(concentration):
    """
    Calculate d[ln(gamma * concentration)]/d concentration.

    Based on the hard-sphere activity-coefficient equation.
    """

    if concentration <= 0:
        raise ValueError(
            "Concentration must be positive."
        )

    V = 0.79

    derivative = (
        8 * V
        + 30 * V**2 * concentration
        + 73.5 * V**3 * concentration**2
        + 141.2 * V**4 * concentration**3
        + 237 * V**5 * concentration**4
        + 395.4 * V**6 * concentration**5
    )

    return derivative + 1 / concentration

def solubility_ode(pressure, state):
    """Differential form of Equation 1 from Henry et al. (2020)."""

    concentration = float(state[0])

    if concentration <= 0:
        raise ValueError("Solubility must remain positive.")

    free_saturation = mwc_saturation(
        pressure, L, K_T, K_R
    )

    fibre_saturation_value = fiber_saturation(
        pressure, K_P
    )

    # Calculate the saturation difference per unit pressure.
    if pressure < 1e-8:
        free_initial_slope = (
            L * K_T + K_R
        ) / (L + 1)

        saturation_difference_per_pressure = (
            free_initial_slope - K_P
        )
    else:
        saturation_difference_per_pressure = (
            free_saturation - fibre_saturation_value
        ) / pressure

    water_volume_ratio = (
        (1 / POLYMER_CONCENTRATION - PARTIAL_SPECIFIC_VOLUME)
        / (1 / concentration - PARTIAL_SPECIFIC_VOLUME)
    )

    denominator = 1 - water_volume_ratio

    if abs(denominator) < 1e-12:
        raise ValueError(
            f"Concentration-dependent denominator approaches zero "
            f"at pressure {pressure:.4f} torr; "
            f"concentration {concentration:.6f} g/mL."
        )

    right_hand_side = (
        4 * saturation_difference_per_pressure / denominator
    )

    derivative_factor = activity_log_derivative(concentration)

    d_concentration_d_pressure = (
        right_hand_side / derivative_factor
    )

    return [d_concentration_d_pressure]

def calculate_solubility_curve(
    reference_solubility,
    maximum_pressure=100,
    number_of_points=101,
):
    """
    Calculate HbS solubility across oxygen pressures.

    Returns
    -------
    pressures : numpy.ndarray
        Oxygen pressures in torr.

    solubilities : numpy.ndarray
        Calculated solubilities in g/mL.
    """

    if reference_solubility <= 0:
        raise ValueError(
            "Reference solubility must be positive."
        )

    if maximum_pressure <= 0:
        raise ValueError(
            "Maximum pressure must be positive."
        )

    if number_of_points < 2:
        raise ValueError(
            "At least two points are required."
        )

    pressures = np.linspace(
        0,
        maximum_pressure,
        number_of_points,
    )

    result = solve_ivp(
        solubility_ode,
        (0, maximum_pressure),
        [reference_solubility],
        t_eval=pressures,
        rtol=1e-8,
        atol=1e-10,
    )

    if not result.success:
        raise RuntimeError(
            f"Solubility calculation failed: {result.message}"
        )

    if not np.all(np.isfinite(result.y[0])):
        raise RuntimeError(
            "The calculation produced invalid numerical values."
        )

    return result.t, result.y[0]


if __name__ == "__main__":

    print("Complete HbS Solubility Model")
    print("=============================")
    print()

    print(
        "Reference solubility:",
        REFERENCE_SOLUBILITY,
        "g/mL",
    )

    print(
        "WARNING: The reference value is provisional. "
        "Scientific validation is required."
    )

    print()

    pressures, solubilities = calculate_solubility_curve(
        REFERENCE_SOLUBILITY
    )

    print("First five calculated points")
    print("----------------------------")

    for pressure, solubility in zip(
        pressures[:5],
        solubilities[:5],
    ):
        print(
            f"Pressure: {pressure:6.2f} torr | "
            f"Solubility: {solubility:.6f} g/mL"
        )

    print()

    print(
        "Final calculated solubility:",
        f"{solubilities[-1]:.6f} g/mL",
    )

    print(
        "Calculated points:",
        len(solubilities),
    )

    print()
    print("Numerical calculation completed.")
    print(
        "Scientific validation against published "
        "measurements is still required."
    )