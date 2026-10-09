import matplotlib.pyplot as plt
import numpy as np

from oxygen_binding import hill_saturation

# Illustrative parameters for testing
p50 = 26.6
hill_coefficient = 2.7

# Generate oxygen pressure values
pressures = np.linspace(0, 100, 200)

# Calculate fractional oxygen saturation
saturations = [
    hill_saturation(p, p50, hill_coefficient) * 100
    for p in pressures
]

# Plot the oxygen-binding curve
plt.figure(figsize=(8, 5))
plt.plot(pressures, saturations)

plt.xlabel("Oxygen partial pressure (mmHg)")
plt.ylabel("Oxygen saturation (%)")
plt.title("Illustrative Oxygen-Binding Curve")

plt.ylim(0, 100)
plt.xlim(0, 100)
plt.grid(True)

plt.tight_layout()
plt.savefig("oxygen_binding_curve.png", dpi=300)
plt.show()

print("Graph saved as oxygen_binding_curve.png")