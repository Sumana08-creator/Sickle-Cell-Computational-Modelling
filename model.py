def calculate_polymerisation_proxy(oxygen_saturation, hbf_percentage):
    if not 0 <= oxygen_saturation <= 100:
        raise ValueError("Oxygen saturation must be between 0 and 100.")

    if not 0 <= hbf_percentage <= 100:
        raise ValueError("HbF percentage must be between 0 and 100.")
    """
    Calculate a simplified, illustrative polymerisation proxy.

    This is a teaching model, not a validated biological prediction.
    """

    deoxygenation_fraction = 1 - (oxygen_saturation / 100)

    hbf_fraction = hbf_percentage / 100

    illustrative_proxy = deoxygenation_fraction * (1 - hbf_fraction)

    return illustrative_proxy
if __name__ == "__main__":
    print("Testing the illustrative model")
    print("-------------------------------")

    oxygen = 50
    hbf = 10

    result = calculate_polymerisation_proxy(oxygen, hbf)

    print("Oxygen input:", oxygen, "%")
    print("HbF input:", hbf, "%")
    print("Illustrative score:", round(result, 3))