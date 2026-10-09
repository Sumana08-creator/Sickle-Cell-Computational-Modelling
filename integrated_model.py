from oxygen_binding import hill_saturation
from model import calculate_polymerisation_proxy


def run_integrated_model(po2, p50, hill_coefficient, hbf_percentage):
    """
    Connect oxygen binding to the illustrative polymerisation proxy.

    This is an educational demonstration, not a validated
    prediction of HbS polymerisation.
    """

    oxygen_saturation = hill_saturation(
        po2,
        p50,
        hill_coefficient
    )

    proxy = calculate_polymerisation_proxy(
        oxygen_saturation * 100,
        hbf_percentage
    )

    return oxygen_saturation, proxy


if __name__ == "__main__":
    po2 = 26.6
    p50 = 26.6
    hill_coefficient = 2.7
    hbf_percentage = 10

    saturation, proxy = run_integrated_model(
        po2,
        p50,
        hill_coefficient,
        hbf_percentage
    )

    print("Integrated model demonstration")
    print("------------------------------")
    print(f"Oxygen partial pressure: {po2} mmHg")
    print(f"Calculated oxygen saturation: {saturation * 100:.2f}%")
    print(f"HbF input: {hbf_percentage}%")
    print(f"Illustrative polymerisation proxy: {proxy:.3f}")