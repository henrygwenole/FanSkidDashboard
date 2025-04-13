# README.md

## 🛠️ Predictive Maintenance Dashboard
This is a multipage Streamlit app designed to monitor a G.U.N.T. belt-driven diagnostic system.

It consists of:
- **Home.py**: The system health overview and entry point
- **pages/Sensor_Data.py**: Detailed sensor plots and diagnostics

---

### 🧭 File Structure
```
📁 predictive-maintenance-dashboard/
├── Home.py                     # Main page (overview grid and navigation)
├── pages/
│   └── Sensor_Data.py          # Sensor signals and FFT analysis
├── data/
│   └── Data 110-F-0/51.txt     # Sample signal
├── README.md
```

---

### 🚀 How to Run Locally
```bash
cd predictive-maintenance-dashboard
streamlit run Home.py
```

Make sure `pages/Sensor_Data.py` exists and data files are in the correct path.

---

### 🧪 Pages Description
- `Home.py` provides a status overview and links to other sections
- `Sensor_Data.py` shows:
  - Time-domain signals
  - Frequency-domain FFT
  - Harmonic overlays
  - Diagnosis: Healthy / Fault

---

### 🧠 Dataset Info
Default data comes from:
```
data/Data 110-F-0/51.txt
```
This corresponds to a **faulty belt**, pretension 110 N, speed 2000 RPM.

---

### 🔗 Navigation
Streamlit's multipage app system automatically renders files in `/pages` as links in the sidebar. You can also link between them using:
```python
st.page_link("pages/Sensor_Data.py", label="🔍 View Sensor Analysis")
```

---

### 👓 AR Launch
You can simulate a maintenance workflow by tapping the AR app:
```markdown
[Open on HoloLens](frn://s/6u615mm)
```
---