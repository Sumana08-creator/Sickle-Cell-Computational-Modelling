import csv

from model import calculate_polymerisation_proxy


def run_oxygen_experiment():
    """Test different oxygen inputs while keeping HbF constant."""

    results = []

    hbf = 10

    for oxygen in [100, 75, 50, 25, 0]:
        score = calculate_polymerisation_proxy(oxygen, hbf)

        results.append({
            "experiment": "oxygen",
            "oxygen_saturation_percent": oxygen,
            "hbf_percentage": hbf,
            "illustrative_score": score
        })

    return results


def run_hbf_experiment():
    """Test different HbF inputs while keeping oxygen constant."""

    results = []

    oxygen = 50

    for hbf in [0, 10, 20, 30, 50]:
        score = calculate_polymerisation_proxy(oxygen, hbf)

        results.append({
            "experiment": "hbf",
            "oxygen_saturation_percent": oxygen,
            "hbf_percentage": hbf,
            "illustrative_score": score
        })

    return results


if __name__ == "__main__":

    results = run_oxygen_experiment() + run_hbf_experiment()

    with open("experiment_results.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())

        writer.writeheader()
        writer.writerows(results)

    print("Experiments completed successfully.")
    print("Number of experiment results:", len(results))
    print("Results saved to experiment_results.csv")
import matplotlib.pyplot as plt

oxygen_values = [100, 75, 50, 25, 0]
hbf = 10

scores = [
    calculate_polymerisation_proxy(oxygen, hbf)
    for oxygen in oxygen_values
]

plt.plot(oxygen_values, scores, marker="o")
plt.xlabel("Oxygen saturation (%)")
plt.ylabel("Illustrative score")
plt.title("Oxygen Saturation vs Illustrative Score")
plt.grid(True)
plt.savefig("oxygen_experiment.png", dpi=300, bbox_inches="tight")
plt.show()
# HbF experiment graph
hbf_values = [0, 10, 20, 30, 50]
oxygen = 50

hbf_scores = [
    calculate_polymerisation_proxy(oxygen, hbf)
    for hbf in hbf_values
]

plt.figure()
plt.plot(hbf_values, hbf_scores, marker="o")
plt.xlabel("Fetal haemoglobin (HbF) percentage")
plt.ylabel("Illustrative score")
plt.title("HbF Percentage vs Illustrative Score")
plt.grid(True)
plt.savefig("hbf_experiment.png", dpi=300, bbox_inches="tight")
plt.show()