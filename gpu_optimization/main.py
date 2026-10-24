
# main.py

import os
import pandas as pd

from data import gpu_data, workload_data
from optimizer import run_optimization
from results import generate_results


def main():

    # STEP 1: Create output directory
    os.makedirs("outputs", exist_ok=True)

    # STEP 2: Run the optimization model
    gpu_results, allocation_results, optimized_cost = (
        run_optimization()
    )

    # STEP 3: Convert results into DataFrames
    gpu_df = pd.DataFrame(gpu_results)
    allocation_df = pd.DataFrame(allocation_results)

    # STEP 4: Save the optimization results
    gpu_df.to_csv(
        "outputs/gpu_provisioning.csv",
        index=False
    )

    allocation_df.to_csv(
        "outputs/workload_allocation.csv",
        index=False
    )

    # STEP 5: Display GPU provisioning
    print("\n===== OPTIMAL GPU PROVISIONING =====")
    print(gpu_df.to_string(index=False))

    # STEP 6: Display non-zero workload allocations
    print("\n===== WORKLOAD ALLOCATION =====")

    used_allocations = allocation_df[
        allocation_df["Allocated Units"] > 0
    ]

    print(used_allocations.to_string(index=False))

    # STEP 7: Calculate demand and provisioned capacity
    total_demand = sum(
        details["demand"]
        for details in workload_data.values()
    )

    total_capacity = sum(
        row["Quantity"]
        * gpu_data[row["GPU"]]["capacity"]
        for row in gpu_results
    )

    # STEP 8: Display optimization summary
    print("\n===== OPTIMIZATION SUMMARY =====")
    print(f"Minimum Hourly Cost: Rs. {optimized_cost:.2f}")
    print(f"Total Workload Demand: {total_demand}")
    print(f"Total Provisioned Capacity: {total_capacity}")

    # STEP 9: Generate graphs and compare costs
    generate_results(
        gpu_df,
        allocation_df,
        optimized_cost
    )

    # STEP 10: Confirm CSV outputs
    print("\n===== SAVED CSV FILES =====")
    print("- outputs/gpu_provisioning.csv")
    print("- outputs/workload_allocation.csv")


if __name__ == "__main__":
    main()
