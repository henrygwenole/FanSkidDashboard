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

🧠 **Note**: The dataset contains 10,000 samples collected over 100 seconds, giving a sampling rate of **100 Hz**. However, if you're seeing valid content up to 5,000 Hz, then the true sampling rate is **10,000 Hz**. This has now been correctly reflected in the frequency axis.
""")

uploaded_file = st.file_uploader("Upload vibration .txt file", type="txt")

if uploaded_file is not None:
    data = np.loadtxt(uploaded_file, delimiter="\t", usecols=(1, 2))
    st.success("Custom file uploaded and loaded.")
else:
    try:
        data = np.loadtxt("data/Data 70-F-0/1.txt", delimiter="\t", usecols=(1, 2))
    except Exception as e:
        st.error("Failed to load default example file.")
        st.stop()

impeller_signal = data[:, 0] - np.mean(data[:, 0])  # Impeller side (Bearing)
motor_signal = data[:, 1] - np.mean(data[:, 1])     # Motor side (Pulley)

# Plot time-domain signals
st.subheader("Time Domain Signals")
st.line_chart({"Impeller Side (Bearing)": impeller_signal, "Motor Side (Pulley)": motor_signal})

# Frequency analysis function
def compute_fft(signal, sample_rate=10000):
    fft_result = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal), d=1/sample_rate)
    return freq[:len(signal) // 2], np.abs(fft_result[:len(signal) // 2])

def calculate_characteristic_frequencies(speed_rpm, driver_diameter=63, belt_length=912):
    drive_speed_hz = speed_rpm / 60
    fr = (drive_speed_hz * np.pi * driver_diameter) / belt_length
    return {
        "n/2": drive_speed_hz / 2,
        "fr": fr,
        "2fr": 2 * fr,
        "4fr": 4 * fr,
        "6fr": 6 * fr,
        "8fr": 8 * fr,
        "n": drive_speed_hz
    }

char_freqs = calculate_characteristic_frequencies(400)

# Plot FFT for both measurements
for signal, label in zip([impeller_signal, motor_signal], ["Impeller Side (Bearing)", "Motor Side (Pulley)"]):
    freq, fft_magnitude = compute_fft(signal)
    fig, ax = plt.subplots()
    ax.plot(freq, fft_magnitude, label='FFT Magnitude')
    ax.set_xlim(0, 30)
    ax.set_ylim(0, np.max(fft_magnitude[:len(freq)//4]) * 1.2)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title(f"FFT of {label} Signal (DC removed)")

    for f_label, f_val in char_freqs.items():
        color = "orange" if f_label == "n/2" else "purple"
        linestyle = "-." if f_label == "n/2" else "--"
        ax.axvline(f_val, color=color, linestyle=linestyle, alpha=0.6)
        ax.text(f_val, np.max(fft_magnitude[:len(freq)//4]) * 0.9, f"{f_label}", color=color, ha="center", fontsize=8, rotation=90)

    st.pyplot(fig)

# Feature extraction from impeller side only
features = extract_features(impeller_signal)

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
