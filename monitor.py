import psutil
import time
import csv

def collect_metrics(interval=1, duration=60, output_file="dataset.csv"):
    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cpu_percent", "memory_percent"])

        start_time = time.time()
        while time.time() - start_time < duration:
            cpu = psutil.cpu_percent(interval=interval)
            mem = psutil.virtual_memory().percent
            writer.writerow([int(time.time()), cpu, mem])
            print(f"[Monitor] CPU: {cpu}%, Mem: {mem}%")