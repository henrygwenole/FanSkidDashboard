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
n = len(signal)
freq = np.fft.rfftfreq(n, d=1/10000)  # 10kHz sampling rate
fft_magnitude = np.abs(np.fft.rfft(signal))
fig, ax = plt.subplots()
ax.plot(freq, fft_magnitude)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude")
ax.set_title("FFT of Vibration Signal")
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
else:
    st.warning("Model file 'rf_model.pkl' not found. Prediction skipped.")

st.markdown("""
### 👓 Launch AR Maintenance App
[Open on HoloLens](frn://s/6u615mm)
""", unsafe_allow_html=True)