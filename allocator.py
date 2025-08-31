def adjust_priority(cpu_prediction):
    if cpu_prediction > 80:
        priority = "High"
    elif cpu_prediction > 50:
        priority = "Medium"
    else:
        priority = "Low"

    print(f"[Allocator] Predicted CPU: {cpu_prediction}%, Priority set to: {priority}")
    return priority