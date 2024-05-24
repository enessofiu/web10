import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import pytz
import time

# Titulli i aplikacionit
st.title('Weather Dashboard')

# Load custom CSS (assuming your CSS file is named "styles.css")
css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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

# Function to calculate forecast for the actual day
def calculate_actual_day_forecast(df_today):
    if not df_today.empty:
        forecast_data = {
            'TC_predicted': df_today.iloc[-1]['TC_predicted'],
            'HUM_predicted': df_today.iloc[-1]['HUM_predicted'],
            'PRES_predicted': df_today.iloc[-1]['PRES_predicted'],
            'US_predicted': df_today.iloc[-1]['US_predicted'],
            'SOIL1_predicted': df_today.iloc[-1]['SOIL1_predicted']
        }
    else:
        forecast_data = {}
    return forecast_data

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

    # Filter data for the current date
    df_today = get_today_data(df, current_datetime)

    # Extract the latest data point for current conditions
    if not df_today.empty:
        current_data = df_today.iloc[-1]
    else:
        st.error("No data available for today.")
        return

    # Lokacioni aktual
    current_location = 'Prizren, Kosovë'
    st.subheader(f'Current Location: {current_location}')

    # Ikona e motit dhe temperatura
    col1, col2 = st.columns([3, 1])
    with col1:
        st.image('https://upload.wikimedia.org/wikipedia/commons/a/a6/Golden_Gate_Bridge_fog.JPG', use_column_width=True)
    with col2:
        st.markdown(f"### {current_data['TC_predicted']:.2f}°C")
        st.markdown(f"#### {current_datetime.strftime('%A, %I:%M:%S %p')}")
        st.markdown('##### Partly Cloudy')

    # Pikat kryesore të ditës
    st.subheader("Today's Highlights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Precipitation", "2%")  # Assuming constant, as no precipitation data in the dataset
    col2.metric("Humidity", f"{current_data['HUM_predicted']}%")
    col3.metric("Wind", "0 km/h")  # Assuming constant, as no wind data in the dataset
    col4.metric("Sunrise & Sunset", "6:18 AM", "7:27 PM")  # Assuming constant times

    # Parashikimi për 3 ditët e ardhshme
    st.subheader('3 Days Forecast')
    forecast_data_actual_day = calculate_actual_day_forecast(df_today)
    if forecast_data_actual_day:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write(f"<div class='metric-container'><h4>Temperature</h4><div class='metric-value'>{forecast_data_actual_day['TC_predicted']:.2f}°C</div></div>", unsafe_allow_html=True)
        with col2:
            st.write(f"<div class='metric-container'><h4>Humidity</h4><div class='metric-value'>{forecast_data_actual_day['HUM_predicted']:.2f}%</div></div>", unsafe_allow_html=True)
        with col3:
            st.write(f"<div class='metric-container'><h4>Pressure</h4><div class='metric-value'>{forecast_data_actual_day['PRES_predicted']:.2f}</div></div>", unsafe_allow_html=True)
        with col4:
            st.write(f"<div class='metric-container'><h4>US</h4><div class='metric-value'>{forecast_data_actual_day['US_predicted']:.2f}</div></div>", unsafe_allow_html=True)
        with col5:
            st.write(f"<div class='metric-container'><h4>Soil</h4><div class='metric-value'>{forecast_data_actual_day['SOIL1_predicted']:.2f}</div></div>", unsafe_allow_html=True)
    else:
        st.error("No data available for the forecast.")

    # Calculate forecast for the next 3 days
    forecast_data_3_days = calculate_3_day_forecast(df, current_datetime)

    # Display forecast for the next 3 days
    for i in range(3):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write(f"<div class='metric-container'><h4>Temperature</h4><div class='metric-value'>{forecast_data_3_days['TC_predicted'][i]:.2f}°C</div></div>", unsafe_allow_html=True)
        with col2:
            st.write(f"<div class='metric-container'><h4>Humidity</h4><div class='metric-value'>{forecast_data_3_days['HUM_predicted'][i]:.2f}%</div></div>", unsafe_allow_html=True)
        with col3:
            st.write(f"<div class='metric-container'><h4>Pressure</h4><div class='metric-value'>{forecast_data_3_days['PRES_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)
        with col4:
            st.write(f"<div class='metric-container'><h4>US</h4><div class='metric-value'>{forecast_data_3_days['US_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)
        with col5:
            st.write(f"<div class='metric-container'><h4>Soil</h4><div class='metric-value'>{forecast_data_3_days['SOIL1_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)


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
