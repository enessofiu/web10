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

# Function to calculate forecast for the next three days
# Function to calculate forecast for the next three days
def calculate_three_days_forecast(df_today):
    forecast_data = []
    current_date = df_today.iloc[-1]['timestamp'].date()
    for i in range(3):
        # Filter data for the current date
        df_current_day = df_today[df_today['timestamp'].dt.date == current_date]
        if not df_current_day.empty:
            forecast_data.append({
                'TC_predicted': df_current_day.iloc[-1]['TC_predicted'],
                'HUM_predicted': df_current_day.iloc[-1]['HUM_predicted'],
                'PRES_predicted': df_current_day.iloc[-1]['PRES_predicted'],
                'US_predicted': df_current_day.iloc[-1]['US_predicted'],
                'SOIL1_predicted': df_current_day.iloc[-1]['SOIL1_predicted']
            })
        else:
            forecast_data.append({})
        # Move to the next day
        current_date += timedelta(days=1)
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
        st.markdown('##### Partly Cloudy')

    # Today's Highlights
    st.subheader("Today's Highlights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Soil", f"{current_data['SOIL1_predicted']}%")  # Using soil data as precipitation
    col2.metric("Humidity", f"{current_data['HUM_predicted']}%")
    col3.metric("Wind", f"{current_data['PRES_predicted']} km/h")  # Using pres data as wind
    col4.metric("Ultrasound", f"{current_data['US_predicted']}")  # Using US data for both

    # 3 Days Forecast
    st.subheader('3 Days Forecast')
    forecast_data = calculate_three_days_forecast(df_today)
    if forecast_data:
        for day, data in enumerate(forecast_data, 1):
            st.write(f"### Day {day}")
            if data:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.write(f"<div class='metric-container'><h4>Temperature</h4><div class='metric-value'>{data['TC_predicted']:.2f}°C</div></div>", unsafe_allow_html=True)
                with col2:
                    st.write(f"<div class='metric-container'><h4>Humidity</h4><div class='metric-value'>{data['HUM_predicted']:.2f}%</div></div>", unsafe_allow_html=True)
                with col3:
                    st.write(f"<div class='metric-container'><h4>Pressure</h4><div class='metric-value'>{data['PRES_predicted']:.2f}</div></div>", unsafe_allow_html=True)
                with col4:
                    st.write(f"<div class='metric-container'><h4>US</h4><div class='metric-value'>{data['US_predicted']:.2f}</div></div>", unsafe_allow_html=True)
                with col5:
                    st.write(f"<div class='metric-container'><h4>Soil</h4><div class='metric-value'>{data['SOIL1_predicted']:.2f}</div></div>", unsafe_allow_html=True)
            else:
                st.error("No data available for the forecast.")
    else:
        st.error("No data available for the forecast.")

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
