# SWV-Simulator
Python-based Square Wave Voltammetry (SWV) simulator, specifically designed to handle the complex baselines found in MIP (Molecularly Imprinted Polymer) sensors by using a sliding-window linear regression to isolate the true peak signal from background capacitive current.

---

## 🎯 Purpose of This Project

* Simulation of SWV: Modeling the potential staircase and square wave pulses to simulate the current response of a redox system.
* Advanced Data Processing: implementing a Sliding Window Linear Regression to automatically identify and subtract sloped baselines.
* GitHub portfolio demonstration.

--- 

## ▶️ How to Run

Run script `1_SWV_simulation.py` to generate data in *data/*.

Run script `2_SWV_peak.py` to find peak height from generated curve.

---

## 📊 Result and Conclusion

**1. Simulated SWV Curve:** The simulator models the differential current ($I_{dif} = I_{fwd} - I_{rev}$), producing the characteristic bell-shaped curve. By incorporating charging current ($\text{i} = \text{C} \cdot \frac{dV}{dt}$), the model accurately reflects real-world MIP sensor data with a non-zero baseline.
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/4616d7fa-7152-4557-bf06-0b0813f16a2b" />

**2. Baseline Correction & Peak Detection:** The analysis script utilizes a sliding window (10 points) to find the region of highest linearity in the pre-peak zone. It then extrapolates a baseline equation ($y = Ax + B$) to calculate the true Faradaic peak height.
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/e93104ad-01ee-4878-a8a0-8ff4c6c1054a" />

--- 

## 🧑‍💻 Author

Developed by: Vu Bao Chau Nguyen, Ph.D.

Keywords: Square Wave Voltammetry (SWV), Molecularly Imprinted Polymers (MIP), Baseline Correction, Signal Processing.

---
