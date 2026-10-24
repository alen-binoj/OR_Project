
import pandas as pd
import matplotlib.pyplot as plt

# Read actual optimization results
gpu_df = pd.read_csv("gpu_provisioning.csv")

optimized_cost = gpu_df["Total Cost"].sum()

# Baseline: use A100 GPUs for all workloads
total_demand = 300 + 200 + 150

a100_capacity = 600
a100_cost = 120

baseline_gpu_count = -(-total_demand // a100_capacity)
baseline_cost = baseline_gpu_count * a100_cost

# Calculate savings
savings = baseline_cost - optimized_cost
savings_percent = (savings / baseline_cost) * 100

# Display comparison
comparison = pd.DataFrame({
    "Configuration": ["All-A100 Baseline", "Optimized"],
    "Hourly Cost (Rs.)": [baseline_cost, optimized_cost]
})

print("\nCost Comparison")
print(comparison.to_string(index=False))

print(f"\nHourly Savings: Rs. {savings:.2f}")
print(f"Cost Reduction: {savings_percent:.2f}%")

# Plot comparison
plt.figure(figsize=(8, 5))

plt.bar(
    comparison["Configuration"],
    comparison["Hourly Cost (Rs.)"]
)

plt.title("Baseline vs Optimized GPU Cost")
plt.xlabel("Configuration")
plt.ylabel("Hourly Cost (Rs.)")

plt.tight_layout()
plt.savefig("cost_comparison.png")
plt.show()
