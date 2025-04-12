# utils.py
import numpy as np
import joblib
from preprocessing import extract_features_from_signal


def load_vibration_file(file):
    """Reads a .txt vibration file and returns a numpy array."""
    content = file.read().decode("utf-8").splitlines()
    return np.array([float(line.strip()) for line in content if line.strip()])


def extract_features(signal):
    """Wrapper for preprocessing."""
    return extract_features_from_signal(signal)


def load_model(path="rf_model.pkl"):
    """Loads the trained model."""
    return joblib.load(path)
