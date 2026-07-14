from predictor import predict_resources


def adjust_priority(features):
    """
    features must contain:

    [
        memory_percent,
        memory_available_mb,
        swap_percent,
        disk_percent,
        disk_read_mb,
        disk_write_mb,
        network_sent_mb,
        network_recv_mb,
        process_count,
        load_avg_1min,
        load_avg_5min,
        load_avg_15min
    ]
    """

    prediction = predict_resources(features)

    cpu = prediction["Predicted CPU"]
    memory = prediction["Predicted Memory"]
    disk = prediction["Predicted Disk"]

    if cpu > 80:
        priority = "High"
        action = "Increase CPU allocation"

    elif memory > 85:
        priority = "High"
        action = "Allocate more RAM"

    elif disk > 90:
        priority = "Medium"
        action = "Reduce Disk I/O"

    elif cpu > 50:
        priority = "Medium"
        action = "Normal scheduling"

    else:
        priority = "Low"
        action = "System Stable"

    print("\n========== AI Resource Allocation ==========")
    print(f"Predicted CPU Usage    : {cpu:.2f}%")
    print(f"Predicted Memory Usage : {memory:.2f}%")
    print(f"Predicted Disk Usage   : {disk:.2f}%")
    print(f"Priority               : {priority}")
    print(f"Decision               : {action}")
    print("===========================================\n")

    return {
        "priority": priority,
        "action": action,
        "prediction": prediction
    }


if __name__ == "__main__":

    sample_features = [
        45.0,      # memory_percent
        6100.0,    # memory_available_mb
        0.0,       # swap_percent
        55.0,      # disk_percent
        0.10,      # disk_read_mb
        0.02,      # disk_write_mb
        0.01,      # network_sent_mb
        0.03,      # network_recv_mb
        210,       # process_count
        1.10,      # load_avg_1min
        1.20,      # load_avg_5min
        1.30       # load_avg_15min
    ]

    adjust_priority(sample_features)