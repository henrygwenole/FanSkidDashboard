# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
from utils import load_vibration_file, extract_features, load_model

st.set_page_config(page_title="Predictive Maintenance Dashboard", layout="wide")
st.title("🛠️ Predictive Maintenance Dashboard")

st.markdown("""
This dashboard analyzes vibration data from a belt-driven system to detect misalignment or wear.

Analysing the vibration data in the frequency domain provides critical insights that are not as easily observed in the time domain. By converting the data to the frequency domain using Fast Fourier Transform (FFT), we can identify specific frequency components associated with various mechanical behaviours and potential faults within the system.

When FFT is applied directly to the raw signal, a large spike may appear at 0 Hz — this is a **DC offset**. Since it doesn’t provide useful mechanical information, we remove it by subtracting the **mean of the signal** before computing the FFT.

#### 🔍 Key Frequency Components to Monitor:
- **Belt Frequency (fr):** Main belt frequency with harmonics at 2fr, 4fr, etc.
- **Drive Speed (n):** Pulley or motor rotation frequency and its harmonics.
- **Half Drive Speed (n/2):** Often reveals misalignment or load imbalance issues.
""")

uploaded_file = st.file_uploader("Upload vibration .txt file", type="txt")

if uploaded_file is not None:
    signal = load_vibration_file(uploaded_file)
    st.success("Custom file uploaded and loaded.")
else:
    try:
        with open("data/Data 70-F-0/1.txt", "r") as f:
            lines = f.readlines()
        signal = np.array([float(line.strip().split("\t")[-1]) for line in lines if line.strip()])
    except Exception as e:
        st.error("Failed to load default example file.")
        st.stop()

# Plot time-domain signal
st.subheader("Time Domain Signal")
st.line_chart(signal)

# Plot frequency-domain (FFT)
st.subheader("Frequency Domain (FFT)")
signal_detrended = signal - np.mean(signal)  # remove DC component
n = len(signal_detrended)
freq = np.fft.rfftfreq(n, d=1/10000)  # 10kHz sampling rate
fft_magnitude = np.abs(np.fft.rfft(signal_detrended))
fig, ax = plt.subplots()
ax.plot(freq, fft_magnitude)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude")
ax.set_title("FFT of Vibration Signal (DC removed)")
st.pyplot(fig)

# Feature extraction
features = extract_features(signal)

# Load model and predict only if model file exists
if os.path.exists("rf_model.pkl"):
    model = load_model()
    prediction = model.predict([features])[0]
    label = "✅ Healthy" if prediction == 0 else "⚠️ Fault Detected"

    st.subheader("Prediction")
    st.write(label)

    if prediction != 0:
        st.error("Maintenance Required! Possible misalignment or belt wear.")

st.markdown("""
### 👓 Launch AR Maintenance App
[Open on HoloLens](frn://s/6u615mm)
""", unsafe_allow_html=True)
