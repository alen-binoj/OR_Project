
# optimizer.py

import pulp
from data import gpu_data, workload_data


def run_optimization():

    # STEP 1: Define the minimization problem
    model = pulp.LpProblem(
        "GPU_Cost_Optimization",
        pulp.LpMinimize
    )

    # STEP 2: Decision variables

    # Number of GPUs of each type to provision
    x = {
        g: pulp.LpVariable(
            f"GPU_{g}",
            lowBound=0,
            cat="Integer"
        )
        for g in gpu_data
    }

    # Workload units assigned to each GPU type
    y = {
        (w, g): pulp.LpVariable(
            f"Allocation_{w}_{g}",
            lowBound=0,
            cat="Continuous"
        )
        for w in workload_data
        for g in gpu_data
    }

    # STEP 3: Objective function
    # Minimize total hourly GPU cost
    model += pulp.lpSum(
        gpu_data[g]["cost_per_hour"] * x[g]
        for g in gpu_data
    ), "Total_GPU_Cost"

    # STEP 4: Demand constraints
    # Each workload's entire demand must be allocated
    for w in workload_data:
        model += (
            pulp.lpSum(y[w, g] for g in gpu_data)
            == workload_data[w]["demand"]
        ), f"Demand_{w}"

    # STEP 5: GPU capacity constraints
    # Allocated workload cannot exceed provisioned capacity
    for g in gpu_data:
        model += (
            pulp.lpSum(y[w, g] for w in workload_data)
            <= gpu_data[g]["capacity"] * x[g]
        ), f"Capacity_{g}"

    # STEP 6: VRAM compatibility constraints
    # Incompatible GPU types cannot receive that workload
    for w in workload_data:
        for g in gpu_data:
            if (
                gpu_data[g]["vram"]
                < workload_data[w]["min_vram"]
            ):
                model += (
                    y[w, g] == 0
                ), f"VRAM_{w}_{g}"

    # STEP 7: Solve using HiGHS
    solver = pulp.HiGHS(msg=False)
    model.solve(solver)

    status = pulp.LpStatus[model.status]
    print(f"\nSolver Status: {status}")

    if status != "Optimal":
        raise RuntimeError(
            f"Optimization failed. Solver status: {status}"
        )

    # STEP 8: Collect GPU provisioning results
    gpu_results = []

    for g in gpu_data:
        quantity = int(round(pulp.value(x[g])))

        gpu_results.append({
            "GPU": g,
            "Quantity": quantity,
            "Cost per Hour": gpu_data[g]["cost_per_hour"],
            "Total Cost": (
                quantity * gpu_data[g]["cost_per_hour"]
            )
        })

    # STEP 9: Collect workload allocation results
    allocation_results = []

    for w in workload_data:
        for g in gpu_data:
            amount = pulp.value(y[w, g])

            allocation_results.append({
                "Workload": w,
                "GPU": g,
                "Allocated Units": round(amount or 0, 2)
            })

    # STEP 10: Get the optimized objective value
    optimized_cost = pulp.value(model.objective)

    return gpu_results, allocation_results, optimized_cost
