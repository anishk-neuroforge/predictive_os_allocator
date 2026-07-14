import csv
import time
import psutil
import platform


def collect_metrics(interval=1, duration=60, output_file="dataset.csv"):
    """
    Collect detailed system metrics for ML training.
    """

    headers = [
        "timestamp",
        "cpu_percent",
        "memory_percent",
        "memory_available_mb",
        "swap_percent",
        "disk_percent",
        "disk_read_mb",
        "disk_write_mb",
        "network_sent_mb",
        "network_recv_mb",
        "process_count",
        "load_avg_1min",
        "load_avg_5min",
        "load_avg_15min",
    ]

    disk0 = psutil.disk_io_counters()
    net0 = psutil.net_io_counters()

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        start = time.time()

        while time.time() - start < duration:

            cpu = psutil.cpu_percent(interval=interval)

            memory = psutil.virtual_memory()

            swap = psutil.swap_memory()

            disk = psutil.disk_usage("/")

            disk_now = psutil.disk_io_counters()
            net_now = psutil.net_io_counters()

            process_count = len(psutil.pids())

            if platform.system() != "Windows":
                load1, load5, load15 = psutil.getloadavg()
            else:
                load1 = load5 = load15 = 0

            writer.writerow([
                int(time.time()),
                cpu,
                memory.percent,
                round(memory.available / (1024**2), 2),
                swap.percent,
                disk.percent,
                round((disk_now.read_bytes - disk0.read_bytes) / (1024**2), 2),
                round((disk_now.write_bytes - disk0.write_bytes) / (1024**2), 2),
                round((net_now.bytes_sent - net0.bytes_sent) / (1024**2), 2),
                round((net_now.bytes_recv - net0.bytes_recv) / (1024**2), 2),
                process_count,
                round(load1, 2),
                round(load5, 2),
                round(load15, 2),
            ])

            disk0 = disk_now
            net0 = net_now

            print(
                f"CPU:{cpu:5.1f}% | "
                f"RAM:{memory.percent:5.1f}% | "
                f"Disk:{disk.percent:5.1f}% | "
                f"Proc:{process_count}"
            )

    print(f"\nDataset saved to {output_file}")