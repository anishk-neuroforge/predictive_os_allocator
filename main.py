from monitor import collect_metrics
from gui import ResourceGUI
import tkinter as tk
import threading

def start_gui():
    root = tk.Tk()
    app = ResourceGUI(root)
    root.mainloop()

def main():
    print("Collecting real-time system metrics...")
    collect_metrics(interval=1, duration=30)

    print("Launching Predictive Dashboard...")
    t = threading.Thread(target=start_gui)
    t.start()

if __name__ == "__main__":
    main()
