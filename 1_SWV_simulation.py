import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

#==============
# 1. Parameters
#==============

E_start_formal = -0.33  # where oxidation and reduction are equal
E_initial = -0.6        
E_final = -0.15         
C_bulk = 1.0e-7 # bulk concentration of the analyte (mol/cm³)       
D = 1e-5        # diffusion coefficient (cm²/s)                
n = 1           # number of electrons transferred in the redox reaction
F = 96485
R = 8.314
T = 298.15
sigma = F / (R * T)

#===============================
# 2. SWV & MIP Specific Settings
#===============================

E_step = 0.005  # step size (V)          
E_sw = 0.025    # pulse amplitude (V)            
f = 25          # frequency (Hz)                        
tau = 1/f       # time for one square-wave cycle (s)

C_dl = 10e-6    # double-layer capacitance of the MIP film, from non-faradic current
background_offset = 0.5e-6 # small constant current from impurities or oxygen

#===================
# 4. Numerical Setup
#===================

steps_per_half = 40  # number of small time steps in each half pulse   
dt = (tau / 2) / steps_per_half # time step size (s)
dx = np.sqrt(D * dt / 0.45) # thickness of one diffusion layer slice (cm)
L = 150  # number of spatial points in the diffusion layer               
alpha = D * dt / (dx**2) # stability factor for diffusion calculation

C_O = np.ones(L) * C_bulk   # oxidized species concentration (initially everywhere)
C_R = np.zeros(L)   # reduced species concentration (initially zero)

e_axis = np.arange(E_initial, E_final, E_step)  # potential axis for SWV
i_net = [] # to store net current values     

#===================
# 5. Simulation Loop
#===================

for E_base in e_axis:
    # Forward Pulse
    E_fwd = E_base + E_sw
    for _ in range(steps_per_half): # simulate diffusion during this pulse
        ratio = np.exp(n * sigma * (E_fwd - E_start_formal))    # Nernst equation
        c_surf = C_O[0] + C_R[0]    # total concentration at the surface
        C_R[0] = c_surf / (1 + ratio) # update surface concentrations
        C_O[0] = c_surf - C_R[0]
        C_O[1:-1] += alpha * (C_O[2:] - 2*C_O[1:-1] + C_O[:-2]) # diffusion step, away from the electrode
        C_R[1:-1] += alpha * (C_R[2:] - 2*C_R[1:-1] + C_R[:-2]) 
    
    i_fwd_faradaic = -n * F * D * (C_O[1] - C_O[0]) / dx
    # Charging current approximation: i = C * dV/dt
    i_fwd_charging = C_dl * (E_sw / (tau/2)) 

    # Reverse Pulse
    E_rev = E_base - E_sw
    for _ in range(steps_per_half):
        ratio = np.exp(n * sigma * (E_rev - E_start_formal))
        c_surf = C_O[0] + C_R[0]
        C_R[0] = c_surf / (1 + ratio)
        C_O[0] = c_surf - C_R[0]
        C_O[1:-1] += alpha * (C_O[2:] - 2*C_O[1:-1] + C_O[:-2])
        C_R[1:-1] += alpha * (C_R[2:] - 2*C_R[1:-1] + C_R[:-2])
        
    i_rev_faradaic = -n * F * D * (C_O[1] - C_O[0]) / dx
    i_rev_charging = C_dl * (-E_sw / (tau/2))

    # Calculate net current with baseline components
    total_fwd = i_fwd_faradaic + i_fwd_charging + background_offset
    total_rev = i_rev_faradaic + i_rev_charging + background_offset
    
    i_net.append(total_fwd - total_rev)

#=============
# 6. Save data
#=============

# Create csv file
data_dir = 'data'
file_path = os.path.join(data_dir, 'SWV_curve.csv')
os.makedirs(data_dir, exist_ok=True)

# Define DataFrame
df_data = pd.DataFrame({
    'Vstep': e_axis,
    'Idif': i_net
})

# Define the two header rows
header_names = ['Vstep', 'Idif']
header_units = ['V', 'uA'] 

# Write the names row
with open(file_path, 'w') as f:
    f.write(','.join(header_names) + '\n')
# Write the units row
with open(file_path, 'a') as f:
    f.write(','.join(header_units) + '\n')
# Append the actual data without the pandas default header and index
df_data.to_csv(file_path, mode='a', header=False, index=False)

print(df_data.head())

#============
# 7. Plotting
#============

plt.figure(figsize=(14, 10))

plt.plot(e_axis, np.array(i_net) * 1e6, '.-', color='purple', linewidth=1.5)

plt.xlabel("Vstep (V)", fontsize=14)
plt.ylabel("Idif (uA)", fontsize=14)
plt.title("MIP Sensor SWV Simulation with Non-Zero Baseline", fontsize=18)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()