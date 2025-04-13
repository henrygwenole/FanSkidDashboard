# Sensor_Data.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sensor Signal Analysis", layout="wide")
st.title("📈 Sensor Signal Analysis")

# Load both faulty and good data for comparison
try:
    faulty_data = np.loadtxt("data/Data 110-F-0/51.txt", delimiter="\t", usecols=(1, 2))
    good_data = np.loadtxt("data/Data 110-H-0/51.txt", delimiter="\t", usecols=(1, 2))
except Exception as e:
    st.error("Failed to load example data files.")
    st.stop()

impeller_faulty = faulty_data[:, 0] - np.mean(faulty_data[:, 0])
motor_faulty = faulty_data[:, 1] - np.mean(faulty_data[:, 1])
impeller_good = good_data[:, 0] - np.mean(good_data[:, 0])
motor_good = good_data[:, 1] - np.mean(good_data[:, 1])

# Frequency analysis function
def compute_fft(signal, sample_rate=10000):
    windowed = signal * np.hanning(len(signal))
    fft_result = np.fft.fft(windowed)
    freq = np.fft.fftfreq(len(signal), d=1/sample_rate)
    return freq[:len(signal) // 2], np.abs(fft_result[:len(signal) // 2]) / len(signal)

# Updated frequency markers from reference article
char_freqs = {
    "n/2": 20,
    "2fr": 30,
    "4fr": 40,
    "n": 45,
    "6fr": 60,
    "8fr": 80
}

# Time Domain
st.subheader("Time Domain Signals")
st.line_chart({
    "Faulty - Bearing Sensor": impeller_faulty,
    "Good - Bearing Sensor": impeller_good,
    "Faulty - Pulley Sensor": motor_faulty,
    "Good - Pulley Sensor": motor_good
})

# Frequency Domain
st.subheader("Frequency Domain Comparison (FFT)")
for faulty, good, label in zip([motor_faulty, impeller_faulty], [motor_good, impeller_good], ["Pulley Sensor", "Bearing Sensor"]):
    freq_f, fft_f = compute_fft(faulty)
    freq_g, fft_g = compute_fft(good)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(freq_f, fft_f, label="Faulty", color="red", alpha=0.7)
    ax.plot(freq_g, fft_g, label="Good", color="blue", alpha=0.6)
    ax.set_xlim(0, 220)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title(f"FFT Comparison for {label}")
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.legend()

    for f_label, f_val in char_freqs.items():
        color = "orange" if f_label == "n/2" else "purple"
        linestyle = "-." if f_label == "n/2" else "--"
        ax.axvline(f_val, color=color, linestyle=linestyle, alpha=0.6)
        ax.text(f_val, max(max(fft_f), max(fft_g)) * 0.85, f_label, color=color, ha="center", fontsize=8, rotation=90)

    st.pyplot(fig)

# Diagnostic summary
st.subheader("Illustrated Diagnostic Result")
def illustrate_classification(signal):
    rms = np.sqrt(np.mean(signal ** 2))
    peak = np.max(np.abs(signal))
    crest_factor = peak / rms if rms > 0 else 0
    
    if rms > 0.05 and peak > 0.1:
        if crest_factor > 5:
            return "⚠️ Fault Detected", "High crest factor may indicate loose components or shock loads."
        elif crest_factor > 3:
            return "⚠️ Fault Detected", "Moderate crest factor. Possible misalignment or belt wear."
        else:
            return "⚠️ Fault Detected", "Abnormal vibration detected. Inspect motor and belt system."
    else:
        return "✅ Healthy", "System appears to be running normally."

classification_label, explanation = illustrate_classification(impeller_faulty)
st.write(classification_label)
if "Fault" in classification_label:
    st.error(explanation)
else:
    st.success(explanation)

st.markdown("""
### 👓 Launch AR Maintenance App
[Open on HoloLens](frn://s/6u615mm)
""", unsafe_allow_html=True)
