import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class ResourcePredictor:
    def __init__(self):
        self.model = RandomForestRegressor()

    def train(self, csv_file="dataset.csv"):
        data = pd.read_csv(csv_file)
        data['next_cpu'] = data['cpu_percent'].shift(-1)
        data = data.dropna()

        X = data[['cpu_percent', 'memory_percent']]
        y = data['next_cpu']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(self.X_train, self.y_train)
        print("[Predictor] Model trained.")

    def predict(self, current_cpu, current_mem):
        input_data = [[current_cpu, current_mem]]
        prediction = self.model.predict(input_data)[0]
        return round(prediction, 2)
