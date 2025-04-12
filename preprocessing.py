# preprocessing.py
import numpy as np
from scipy.stats import skew, kurtosis


def extract_features_from_signal(signal):
    # Basic time-domain features
    rms = np.sqrt(np.mean(signal**2))
    peak = np.max(np.abs(signal))
    crest_factor = peak / rms if rms != 0 else 0
    skewness = skew(signal)
    kurt = kurtosis(signal)

    # Frequency-domain features
    fft_vals = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(len(signal), d=1/10000)  # assuming 10kHz sample rate
    dominant_freq = freqs[np.argmax(fft_vals)]

    return [rms, peak, crest_factor, skewness, kurt, dominant_freq]
