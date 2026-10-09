def fiber_saturation(po2, k_p):
    """
    Calculate fractional oxygen saturation of haemoglobin fibres.

    Based on Equation 4 in Henry et al. (2020).

    Parameters:
        po2: Oxygen partial pressure in torr.
        k_p: Oxygen-binding constant for the fibres, in inverse torr.

    Returns:
        Fractional oxygen saturation between 0 and 1.

    This function models oxygen binding by fibres.
    It does not independently predict fibre formation or its rate.
    """

    if po2 < 0:
        raise ValueError("Oxygen pressure cannot be negative.")

    if k_p <= 0:
        raise ValueError("k_p must be positive.")

    return (k_p * po2) / (1 + k_p * po2)


if __name__ == "__main__":
    # Reported fibre-binding parameter for the study's
    # specified experimental conditions.
    k_p = 0.0059

    print("Haemoglobin fibre oxygen-binding model")
    print("--------------------------------------")

    for po2 in [0, 10, 20, 40, 60, 100]:
        saturation = fiber_saturation(po2, k_p)

        print(
            f"PO2 = {po2:>3} torr | "
            f"Fibre saturation = {saturation * 100:.2f}%"
        )