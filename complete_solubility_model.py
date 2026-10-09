"""
HbS Solubility Computational Model
Reference: Henry et al. (2020), PNAS.

Compares three fibre oxygen-binding assumptions:
1. Measured noncooperative fibre binding
2. MWC fibre-binding assumption
3. TTS fibre-binding model

IMPORTANT:
The initial reference solubility is provisional.
Model predictions must be compared with experimental data
before scientific validation can be claimed.
"""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


# =========================================================
# 1. PARAMETERS
# =========================================================

# Free haemoglobin: MWC model
L = 60500.0
K_T = 0.016
K_R = 1.47

# Measured noncooperative fibre binding
K_P = 0.0059

# TTS fibre-binding parameters from Henry et al. (2020)
K_t = 0.0036
K_r = 3.7
l_T = 840.0

# Concentration and activity parameters
POLYMER_CONCENTRATION = 0.69       # g/mL
PARTIAL_SPECIFIC_VOLUME = 0.76     # mL/g
HARD_SPHERE_VOLUME = 0.79          # mL/g

# PROVISIONAL: not yet verified against the original data
REFERENCE_SOLUBILITY = 0.178375    # g/mL

MAXIMUM_PRESSURE = 100.0           # torr
NUMBER_OF_POINTS = 501

CONCENTRATION_LIMIT = (
    POLYMER_CONCENTRATION * (1.0 - 1e-5)
)

OUTPUT_DIR = Path(__file__).resolve().parent

CSV_PATH = OUTPUT_DIR / "solubility_model_comparison.csv"
GRAPH_PATH = OUTPUT_DIR / "solubility_model_comparison.png"


# =========================================================
# 2. FREE HAEMOGLOBIN OXYGEN SATURATION
# =========================================================

def free_saturation(pressure):
    """
    MWC oxygen saturation of free haemoglobin.

    Parameters:
        pressure: Oxygen pressure in torr.

    Returns:
        Fractional oxygen saturation.
    """

    p = np.asarray(pressure, dtype=float)

    t = 1.0 + K_T * p
    r = 1.0 + K_R * p

    numerator = (
        L * K_T * p * t**3
        + K_R * p * r**3
    )

    denominator = (
        L * t**4
        + r**4
    )

    result = numerator / denominator

    return float(result) if result.ndim == 0 else result


# =========================================================
# 3. FIBRE OXYGEN-SATURATION MODELS
# =========================================================

def measured_fibre_saturation(pressure):
    """
    Noncooperative fibre-binding curve.

    Henry et al. (2020):
        K_P = 0.0059 torr^-1
    """

    p = np.asarray(pressure, dtype=float)

    result = K_P * p / (1.0 + K_P * p)

    return float(result) if result.ndim == 0 else result


def mwc_fibre_saturation(pressure):
    """
    MWC comparison: fibre binding assumed to have
    the same oxygen affinity as the free T state.

    Henry et al. (2020):
        K_T = 0.016 torr^-1
    """

    p = np.asarray(pressure, dtype=float)

    result = K_T * p / (1.0 + K_T * p)

    return float(result) if result.ndim == 0 else result


def tts_fibre_saturation(pressure):
    """
    TTS fibre saturation from Henry et al. (2020), Eq. 6.
    """

    p = np.asarray(pressure, dtype=float)

    effective_K = (
        l_T * K_t + K_r
    ) / (1.0 + l_T)

    result = (
        effective_K * p
        / (1.0 + effective_K * p)
    )

    return float(result) if result.ndim == 0 else result
# =========================================================
# 4. ACTIVITY-COEFFICIENT DERIVATIVE
# =========================================================

def log_activity_derivative(concentration):
    """
    Calculate d[ln(gamma*c)]/dc.

    Derived from the hard-sphere activity-coefficient
    polynomial used in the solubility equation.
    """

    c = float(concentration)

    if c <= 0:
        raise ValueError(
            "Concentration must be positive."
        )

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
# 5. WATER-VOLUME RATIO
# =========================================================

def water_volume_ratio(concentration):
    """
    Calculate the concentration-dependent volume ratio
    appearing in the differential solubility equation.
    """

    numerator = (
        1.0 / POLYMER_CONCENTRATION
        - PARTIAL_SPECIFIC_VOLUME
    )

    denominator = (
        1.0 / concentration
        - PARTIAL_SPECIFIC_VOLUME
    )

    if abs(denominator) < 1e-12:
        raise FloatingPointError(
            "Water-volume denominator approaches zero."
        )

    return numerator / denominator


