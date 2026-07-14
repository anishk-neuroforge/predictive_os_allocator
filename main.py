import os
import customtkinter as ctk

from monitor import collect_metrics
from predictor import train_model
from gui import ResourceGUI

DATASET_FILE = "dataset.csv"
MODEL_FILE = "resource_predictor.pkl"


def setup_ai():
    """
    Prepare dataset and ML model automatically.
    """

    if not os.path.exists(DATASET_FILE):
        print("=" * 60)
        print("Dataset not found.")
        print("Collecting system metrics...")
        print("=" * 60)

        collect_metrics(
            interval=1,
            duration=60,
            output_file=DATASET_FILE
        )

    else:
        print("Dataset found.")

    if (
        not os.path.exists(MODEL_FILE)
        or os.path.getmtime(DATASET_FILE) > os.path.getmtime(MODEL_FILE)
    ):

        print("=" * 60)
        print("Training AI Resource Prediction Model...")
        print("=" * 60)

        train_model()

    else:
        print("AI model found.")


def main():

    setup_ai()

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    ResourceGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()