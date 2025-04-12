# model_training.py
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from preprocessing import extract_features_from_signal


def load_dataset(data_dir):
    data = []
    labels = []

    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        if "H-0" in folder:
            label = 0  # Healthy
        else:
            label = 1  # Faulty or Unbalanced (treated as fault)

        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'r') as f:
                    signal = np.array([float(line.strip()) for line in f])
                features = extract_features_from_signal(signal)
                data.append(features)
                labels.append(label)

    return np.array(data), np.array(labels)


if __name__ == "__main__":
    X, y = load_dataset("data")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    import joblib
    joblib.dump(model, "rf_model.pkl")
