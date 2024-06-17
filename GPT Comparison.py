import pandas as pd
import matplotlib.pyplot as plt

# Sample data (in practice, you would collect this from your experiments)
data = {
    'Tool': ['GPT', 'Human', 'IntelliCode', 'TabNine', 'SonarQube'],
    'CO2 Emissions (kg)': [0.0000196, 0.000025, 0.000021, 0.000020, 0.000022],
    'Execution Time (seconds)': [0.1, 300, 0.15, 0.12, 0.18],
    'Energy Consumption (kWh)': [0.0003, 0.0004, 0.00035, 0.00032, 0.00033],
    'Optimization Effectiveness (%)': [95, 85, 90, 92, 88]
}

df = pd.DataFrame(data)

# Plot CO2 Emissions
plt.figure(figsize=(10, 6))
plt.bar(df['Tool'], df['CO2 Emissions (kg)'], color='green')
plt.xlabel('Tool')
plt.ylabel('CO2 Emissions (kg)')
plt.title('CO2 Emissions Comparison')
plt.show()

# Plot Execution Time
plt.figure(figsize=(10, 6))
plt.bar(df['Tool'], df['Execution Time (seconds)'], color='blue')
plt.xlabel('Tool')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time Comparison')
plt.show()

# Plot Energy Consumption
plt.figure(figsize=(10, 6))
plt.bar(df['Tool'], df['Energy Consumption (kWh)'], color='red')
plt.xlabel('Tool')
plt.ylabel('Energy Consumption (kWh)')
plt.title('Energy Consumption Comparison')
plt.show()

# Plot Optimization Effectiveness
plt.figure(figsize=(10, 6))
plt.bar(df['Tool'], df['Optimization Effectiveness (%)'], color='purple')
plt.xlabel('Tool')
plt.ylabel('Optimization Effectiveness (%)')
plt.title('Optimization Effectiveness Comparison')
plt.show()
