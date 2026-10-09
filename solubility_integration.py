from scipy.integrate import quad

from mwc_binding import mwc_saturation
from fiber_binding import fiber_saturation


def integrate_saturation_difference(
    free_saturation_function,
    fibre_saturation_function,
    start_pressure,
    end_pressure,
):
    """
    Numerically integrate the difference between free haemoglobin
    and fibre oxygen saturation.

    This is an intermediate mathematical calculation, not the
    complete published HbS solubility equation.
    """

    if start_pressure < 0:
        raise ValueError("Start pressure cannot be negative.")

    if end_pressure < start_pressure:
        raise ValueError(
            "End pressure must be greater than or equal to start pressure."
        )

    def integrand(oxygen_pressure):
        free_saturation = free_saturation_function(oxygen_pressure)
        fibre_saturation = fibre_saturation_function(oxygen_pressure)

        return free_saturation - fibre_saturation

    result, estimated_error = quad(
        integrand,
        start_pressure,
        end_pressure,
    )

    return result, estimated_error


def reference_solubility_zero_oxygen(temperature_c):
    """
    Calculate a provisional reference-solubility estimate.

    IMPORTANT:
    The temperature relationship below has not yet been verified
    for the precise experimental conditions in the target paper.
    Do not use this estimate for biological predictions until
    its source and applicability have been confirmed.
    """

    return (
        0.321
        - 0.00883 * temperature_c
        + 0.000125 * temperature_c**2
    )


if __name__ == "__main__":

    # Parameters reported for the oxygen-binding models
    # in Henry et al. (2020).
    L = 60500
    K_T = 0.016
    K_R = 1.47
    K_P = 0.0059

    # Connect the existing oxygen-binding models.
    free_function = lambda pressure: mwc_saturation(
        pressure, L, K_T, K_R
    )

    fibre_function = lambda pressure: fiber_saturation(
        pressure, K_P
    )

    # Integrate over an oxygen-pressure range of 0–100 torr.
    integral, error = integrate_saturation_difference(
        free_function,
        fibre_function,
        0,
        100,
    )

    print("HbS Solubility Model Development")
    print("================================")
    print()

    print(
        "Integrated saturation difference:",
        round(integral, 6),
    )

    print(
        "Estimated numerical integration error:",
        f"{error:.2e}",
    )

    print()

    # Test the provisional reference-solubility function.
    reference_value = reference_solubility_zero_oxygen(25)

    print("Temperature used for reference test: 25 C")
    print(
        "Provisional reference-solubility estimate:",
        round(reference_value, 6),
        "g/mL",
    )

    print()
    print("Integration component test completed.")
    print(
        "The complete published HbS solubility equation "
        "is still under development."
    )