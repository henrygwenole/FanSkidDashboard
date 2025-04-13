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

def calculate_characteristic_frequencies(speed_rpm, driver_diameter=63, belt_length=912):
    drive_speed_hz = speed_rpm / 60
    fr = (drive_speed_hz * np.pi * driver_diameter) / belt_length
    return {
        "fr": fr,
        "2fr": 2 * fr,
        "4fr": 4 * fr,
        "6fr": 6 * fr,
        "8fr": 8 * fr,
        "n": drive_speed_hz,
        "n/2": drive_speed_hz / 2
    }

char_freqs = calculate_characteristic_frequencies(2000)

# Time Domain
st.subheader("Time Domain Signals")
st.line_chart({"Faulty - Bearing": impeller_faulty, "Good - Bearing": impeller_good, "Faulty - Pulley": motor_faulty, "Good - Pulley": motor_good})

# Frequency Domain
st.subheader("Frequency Domain Comparison (FFT)")
for faulty, good, label in zip([impeller_faulty, motor_faulty], [impeller_good, motor_good], ["Impeller Side (Bearing)", "Motor Side (Pulley)"]):
    freq_f, fft_f = compute_fft(faulty)
    freq_g, fft_g = compute_fft(good)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(freq_f, fft_f, label="Faulty", color="red", alpha=0.7)
    ax.plot(freq_g, fft_g, label="Good", color="blue", alpha=0.6)
    ax.set_xlim(0, 2000)
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
    if rms > 0.05 and peak > 0.1:
        return "⚠️ Fault Detected", "Maintenance Required! Possible misalignment or belt wear."
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
