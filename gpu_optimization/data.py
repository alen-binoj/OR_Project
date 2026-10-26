
# data.py

# GPU specifications
# cost_per_hour: hourly cost in rupees
# vram: GPU memory in GB
# capacity: workload units supported per GPU

gpu_data = {
    "T4": {
        "cost_per_hour": 20,
        "vram": 16,
        "capacity": 100
    },
    "A10G": {
        "cost_per_hour": 50,
        "vram": 24,
        "capacity": 250
    },
    "A100": {
        "cost_per_hour": 120,
        "vram": 40,
        "capacity": 600
    }
}


# AI inference workload requirements
# demand: required workload units
# min_vram: minimum GPU memory required in GB
# latency_deadline_ms: maximum acceptable estimated latency

workload_data = {
    "Chatbot": {
        "demand": 300,
        "min_vram": 8,
        "latency_deadline_ms": 2000
    },
    "Summarization": {
        "demand": 200,
        "min_vram": 16,
        "latency_deadline_ms": 2500
    },
    "Code_Auditing": {
        "demand": 150,
        "min_vram": 24,
        "latency_deadline_ms": 4000
    }
}


# Illustrative estimated latency in milliseconds.
# These values are assumptions for the project, not
# verified measurements of real GPU performance.

latency_estimates_ms = {
    "Chatbot": {
        "T4": 1800,
        "A10G": 1200,
        "A100": 800
    },
    "Summarization": {
        "T4": 4500,
        "A10G": 3000,
        "A100": 1800
    },
    "Code_Auditing": {
        "T4": 6000,
        "A10G": 4500,
        "A100": 2500
    }
}
