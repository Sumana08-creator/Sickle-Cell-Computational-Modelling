print("Sickle Cell Computational Modelling")
print("------------------------------------")

# Illustrative values for learning Python
oxygen_levels = [20, 40, 60, 80, 100]

# Calculate the average
average_oxygen = sum(oxygen_levels) / len(oxygen_levels)

print("Demonstration values:", oxygen_levels)
print("Average demonstration value:", average_oxygen)
print("Smallest demonstration value:", min(oxygen_levels))
print("Largest demonstration value:", max(oxygen_levels))
print("------------------------------------")

for oxygen in oxygen_levels:
    if oxygen < 40:
        category = "Low demonstration value"
    elif oxygen < 80:
        category = "Moderate demonstration value"
    else:
        category = "High demonstration value"

    print(oxygen, "->", category)
import matplotlib.pyplot as plt

# Plot our illustrative demonstration values
sample_numbers = [1, 2, 3, 4, 5]

plt.plot(sample_numbers, oxygen_levels, marker="o")

plt.title("Illustrative Demonstration Values")
plt.xlabel("Sample Number")
plt.ylabel("Demonstration Value")

plt.grid(True)
plt.savefig("demonstration_graph.png", dpi=300)
plt.show()