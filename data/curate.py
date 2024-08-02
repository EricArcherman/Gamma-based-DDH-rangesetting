#!/usr/bin/env python3
'''
Description: Combines the high frequency (hf) index data with the daily option volatility data into a curated high frequency options volatility and index price dataset.
Author: Eric Archerman
Date: 16 July 2024
'''
import os
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import random
from graphing import raw_data_plot, vol_plot

LOC = 'data/data_raw/'

HF_FILES = [
        '22-7-12.csv',
        '23-1-7.csv',
        '23-7-12.csv',
        '24-1-7.csv',
        '24-7.csv'
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
        # hf data
        hf_data_sep = []
        for file in hf_files:
            file_path = os.path.join(loc, file)
            print(f"Reading file: {file_path}")
            df = pd.read_csv(file_path)
            hf_data_sep.append(df)

        # daily data
        print(f"Reading file: {os.path.join(loc, daily_file)}")
        daily_data = pd.read_csv(os.path.join(loc, daily_file))
    except Exception as e:
        print(f"An error occured: {e}")
        exit()
    
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
    Meshes together the cleaned data and interpolates missing values as follows: volExpiry w/ backfill. volATM, 10C, 10P, 25C, 25P w/ cubic spline interpolation, then add random noise.

    Args:
        hf_data (pandas dataframe): cleaned hf data compatible with daily data
        daily_file (pandas dataframe): cleaned daily data compatible with hf data

    Returns:
        meshed_data (pandas dataframe): meshed hf and daily data
    '''
    daily_data = daily_data.drop('indexPrice', axis=1)
    meshed_data = pd.merge_ordered(hf_data, daily_data, on='timestamp')

    meshed_data['volExpiry'] = meshed_data['volExpiry'].bfill()

    x_range = list(range(len(meshed_data)))
    for column in meshed_data.columns[-5:]:
        curve = CubicSpline(np.where(~np.isnan(meshed_data[column]))[0], meshed_data[column][~np.isnan(meshed_data[column])])
        meshed_data[column] = curve(x_range)

    pre_noise = meshed_data.copy()

    for column in meshed_data.columns[-5:]:
        noise = [random.uniform(-0.0025, 0.0025) for _ in range(len(meshed_data))]
        meshed_data[column] = meshed_data[column] + noise

    meshed_data.to_csv('meshed.csv', index=False) # meshed_data.to_csv(os.path.join('data', 'meshed.csv'), index=False)

    return pre_noise, meshed_data

def main():
    hf, daily = data_cleaning(LOC, HF_FILES, DAILY_FILE)

    pre_noise, meshed_data = mesh(hf, daily)

    # the [:100] is for a close-up snapshot. For the whole graph, just delete the '[:100].'
    # raw_data_plot(hf[:100], daily[:100])
    vol_plot(daily, pre_noise[:100], meshed_data[:100])

if __name__ == '__main__':
    main()