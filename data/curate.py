import os
import pandas as pd
import matplotlib.pyplot as plt

loc = 'data/data_raw/'

hf_files = [
    '22-7-12.csv',
    '23-1-7.csv',
    '23-7-12.csv',
    '24-1-7.csv',
]

daily_file = 'option-interday.csv'

hf_data_sep = [pd.read_csv(os.path.join(loc, file)) for file in hf_files]
hf_data = pd.concat(hf_data_sep, ignore_index=True)

daily_data = pd.read_csv(os.path.join(loc, daily_file))

print("read csv files:")

print(hf_data.head())
print(daily_data.head())

##############################################

hf_data['timestamp'] = pd.to_datetime(hf_data['timestamp'], unit='ms')
daily_data['timestamp'] = pd.to_datetime(daily_data['timestamp'], unit='ms')

print("converted csv times:")

print(hf_data.head())
print(daily_data.head())

##############################################

fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot high-frequency data
plt.figure(figsize=(15, 7))

# Plot indexPrice from high-frequency data
plt.subplot(2, 1, 1)
plt.plot(hf_data['timestamp'], hf_data['indexPrice'], label='HF Index Price', color='blue')
plt.plot(daily_data['timestamp'], daily_data['indexPrice'], label='Daily Index Price', color='red')
plt.plot(daily_data['timestamp'], daily_data['underlyingPrice'], label='Underlying Price', color='green')
plt.title('High-Frequency Data')
plt.xlabel('Time')
plt.ylabel('Index Price')
plt.legend()

# Plot daily data
plt.subplot(2, 1, 2)
plt.plot(daily_data['timestamp'], daily_data['volATM'], label='Volatility ATM', color='purple')
plt.plot(daily_data['timestamp'], daily_data['vol10C'], label='Volatility 10C', color='orange')
plt.plot(daily_data['timestamp'], daily_data['vol10P'], label='Volatility 10P', color='pink')
plt.plot(daily_data['timestamp'], daily_data['vol25C'], label='Volatility 25C', color='brown')
plt.plot(daily_data['timestamp'], daily_data['vol25P'], label='Volatility 25P', color='grey')

plt.title('Daily Data')
plt.xlabel('Time')
plt.ylabel('Values')
plt.legend()

plt.tight_layout()
plt.show()