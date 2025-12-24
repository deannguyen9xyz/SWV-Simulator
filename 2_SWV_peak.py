import numpy as np
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#=================
# 1. Load SWV data
#=================

data_dir = 'data'
data_path = os.path.join(data_dir, 'SWV_curve.csv')
df = pd.read_csv(data_path, header=0, skiprows=[1])

#=================
# 2. Find Baseline
#=================

# 1. Setup parameters
window_size = 10
search_limit = int(len(df) * 0.4)  # Only look for baseline in the first 40% of data
best_r2 = 0
best_model = None
baseline_x_range = None

# 2. Sliding Window to find the best linear region
for i in range(0, search_limit):
    window = df.iloc[i : i + window_size]
    X = window[['Vstep']].values
    y = window['Idif'].values
    
    model = LinearRegression().fit(X, y)
    r2 = model.score(X, y)
    
    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        baseline_x_range = (window['Vstep'].min(), window['Vstep'].max())

# 3. Create the Baseline across the whole range
df['Baseline_A'] = best_model.predict(df[['Vstep']].values)

A = best_model.coef_[0]
B = best_model.intercept_

#====================
# 3. Find Peak Height
#====================

# Peak location
peak_index = df["Idif"].idxmax()
peak_vstep = round(df["Vstep"].iloc[peak_index], 3)
peak_idif = df["Idif"].iloc[peak_index]

# Get the baseline value at the specific peak index
baseline_at_peak = df["Baseline_A"].iloc[peak_index]

# Calculate the true peak height
true_peak_height = peak_idif - baseline_at_peak

print(f"--- Peak Analysis ---")
print(f"Raw Peak Current: {peak_idif * 1e6:.2f} uA")
print(f"Best Baseline equation: y = {A:.2e} * x + {B:.2e}")
print(f"Best Baseline R^2: {best_r2:.5f}")
print(f"Calculated Peak Height: {true_peak_height * 1e6:.5f} uA at {peak_vstep:.3f} V")

#=================
# 4. Visualization
#=================

plt.figure(figsize=(14, 10))

plt.plot(df['Vstep'], df['Idif'] * 1e6, '.-', label='Original Data', color='purple')
plt.plot(df['Vstep'], df['Baseline_A'] * 1e6, '--', label='Linear Baseline', color='red')

plt.vlines(x=peak_vstep, ymin=baseline_at_peak * 1e6, ymax=peak_idif * 1e6, color='green', linestyle='-', linewidth=2, label='Peak Height')
plt.text(peak_vstep + 0.01, (baseline_at_peak + true_peak_height / 2) * 1e6,
         f'Peak Height: {true_peak_height * 1e6:.3f} uA\nat {peak_vstep:.3f} V',
         color='black', fontsize=12)

plt.ylabel('Current (uA)', fontsize=14)
plt.xlabel('Potential (V)', fontsize=14)
plt.title('Baseline Correction using Sliding Window Linearity', fontsize=18)
plt.legend(fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()