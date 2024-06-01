import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

def exponential_decay(x, a, b, c):
    return a * np.exp(-b * x) + c

# Step 1: Define the Data
data = {
    'min obs./obj. class': [25, 50, 100, 200, 400, 800],
    'WRA': [0.4479, 0.4896, 0.5895, 0.6217, 0.6443, 0.6575],
    'WER': [0.529, 0.492, 0.398, 0.3684, 0.3511, 0.3398],
    'CRA': [0.6561, 0.6925, 0.7792, 0.7966, 0.8164, 0.8151],
    'CER': [0.2325, 0.2052, 0.1599, 0.1521, 0.1392, 0.1441]
}

df = pd.DataFrame(data)

# Step 2: Fit Exponential Decay Model
x = np.array(df['min obs./obj. class'])
x_fit = np.linspace(25, 1000, 500)  # For extrapolation and smooth curve
lines = {}

# Plotting setup
sns.set_style("darkgrid")
plt.figure(figsize=(10, 6))
colors = ['green', 'red', 'lightgreen', 'lightcoral']
y_vars = ['WRA', 'WER', 'CRA', 'CER']
full_bsbhd_values = [0.8580, 0.1420, 0.9441, 0.0559]

for y_var, color, bsbhd_value in zip(y_vars, colors, full_bsbhd_values):
    y = np.array(df[y_var])
    # Fit exponential decay function
    popt, _ = curve_fit(exponential_decay, x, y, maxfev=10000, p0=[1, 0.01, 0])
    lines[y_var] = exponential_decay(x_fit, *popt)
    
    # Plotting
    plt.plot(x_fit, lines[y_var], label=f'Trend of {y_var}', color=color)
    plt.scatter(x, y, color=color)  # Actual data points
    plt.axhline(y=bsbhd_value, color=color, linestyle='--', label=f'Full BSBHD {y_var}')

plt.title("Trends and Data for WRA, WER, CRA, and CER")
plt.xlabel("min obs./obj. class")
plt.ylabel("Values")
plt.ylim(0, 1)
plt.legend()
plt.show()
