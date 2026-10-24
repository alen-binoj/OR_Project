
# results.py

import os
import math
import matplotlib.pyplot as plt
import pandas as pd

from data import gpu_data, workload_data


def generate_results(
    gpu_df,
    allocation_df,
    optimized_cost
):
    os.makedirs("outputs", exist_ok=True)

    # STEP 1: Plot GPU provisioning
    plt.figure(figsize=(8, 5))

    plt.bar(
        gpu_df["GPU"],
        gpu_df["Quantity"]
    )

    plt.title("Optimal GPU Provisioning")
    plt.xlabel("GPU Type")
    plt.ylabel("Number of GPUs")
    plt.tight_layout()

    plt.savefig(
        "outputs/gpu_provisioning.png",
        dpi=300
    )
    plt.close()

    # STEP 2: Plot workload allocation
    allocation_pivot = allocation_df.pivot(
        index="Workload",
        columns="GPU",
        values="Allocated Units"
    ).fillna(0)

    allocation_pivot = allocation_pivot.reindex(
        columns=list(gpu_data.keys()),
        fill_value=0
    )

    allocation_pivot.plot(
        kind="bar",
        stacked=True,
        figsize=(9, 5)
    )

    plt.title("Workload Allocation by GPU Type")
    plt.xlabel("Workload")
    plt.ylabel("Allocated Workload Units")
    plt.xticks(rotation=15)
    plt.legend(title="GPU Type")
    plt.tight_layout()

    plt.savefig(
        "outputs/workload_allocation.png",
        dpi=300
    )
    plt.close()

    # STEP 3: Calculate the A100-only baseline
    total_demand = sum(
        details["demand"]
        for details in workload_data.values()
    )

    a100_capacity = gpu_data["A100"]["capacity"]
    a100_cost = gpu_data["A100"]["cost_per_hour"]

    # Round up because GPUs are provisioned as whole units
    baseline_gpu_count = math.ceil(
        total_demand / a100_capacity
    )

    baseline_cost = baseline_gpu_count * a100_cost

    savings = baseline_cost - optimized_cost

    savings_percentage = (
        (savings / baseline_cost) * 100
        if baseline_cost > 0
        else 0
    )

    # STEP 4: Save the cost comparison
    comparison_df = pd.DataFrame([
        {
            "Configuration": "Optimized",
            "A100 GPUs Required": None,
            "Hourly Cost": round(optimized_cost, 2)
        },
        {
            "Configuration": "A100 Only",
            "A100 GPUs Required": baseline_gpu_count,
            "Hourly Cost": baseline_cost
        }
    ])

    comparison_df.to_csv(
        "outputs/cost_comparison.csv",
        index=False
    )

    # STEP 5: Plot the cost comparison
    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        comparison_df["Configuration"],
        comparison_df["Hourly Cost"]
    )

    plt.title("Optimized Cost vs A100-Only Baseline")
    plt.xlabel("Configuration")
    plt.ylabel("Hourly Cost (Rs.)")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"Rs. {height:.0f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    plt.savefig(
        "outputs/cost_comparison.png",
        dpi=300
    )
    plt.close()

    # STEP 6: Print the comparison summary
    print("\n===== COST COMPARISON =====")
    print(f"Optimized hourly cost: Rs. {optimized_cost:.2f}")
    print(f"A100-only hourly cost: Rs. {baseline_cost:.2f}")
    print(f"Hourly savings: Rs. {savings:.2f}")
    print(f"Percentage savings: {savings_percentage:.2f}%")

    print("\n===== GENERATED GRAPHS =====")
    print("- outputs/gpu_provisioning.png")
    print("- outputs/workload_allocation.png")
    print("- outputs/cost_comparison.png")
    print("- outputs/cost_comparison.csv")
