import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import pytz
import time

# Function to construct the file path
def get_file_path(filename):
    """
    Constructs the absolute path to the data file.

    Args:
        filename (str): The name of the data file (e.g., "predicted_data_2024.csv").

    Returns:
        str: The absolute path to the data file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)

# Define the filename
data_file = "predicted_data_2024.csv"

# Load dataset
df = pd.read_csv(get_file_path(data_file))

# Convert the timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set timezone to GMT+1
tz = pytz.timezone('Europe/Belgrade')  # Prizren is in the same timezone as Belgrade

# Function to get the current time in GMT+1
def get_current_time_gmt_plus_1():
    return datetime.now(tz)

# Filter data for the current date
def get_today_data(df, current_datetime):
    return df[df['timestamp'].dt.date == current_datetime.date()]

# Function to calculate forecast for the next 3 days
def calculate_3_day_forecast(df, current_datetime):
    forecast_data = {
        'TC_predicted': [],
        'HUM_predicted': [],
        'PRES_predicted': [],
        'US_predicted': [],
        'SOIL1_predicted': []
    }
    for i in range(3):
        next_date = current_datetime + timedelta(days=i+1)
        df_next_day = df[df['timestamp'].dt.date == next_date.date()]
        if not df_next_day.empty:
            forecast_data['TC_predicted'].append(df_next_day.iloc[-1]['TC_predicted'])
            forecast_data['HUM_predicted'].append(df_next_day.iloc[-1]['HUM_predicted'])
            forecast_data['PRES_predicted'].append(df_next_day.iloc[-1]['PRES_predicted'])
            forecast_data['US_predicted'].append(df_next_day.iloc[-1]['US_predicted'])
            forecast_data['SOIL1_predicted'].append(df_next_day.iloc[-1]['SOIL1_predicted'])
        else:
            forecast_data['TC_predicted'].append(None)
            forecast_data['HUM_predicted'].append(None)
            forecast_data['PRES_predicted'].append(None)
            forecast_data['US_predicted'].append(None)
            forecast_data['SOIL1_predicted'].append(None)
    return forecast_data

# Main dashboard function
def main():
    # Get current datetime in GMT+1
    current_datetime = get_current_time_gmt_plus_1()

    # Parashikimi për 3 ditët e ardhshme
    st.subheader('3 Days Forecast')

    # Calculate forecast for the next 3 days
    forecast_data_3_days = calculate_3_day_forecast(df, current_datetime)

    # Display forecast for the next 3 days
    days = [current_datetime + timedelta(days=i+1) for i in range(3)]
    for i in range(3):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write(f"<div class='metric-container'><h4>{days[i].strftime('%A')}</h4><div class='metric-value'>{forecast_data_3_days['TC_predicted'][i]:.2f}°C</div></div>", unsafe_allow_html=True)
        with col2:
            st.write(f"<div class='metric-container'><h4>{days[i].strftime('%A')}</h4><div class='metric-value'>{forecast_data_3_days['HUM_predicted'][i]:.2f}%</div></div>", unsafe_allow_html=True)
        with col3:
            st.write(f"<div class='metric-container'><h4>{days[i].strftime('%A')}</h4><div class='metric-value'>{forecast_data_3_days['PRES_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)
        with col4:
            st.write(f"<div class='metric-container'><h4>{days[i].strftime('%A')}</h4><div class='metric-value'>{forecast_data_3_days['US_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)
        with col5:
            st.write(f"<div class='metric-container'><h4>{days[i].strftime('%A')}</h4><div class='metric-value'>{forecast_data_3_days['SOIL1_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)


    # Temperature and Humidity Analytics for Today
    st.subheader('Analytics for Today')

    # Resample the data for visualization
    df_today_resampled = df_today.set_index('timestamp').resample('3H').mean()

    # Create subplots
    fig, ax = plt.subplots(3, 2, figsize=(10, 10))

    # Plot temperature
    ax[0, 0].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['TC_predicted'], marker='o')
    ax[0, 0].set_ylabel('Temperature (°C)')
    ax[0, 0].set_title('Temperature')

    # Plot humidity
    ax[0, 1].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['HUM_predicted'], marker='o')
    ax[0, 1].set_ylabel('Humidity (%)')
    ax[0, 1].set_title('Humidity')

    # Plot pressure
    ax[1, 0].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['PRES_predicted'], marker='o')
    ax[1, 0].set_ylabel('Pressure')
    ax[1, 0].set_title('Pressure')

    # Plot US
    ax[1, 1].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['US_predicted'], marker='o')
    ax[1, 1].set_ylabel('US')
    ax[1, 1].set_title('US')

    # Plot Soil
    ax[2, 0].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['SOIL1_predicted'], marker='o')
    ax[2, 0].set_ylabel('Soil')
    ax[2, 0].set_title('Soil')

    # Hide the empty subplot
    ax[2, 1].axis('off')

    # Adjust layout
    plt.tight_layout()

    # Show the plots
    st.pyplot(fig)

# Run the main function
if __name__ == '__main__':
    main()
