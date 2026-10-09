def hill_saturation(po2, p50, hill_coefficient):
    """
    Calculate fractional oxygen saturation using the Hill equation.

    This models oxygen binding, not HbS polymerisation.
    """

    if po2 < 0:
        raise ValueError("Oxygen partial pressure cannot be negative.")

    if p50 <= 0:
        raise ValueError("P50 must be greater than zero.")

    if hill_coefficient <= 0:
        raise ValueError("Hill coefficient must be greater than zero.")

    numerator = po2 ** hill_coefficient

    denominator = (
        p50 ** hill_coefficient
        + numerator
    )

    return numerator / denominator