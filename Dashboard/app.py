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
css_file_path = os.path.join(os.path.dirname(_file_), "styles.css")
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
    current_dir = os.path.dirname(os.path.abspath(_file_))
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
    # Today's Highlights
    st.markdown(
    f"""
    <style>
        .highlight-box {{
            background-color: #3498db;
            padding: 10px;
            border-radius: 5px;
            margin: 10px;
        }}
        .highlight-box h3, .highlight-box h4, .highlight-box p {{
            color: white;
            margin: 5px;
        }}
        .highlight-box .highlight-item {{
            flex: 1;
            padding: 5px;
        }}
        @media only screen and (max-width: 600px) {{
            .highlight-box {{
                padding: 5px;
            }}
        }}
    </style>
    <div class="highlight-box">
        <h3>Today's Highlights</h3>
        <div style="display:flex; flex-wrap: wrap;">
            <div class="highlight-item">
                <h4>Soil</h4>
                <p>{current_data['SOIL1_predicted']:.2f}%</p>
            </div>
            <div class="highlight-item">
                <h4>Humidity</h4>
                <p>{current_data['HUM_predicted']:.2f}%</p>
            </div>
            <div class="highlight-item">
                <h4>Wind</h4>
                <p>{current_data['PRES_predicted']:.2f} km/h</p>
            </div>
            <div class="highlight-item">
                <h4>Ultrasound</h4>
                <p>{current_data['US_predicted']:.2f}</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


    # Parashikimi për 3 ditët e ardhshme
 # Display forecast for the next 3 days
    
    
    st.subheader('3 Days Forecast')
    forecast_data_actual_day = calculate_actual_day_forecast(df_today)

    

    if forecast_data_actual_day:
        st.markdown(
            f"""
            <div style="background-color:#3498db;padding:10px;border-radius:5px">
                <h3 style="color:white">Today's Forecast</h3>
                <div style="display:flex;">
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">Temperature</h4>
                        <p style="color:white">{forecast_data_actual_day['TC_predicted']:.2f}°C</p>
                    </div>
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">Humidity</h4>
                        <p style="color:white">{forecast_data_actual_day['HUM_predicted']:.2f}%</p>
                    </div>
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">Pressure</h4>
                        <p style="color:white">{forecast_data_actual_day['PRES_predicted']:.2f}</p>
                    </div>
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">US</h4>
                        <p style="color:white">{forecast_data_actual_day['US_predicted']:.2f}</p>
                    </div>
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">Soil</h4>
                        <p style="color:white">{forecast_data_actual_day['SOIL1_predicted']:.2f}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("No data available for the forecast.")

    # Display forecast for the next 3 days
    for i in range(3):
        forecast_data_day = forecast_data_3_days[i]
        st.markdown(
            f"""
            <div style="background-color:#3498db;padding:10px;margin-top:10px;border-radius:5px">
                <h3 style="color:white">Day {i+1} Forecast</h3>
                <div style="display:flex;">
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">Temperature</h4>
                        <p style="color:white">{forecast_data_day['TC_predicted']:.2f}°C</p>
                    </div>
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">Humidity</h4>
                        <p style="color:white">{forecast_data_day['HUM_predicted']:.2f}%</p>
                    </div>
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">Pressure</h4>
                        <p style="color:white">{forecast_data_day['PRES_predicted']:.2f}</p>
                    </div>
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">US</h4>
                        <p style="color:white">{forecast_data_day['US_predicted']:.2f}</p>
                    </div>
                    <div style="flex:1;padding:10px;">
                        <h4 style="color:white">Soil</h4>
                        <p style="color:white">{forecast_data_day['SOIL1_predicted']:.2f}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    # Temperature and Humidity Analytics for Today
    st.subheader('Analytics for Today')

    # Resample the data for visualization
    df_today_resampled = df_today.set_index('timestamp').resample('3H').mean()

    # Show the plots for temperature, humidity, pressure, US, and Soil vertically
    fig, ax = plt.subplots(5, 1, figsize=(10, 15))

    # Plot temperature
    ax[0].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['TC_predicted'], marker='o')
    ax[0].set_ylabel('Temperature (°C)')
    ax[0].set_title('Temperature')

    # Plot humidity
    ax[1].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['HUM_predicted'], marker='o')
    ax[1].set_ylabel('Humidity (%)')
    ax[1].set_title('Humidity')

    # Plot pressure
    ax[2].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['PRES_predicted'], marker='o')
    ax[2].set_ylabel('Pressure')
    ax[2].set_title('Pressure')

    # Plot US
    ax[3].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['US_predicted'], marker='o')
    ax[3].set_ylabel('US')
    ax[3].set_title('US')

    # Plot Soil
    ax[4].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['SOIL1_predicted'], marker='o')
    ax[4].set_ylabel('Soil')
    ax[4].set_title('Soil')

    # Adjust layout
    plt.tight_layout()

    # Show the plots vertically
    st.pyplot(fig)

# Run the main function
if _name_ == '_main_':
    main()
