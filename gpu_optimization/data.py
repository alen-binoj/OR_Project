
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

workload_data = {
    "Chatbot": {
        "demand": 300,
        "min_vram": 8
    },
    "Summarization": {
        "demand": 200,
        "min_vram": 16
    },
    "Code_Auditing": {
        "demand": 150,
        "min_vram": 24
    }
}
