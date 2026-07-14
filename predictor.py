import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, r2_score


DATASET = "dataset.csv"
MODEL_FILE = "resource_predictor.pkl"


def train_model():

    df = pd.read_csv(DATASET)

    feature_columns = [
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
        "load_avg_15min"
    ]

    target_columns = [
        "cpu_percent",
        "memory_percent",
        "disk_percent"
    ]

    X = df[feature_columns]
    y = df[target_columns]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=200,
            random_state=42
        )
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nModel Evaluation")

    for i, target in enumerate(target_columns):

        mae = mean_absolute_error(y_test.iloc[:, i], predictions[:, i])

        r2 = r2_score(y_test.iloc[:, i], predictions[:, i])

        print(f"{target}")
        print(f" MAE : {mae:.2f}")
        print(f" R²  : {r2:.3f}")
        print()

    joblib.dump(model, MODEL_FILE)

    print(f"Model saved as {MODEL_FILE}")


def load_model():

    return joblib.load(MODEL_FILE)


def predict_resources(input_data):

    model = load_model()

    prediction = model.predict([input_data])[0]

    return {
        "Predicted CPU": round(prediction[0], 2),
        "Predicted Memory": round(prediction[1], 2),
        "Predicted Disk": round(prediction[2], 2)
    }


if __name__ == "__main__":

    train_model()