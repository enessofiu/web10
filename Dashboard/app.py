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

# Function to calculate forecasted values for next 3 days
def calculate_forecast(df):
    # Get current date
    current_date = datetime.now(tz).date()

    # Calculate forecast for the next 3 days
    forecast_data = {}
    for metric in ['TC_predicted', 'HUM_predicted', 'PRES_predicted', 'US_predicted', 'SOIL1_predicted']:
        forecast_values = []
        for i in range(3):
            forecast_date = current_date + timedelta(days=i)
            # Here you can implement your own logic to predict the values based on historical data
            # For demonstration purposes, let's assume the forecasted value is the same as the last available value
            forecast_value = df.loc[df['timestamp'].dt.date == current_date, metric].iloc[-1]
            forecast_values.append(forecast_value)
        forecast_data[metric] = forecast_values
    return forecast_data

# Load dataset
data_file = "predicted_data_2024.csv"
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

# Main dashboard function
def main():
    # Get current datetime in GMT+1
    current_datetime = get_current_time_gmt_plus_1()

    # Filter data for the current date
    df_today = get_today_data(df, current_datetime)

    # Extract the latest data point for current conditions
    if not df_today.empty:
        current_data = df_today.iloc[-1]
    else:
        st.error("No data available for today.")
        return

    # Location
    current_location = 'Prizren, Kosovë'
    st.subheader(f'Current Location: {current_location}')

    # Weather icon and temperature
    col1, col2 = st.columns([3, 1])
    with col1:
        st.image('https://upload.wikimedia.org/wikipedia/commons/a/a6/Golden_Gate_Bridge_fog.JPG', use_column_width=True)
    with col2:
        st.markdown(f"### {current_data['TC_predicted']:.2f}°C")
        st.markdown(f"#### {current_datetime.strftime('%A, %I:%M:%S %p')}")
        st.markdown('##### Partly Cloudy')

    # Today's Highlights
    st.subheader("Today's Highlights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Precipitation", "2%")  # Assuming constant, as no precipitation data in the dataset
    col2.metric("Humidity", f"{current_data['HUM_predicted']}%")
    col3.metric("Wind", "0 km/h")  # Assuming constant, as no wind data in the dataset
    col4.metric("Sunrise & Sunset", "6:18 AM", "7:27 PM")  # Assuming constant times

    # Forecast for the next 3 days
    st.subheader('3 Days Forecast')
    forecast_data = calculate_forecast(df)
    
    for i in range(len(forecast_data['TC_predicted'])):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write(f"<div class='metric-container'><h4>Temperature</h4><div class='metric-value'>{forecast_data['TC_predicted'][i]:.2f}°C</div></div>", unsafe_allow_html=True)
        with col2:
            st.write(f"<div class='metric-container'><h4>Humidity</h4><div class='metric-value'>{forecast_data['HUM_predicted'][i]:.2f}%</div></div>", unsafe_allow_html=True)
        with col3:
            st.write(f"<div class='metric-container'><h4>Pressure</h4><div class='metric-value'>{forecast_data['PRES_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)
        with col4:
            st.write(f"<div class='metric-container'><h4>US</h4><div class='metric-value'>{forecast_data['US_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)
        with col5:
            st.write(f"<div class='metric-container'><h4>Soil</h4><div class='metric-value'>{forecast_data['SOIL1_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)

    # Temperature and Humidity Analytics for Today
    st.subheader('Temperature Analytics')
    df_today_resampled = df_today.set_index('timestamp').resample('3H').mean()  # Resample every 3 hours and compute mean

    fig, ax = plt.subplots(2)
    ax[0].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['TC_predicted'], marker='o')
    ax[1].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['HUM_predicted'], marker='o')
    ax[0].set_ylabel('Temperature (°C)')
    ax[1].set_ylabel('Humidity (%)')
    st.pyplot(fig)

# Run the main function
if __name__ == '__main__':
    main()
