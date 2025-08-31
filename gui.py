import tkinter as tk
import psutil
from predictor import ResourcePredictor
from allocator import adjust_priority

class ResourceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Predictive OS Resource Dashboard")
        self.root.geometry("400x250")
        self.predictor = ResourcePredictor()
        self.predictor.train()

        self.cpu_label = tk.Label(root, text="CPU Usage: ", font=("Arial", 14))
        self.cpu_label.pack(pady=10)

        self.mem_label = tk.Label(root, text="Memory Usage: ", font=("Arial", 14))
        self.mem_label.pack(pady=10)

        self.pred_label = tk.Label(root, text="Predicted CPU: ", font=("Arial", 14))
        self.pred_label.pack(pady=10)

        self.priority_label = tk.Label(root, text="Priority: ", font=("Arial", 14))
        self.priority_label.pack(pady=10)

        self.update_stats()

    def update_stats(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        pred = self.predictor.predict(cpu, mem)
        priority = adjust_priority(pred)

        self.cpu_label.config(text=f"CPU Usage: {cpu}%")
        self.mem_label.config(text=f"Memory Usage: {mem}%")
        self.pred_label.config(text=f"Predicted CPU: {pred}%")
        self.priority_label.config(text=f"Priority: {priority}")

        self.root.after(3000, self.update_stats)