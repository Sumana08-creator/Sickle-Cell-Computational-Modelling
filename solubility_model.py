import math


def activity_coefficient(concentration):
    """
    Calculate the haemoglobin activity coefficient.

    Based on Equation 2 in Henry et al. (2020).

    Parameters:
        concentration: Haemoglobin concentration in g/mL.

    Returns:
        Activity coefficient (dimensionless).

    Note:
        This function calculates the activity coefficient only.
        It does not independently calculate HbS solubility.
    """

    if concentration <= 0:
        raise ValueError(
            "Concentration must be greater than zero."
        )

    # Hard-sphere volume parameter reported in the paper (mL/g).
    hard_sphere_volume = 0.79

    exponent = (
        8 * hard_sphere_volume * concentration
        + 15 * hard_sphere_volume**2 * concentration**2
        + 24.5 * hard_sphere_volume**3 * concentration**3
        + 35.3 * hard_sphere_volume**4 * concentration**4
        + 47.4 * hard_sphere_volume**5 * concentration**5
        + 65.9 * hard_sphere_volume**6 * concentration**6
    )

    coefficient = math.exp(exponent)

    return coefficient


def reference_solubility_zero_oxygen(temperature_c):
    """
    Calculate the empirical HbS reference solubility
    at zero oxygen saturation.

    Based on the Eaton-Hofrichter empirical relationship.

    Parameters:
        temperature_c: Temperature in degrees Celsius.

    Returns:
        Reference solubility in g/mL.

    Note:
        This is a literature-derived empirical relationship.
        Its applicability to the exact experimental conditions
        of the target model must be checked before validation.
    """

    if not -273.15 < temperature_c:
        raise ValueError(
            "Temperature must be above absolute zero."
        )

    return (
        0.321
        - 0.00883 * temperature_c
        + 0.000125 * temperature_c**2
    )


if __name__ == "__main__":

    print("HbS Solubility Model Development")
    print("================================")
    print()

    # Test 1: Activity coefficient
    test_concentration = 0.1

    coefficient = activity_coefficient(
        test_concentration
    )

    print("Activity coefficient test")
    print("-------------------------")
    print("Concentration:", test_concentration, "g/mL")
    print(
        "Calculated activity coefficient:",
        round(coefficient, 6)
    )

    print()

    # Test 2: Reference solubility at 25 degrees Celsius
    test_temperature = 25

    reference_value = reference_solubility_zero_oxygen(
        test_temperature
    )

    print("Reference solubility test")
    print("-------------------------")
    print("Temperature:", test_temperature, "C")
    print(
        "Reference solubility:",
        round(reference_value, 6),
        "g/mL"
    )

    print()
    print("Component tests completed.")
    print(
        "The complete published HbS solubility model "
        "is still under development."
    )