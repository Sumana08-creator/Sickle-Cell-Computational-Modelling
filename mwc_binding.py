def mwc_saturation(po2, L, K_T, K_R):
    """
    Calculate fractional oxygen saturation using the MWC model.

    Equation 3 from Henry et al. (2020).

    Parameters:
        po2: Oxygen partial pressure in torr (approximately mmHg).
        L: Allosteric equilibrium parameter.
        K_T: Oxygen-binding constant for the T state, in inverse torr.
        K_R: Oxygen-binding constant for the R state, in inverse torr.

    Returns:
        Fractional oxygen saturation between 0 and 1.

    Note:
        The parameters must correspond to the experimental conditions
        being modelled. This function alone does not predict HbS
        polymerisation.
    """

    if po2 < 0:
        raise ValueError("Oxygen pressure cannot be negative.")

    if L <= 0 or K_T <= 0 or K_R <= 0:
        raise ValueError("L, K_T, and K_R must be positive.")

    numerator = (
        L * K_T * po2 * (1 + K_T * po2) ** 3
        + K_R * po2 * (1 + K_R * po2) ** 3
    )

    denominator = (
        L * (1 + K_T * po2) ** 4
        + (1 + K_R * po2) ** 4
    )

    return numerator / denominator


if __name__ == "__main__":
    # Parameters reported for the paper's oxygen-binding
    # measurements at 25 °C under specified laboratory conditions.
    L = 60500
    K_T = 0.016
    K_R = 1.47

    print("Published MWC oxygen-binding model")
    print("----------------------------------")

    for po2 in [0, 10, 20, 40, 60, 100]:
        saturation = mwc_saturation(po2, L, K_T, K_R)

        print(
            f"PO2 = {po2:>3} torr | "
            f"Saturation = {saturation * 100:.2f}%"
        )