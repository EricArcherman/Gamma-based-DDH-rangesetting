#!/usr/bin/env python3
'''
Description: Combines the high frequency (hf) index data with the daily option volatility data into a curated high frequency options volatility and index price dataset.
Author: Eric Archerman
Date: 16 July 2024
'''
import os
import pandas as pd
import matplotlib.pyplot as plt

LOC = 'data/data_raw/'

HF_FILES = [
        '22-7-12.csv',
        '23-1-7.csv',
        '23-7-12.csv',
        '24-1-7.csv',
    ]
DAILY_FILE = 'option-daily.csv'


def data_cleaning(loc, hf_files, daily_file):
    '''
    Converts the high frequency spot and daily volatility data into pandas dataframes, then cleans the data for later curation.

    Args:
        loc (string): relative file path to data
        hf_files (list of strings): high frequency data files
        daily_file (string): daily option volatility data

    Returns:
        hf_data (pandas dataframe): cleaned hf data compatible with daily data
        daily_file (pandas dataframe): cleaned daily data compatible with hf data

    Raises:
        General error: If there is an error with reading the .csv files.
    '''
    # .csv files into 2 dataframes: (1) hf_data, (2) daily_data
    try:
        hf_data_sep = [pd.read_csv(os.path.join(loc, file)) for file in hf_files]
        daily_data = pd.read_csv(os.path.join(loc, daily_file))
    except Exception as e:
        print(f"An error occured: {e}")
        hf_data_sep = []
        daily_data = None
    
    # aligning the format of the dataframes
    hf_data = pd.concat(hf_data_sep, ignore_index=True)
    daily_columns = ['timestamp', 'indexPrice', 'volExpiry', 'volATM', 'vol10C', 'vol10P', 'vol25C', 'vol25P']
    daily_data = daily_data[daily_columns]

    # converting to same time range
    hf_data['timestamp'] = pd.to_datetime(hf_data['timestamp'], unit='ms')
    daily_data['timestamp'] = pd.to_datetime(daily_data['timestamp'], unit='ms')

    latest_date = daily_data.iloc[-1, 0]
    hf_data = hf_data[hf_data['timestamp'] <= latest_date]

    # rounding daily data timestamps to nearest minute
    daily_data['timestamp'] = daily_data['timestamp'].dt.round('min')

    print(hf_data.tail())
    print(daily_data.tail())

    return hf_data, daily_data

def mesh(hf_data, daily_data):
    '''
    Meshes together the cleaned data

    Args:
        hf_data (pandas dataframe): cleaned hf data compatible with daily data
        daily_file (pandas dataframe): cleaned daily data compatible with hf data

    Returns:
        meshed_data (pandas dataframe): meshed hf and daily data
    '''
    daily_data = daily_data.drop('indexPrice', axis=1)
    meshed_data = pd.merge_ordered(hf_data, daily_data, on='timestamp')

    print(meshed_data.tail())

    meshed_data.to_csv('meshed.csv')

    return meshed_data


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
    hf, daily = data_cleaning(LOC, HF_FILES, DAILY_FILE)

    meshed = mesh(hf, daily)
    
    # plot(hf, daily)



if __name__ == '__main__':
    main()