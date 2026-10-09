import matplotlib.pyplot as plt
import numpy as np

from mwc_binding import mwc_saturation
from fiber_binding import fiber_saturation

# Parameters used in our existing model files
L = 60500
K_T = 0.016
K_R = 1.47
k_p = 0.0059

# Generate oxygen pressure values
pressures = np.linspace(0, 100, 200)

# Calculate oxygen saturation for both models
free_hb_saturation = [
    mwc_saturation(p, L, K_T, K_R) * 100
    for p in pressures
]

fibre_saturation = [
    fiber_saturation(p, k_p) * 100
    for p in pressures
]

# Plot the comparison
plt.figure(figsize=(9, 6))

plt.plot(
    pressures,
    free_hb_saturation,
    label="Free haemoglobin (MWC model)"
)

plt.plot(
    pressures,
    fibre_saturation,
    label="Haemoglobin fibres"
)

plt.xlabel("Oxygen partial pressure (torr)")
plt.ylabel("Calculated oxygen saturation (%)")
plt.title("Comparison of Oxygen-Binding Models")

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("binding_comparison.png", dpi=300)
plt.show()

print("Comparison graph saved as binding_comparison.png")