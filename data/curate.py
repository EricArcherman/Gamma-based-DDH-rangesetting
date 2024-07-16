#!/usr/bin/env python3
'''
Description: Combines the high frequency (hf) index data with the daily option volatility data into a curated high frequency options volatility and index price dataset.
Author: Eric Archerman
Date: 16 July 2024
'''
import os
import pandas as pd
import matplotlib.pyplot as plt


def data():
    loc = 'data/data_raw/'

    hf_files = [
        '22-7-12.csv',
        '23-1-7.csv',
        '23-7-12.csv',
        '24-1-7.csv',
    ]

    daily_file = 'option-daily.csv'

    hf_data_sep = [pd.read_csv(os.path.join(loc, file)) for file in hf_files]
    hf_data = pd.concat(hf_data_sep, ignore_index=True)

    daily_data = pd.read_csv(os.path.join(loc, daily_file)).drop(["currency", "data", 'underlyingPrice'], axis='columns')

    hf_data['timestamp'] = pd.to_datetime(hf_data['timestamp'], unit='ms')
    daily_data['timestamp'] = pd.to_datetime(daily_data['timestamp'], unit='ms')

    latest_date = daily_data.iloc[-1, 1]
    hf_data = hf_data[hf_data['timestamp'] <= latest_date]

    print(hf_data.tail())
    print(daily_data.tail())

    return hf_data, daily_data





def plot(hf_data, daily_data):
    # Plot high-frequency data
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot indexPrice from high-frequency data
    plt.subplot(2, 1, 1)
    plt.plot(hf_data['timestamp'], hf_data['indexPrice'], label='HF Index Price', color='blue')
    plt.plot(daily_data['timestamp'], daily_data['indexPrice'], label='Daily Index Price', color='red')
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



def main():
    hf, daily = data()
    
    # plot(hf, daily)



if __name__ == '__main__':
    main()