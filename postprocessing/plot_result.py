import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Define the Data
data = {
    'min obs./obj. class': [25, 50, 100, 200, 400, 800],
    'WRA': [44.79, 48.96, 58.95, 62.17, 64.43, 65.75],
    'WER': [52.9, 49.2, 39.8, 36.84, 35.11, 33.98],
    'CRA': [65.61, 69.25, 77.92, 79.66, 81.64, 81.51],
    'CER': [23.25, 20.52, 15.99, 15.21, 13.92, 14.41]
}

df = pd.DataFrame(data)

# Step 2: Polynomial Regression for trend estimation
x = df['min obs./obj. class']
y_vars = ['WRA', 'WER', 'CRA', 'CER']
colors = ['green', 'red', 'lightgreen', 'lightcoral']
lines = {}

# Fit and extrapolate
x_fit = np.linspace(25, 3200, 500)  # For plotting smooth lines
for y_var, color in zip(y_vars, colors):
    # Polynomial fit
    coefs = np.polyfit(x, df[y_var], deg=3)
    poly = np.poly1d(coefs)
    lines[y_var] = poly(x_fit)

# Step 3: Plotting
sns.set_style("darkgrid")
plt.figure(figsize=(10, 6))

for y_var, color in zip(y_vars, colors):
    plt.plot(x_fit, lines[y_var], label=f'Trend of {y_var}', color=color)
    plt.scatter(x, df[y_var], color=color)  # Plot actual data points

plt.title("Trends and Data for WRA, WER, CRA, and CER")
plt.xlabel("min obs./obj. class")
plt.ylabel("Values")
plt.ylim(-1,101)
plt.legend()
plt.show()
