# Sensor_Data.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sensor Signal Analysis", layout="wide")
st.title("📈 Sensor Signal Analysis")

# Load default data directly without file uploader
try:
    data = np.loadtxt("data/Data 110-F-0/51.txt", delimiter="\t", usecols=(1, 2))
except Exception as e:
    st.error("Failed to load default example file.")
    st.stop()

impeller_signal = data[:, 0] - np.mean(data[:, 0])  # Impeller side (Bearing)
motor_signal = data[:, 1] - np.mean(data[:, 1])     # Motor side (Pulley)

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
        "n/2": drive_speed_hz / 2,
        "fr": fr,
        "2fr": 2 * fr,
        "4fr": 4 * fr,
        "6fr": 6 * fr,
        "8fr": 8 * fr,
        "n": drive_speed_hz
    }

char_freqs = calculate_characteristic_frequencies(2000)

# Time Domain
st.subheader("Time Domain Signals")
st.line_chart({"Impeller Side (Bearing)": impeller_signal, "Motor Side (Pulley)": motor_signal})

# Frequency Domain
st.subheader("Frequency Domain (FFT)")
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

# Diagnostic summary
st.subheader("Illustrated Diagnostic Result")
def illustrate_classification(signal):
    rms = np.sqrt(np.mean(signal ** 2))
    peak = np.max(np.abs(signal))
    if rms > 0.05 and peak > 0.1:
        return "⚠️ Fault Detected", "Maintenance Required! Possible misalignment or belt wear."
    else:
        return "✅ Healthy", "System appears to be running normally."

classification_label, explanation = illustrate_classification(impeller_signal)
st.write(classification_label)
if "Fault" in classification_label:
    st.error(explanation)
else:
    st.success(explanation)

st.markdown("""
### 👓 Launch AR Maintenance App
[Open on HoloLens](frn://s/6u615mm)
""", unsafe_allow_html=True)