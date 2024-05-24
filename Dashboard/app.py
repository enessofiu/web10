import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import pytz

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
    return forecast_data

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

    # Today's Highlights
    st.subheader("Today's Highlights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Precipitation", "2%")  # Assuming constant, as no precipitation data in the dataset
    col2.metric("Humidity", f"{current_data['HUM_predicted']}%")
    col3.metric("Wind", "0 km/h")  # Assuming constant, as no wind data in the dataset
    col4.metric("Sunrise & Sunset", "6:18 AM", "7:27 PM")  # Assuming constant times

    # 3 Days Forecast
    st.subheader('3 Days Forecast')
    forecast_data = calculate_3_day_forecast(df, current_datetime)
    days = [(current_datetime + timedelta(days=i+1)).strftime('%A') for i in range(3)]
    for day, temp, hum, pres, us, soil in zip(days, forecast_data['TC_predicted'], forecast_data['HUM_predicted'], forecast_data['PRES_predicted'], forecast_data['US_predicted'], forecast_data['SOIL1_predicted']):
        st.write(f"**{day}:**")
        st.write(f"- Temperature: {temp:.2f}°C")
        st.write(f"- Humidity: {hum:.2f}%")
        st.write(f"- Pressure: {pres:.2f}")
        st.write(f"- US: {us:.2f}")
        st.write(f"- Soil: {soil:.2f}")

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