# =========================================================
# 6. SOLUBILITY DIFFERENTIAL EQUATION
# =========================================================

def make_solubility_ode(fibre_saturation_function):
    """
    Create the differential equation for a selected
    fibre oxygen-saturation model.

    Equation:
        d ln(gamma*c) / dp
        = 4*(ys - yp) / [p*(1 - volume_ratio)]

    where:
        ys = free haemoglobin saturation
        yp = fibre saturation

    The concentration derivative is obtained by dividing
    by d ln(gamma*c)/dc.
    """

    def solubility_ode(pressure, state):

        concentration = float(state[0])

        if not np.isfinite(concentration):
            raise FloatingPointError(
                "Concentration became non-finite."
            )

        # Keep intermediate solver evaluations away
        # from the singular polymer-concentration boundary.
        concentration = float(
            np.clip(
                concentration,
                1e-10,
                CONCENTRATION_LIMIT,
            )
        )

        volume_ratio = water_volume_ratio(
            concentration
        )

        denominator = 1.0 - volume_ratio

        if abs(denominator) < 1e-12:
            raise FloatingPointError(
                "Equation denominator approaches zero."
            )

        if pressure < 1e-7:

            # Analytical pressure-zero limit:
            # lim(p->0) [ys(p)-yp(p)]/p
            #
            # Free MWC saturation slope at zero:
            # (L*K_T + K_R)/(L+1)
            #
            # Fibre saturation slope depends on the model.
            if fibre_saturation_function is measured_fibre_saturation:
                fibre_slope = K_P

            elif fibre_saturation_function is mwc_fibre_saturation:
                fibre_slope = K_T

            elif fibre_saturation_function is tts_fibre_saturation:
                fibre_slope = (
                    l_T * K_t + K_r
                ) / (l_T + 1.0)

            else:
                raise ValueError(
                    "Unknown fibre saturation function."
                )

            saturation_difference_per_pressure = (
                (L * K_T + K_R) / (L + 1.0)
                - fibre_slope
            )

        else:

            ys = free_saturation(pressure)

            yp = fibre_saturation_function(
                pressure
            )

            saturation_difference_per_pressure = (
                (ys - yp) / pressure
            )

        derivative = (
            4.0
            * saturation_difference_per_pressure
            / (
                denominator
                * log_activity_derivative(
                    concentration
                )
            )
        )

        return [derivative]

    return solubility_ode


# =========================================================
# 7. CONCENTRATION-LIMIT EVENT
# =========================================================

def concentration_limit_event(pressure, state):
    """
    Stop integration before the concentration reaches
    the near-singular polymer-concentration boundary.
    """

    return (
        CONCENTRATION_LIMIT
        - float(state[0])
    )


concentration_limit_event.terminal = True
concentration_limit_event.direction = -1


# =========================================================
# 8. SOLVE ONE MODEL
# =========================================================

def calculate_one_model(
    fibre_saturation_function,
    maximum_pressure=MAXIMUM_PRESSURE,
    number_of_points=NUMBER_OF_POINTS,
):
    """
    Calculate one solubility curve.

    Returns:
        pressures
        concentrations
        status
    """

    if maximum_pressure <= 0:
        raise ValueError(
            "Maximum pressure must be positive."
        )

    if number_of_points < 2:
        raise ValueError(
            "At least two output points are required."
        )

    if not (
        0 < REFERENCE_SOLUBILITY
        < POLYMER_CONCENTRATION
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

    ode = make_solubility_ode(
        fibre_saturation_function
    )

    solution = solve_ivp(
        fun=ode,
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
            "Numerical solver failed: "
            + solution.message
        )

    if solution.t.size == 0:
        raise RuntimeError(
            "The solver returned no usable results."
        )

    reached_limit = bool(
        solution.t_events[0].size
    )

    if reached_limit:
        status = (
            "PARTIAL: concentration boundary reached."
        )

    elif solution.t[-1] < maximum_pressure - 1e-8:
        status = (
            "PARTIAL: integration stopped early."
        )

    else:
        status = (
            "COMPLETED: numerical integration finished; "
            "experimental validation is still required."
        )

    return (
        solution.t,
        solution.y[0],
        status,
    )


# =========================================================
# 9. CALCULATE ALL THREE CURVES
# =========================================================

def calculate_all_models():
    """
    Calculate the three fibre-binding model predictions.
    """

    models = {
        "Measured fibre binding (Kp=0.0059)":
            measured_fibre_saturation,

        "MWC fibre binding (KT=0.016)":
            mwc_fibre_saturation,

        "TTS fibre binding (lT=840)":
            tts_fibre_saturation,
    }

    results = {}

    for model_name, saturation_function in models.items():

        print()
        print("Calculating:", model_name)

        pressures, concentrations, status = (
            calculate_one_model(
                saturation_function
            )
        )

        results[model_name] = {
            "pressures": pressures,
            "concentrations": concentrations,
            "status": status,
        }

        print("Status:", status)
        print(
            "Last pressure:",
            f"{pressures[-1]:.3f} torr",
        )
        print(
            "Last solubility:",
            f"{concentrations[-1]:.6f} g/mL",
        )

    return results


# =========================================================
# 10. EXPORT COMPARISON CSV
# =========================================================

def save_comparison_csv(results):
    """
    Export calculated model predictions.

    These are model predictions, not measured data.
    """

    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "model",
            "oxygen_pressure_torr",
            "free_hbs_saturation_fraction",
            "fibre_saturation_fraction",
            "calculated_solubility_g_per_ml",
            "calculated_solubility_mg_per_ml",
            "reference_concentration_g_per_ml",
            "reference_status",
            "calculation_status",
        ])

        for model_name, result in results.items():

            pressures = result["pressures"]
            concentrations = result["concentrations"]

            saturation_function = {
                "Measured fibre binding (Kp=0.0059)":
                    measured_fibre_saturation,

                "MWC fibre binding (KT=0.016)":
                    mwc_fibre_saturation,

                "TTS fibre binding (lT=840)":
                    tts_fibre_saturation,
            }[model_name]

            for pressure, concentration in zip(
                pressures,
                concentrations,
            ):

                writer.writerow([
                    model_name,
                    f"{pressure:.6f}",
                    f"{free_saturation(pressure):.8f}",
                    f"{saturation_function(pressure):.8f}",
                    f"{concentration:.8f}",
                    f"{concentration * 1000.0:.4f}",
                    f"{REFERENCE_SOLUBILITY:.6f}",
                    "PROVISIONAL",
                    result["status"],
                ])


# =========================================================
# 11. CREATE GRAPH
# =========================================================

def save_comparison_graph(results):
    """
    Plot model predictions against free haemoglobin
    fractional oxygen saturation, as in Figure 3.

    The curves are predictions, not experimental data.
    """

    fig, ax = plt.subplots(figsize=(10, 7))

    for model_name, result in results.items():

        pressures = result["pressures"]
        concentrations = result["concentrations"]

        x_values = free_saturation(pressures)

        ax.plot(
            x_values,
            concentrations * 1000.0,
            label=model_name,
            linewidth=2,
        )

    ax.set_title(
        "HbS Solubility vs Fractional Oxygen Saturation"
    )

    ax.set_xlabel(
        "Free haemoglobin fractional oxygen saturation"
    )

    ax.set_ylabel(
        "Calculated solubility (mg/mL)"
    )

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


# =========================================================
# 12. MAIN PROGRAM
# =========================================================

def main():

    print("=" * 65)
    print("HbS SOLUBILITY MODEL COMPARISON")
    print("=" * 65)

    print("Reference: Henry et al. (2020), PNAS")
    print(
        "Initial solubility:",
        f"{REFERENCE_SOLUBILITY:.6f} g/mL",
    )
    print("Initial solubility status: PROVISIONAL")
    print(
        "Maximum pressure:",
        f"{MAXIMUM_PRESSURE:.1f} torr",
    )
    print(
        "Output points per model:",
        NUMBER_OF_POINTS,
    )

    try:

        results = calculate_all_models()

        save_comparison_csv(results)

        save_comparison_graph(results)

    except (
        ValueError,
        RuntimeError,
        FloatingPointError,
    ) as error:

        print()
        print("CALCULATION FAILED")
        print("Reason:", error)
        print(
            "Do not interpret incomplete output "
            "as a validated scientific result."
        )
        return

    print()
    print("=" * 65)
    print("OUTPUT FILES")
    print("=" * 65)

    print("CSV:", CSV_PATH)
    print("Graph:", GRAPH_PATH)

    print()
    print("IMPORTANT:")
    print(
        "All curves are model predictions. "
        "The initial concentration remains provisional."
    )
    print(
        "No experimental error metric has been calculated "
        "because verified numerical measurement data "
        "have not yet been supplied."
    )


if __name__ == "__main__":
    main()