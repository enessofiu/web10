import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import pytz

# Set page configuration
st.set_page_config(page_title="Weather and Agriculture Dashboard", layout="wide")

# Load custom CSS
css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to construct the file path
def get_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)

# Cache the data loading function
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    return data

# Cache the function to calculate average values
@st.cache_data
def calculate_averages(data):
    avg_values = {
        "TC": data["TC"].mean(),
        "HUM": data["HUM"].mean(),
        "PRES": data["PRES"].mean(),
        "US": data["US"].mean(),
        "SOIL1": data["SOIL1"].mean()
    }
    return avg_values

# Load the main dataset
data_file = "predicted_data_2024.csv"
data = load_data(get_file_path(data_file))

# Convert the timestamp column to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

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

def main():
    # Get current datetime in GMT+1
    current_datetime = get_current_time_gmt_plus_1()

    # Filter data for the current date
    df_today = get_today_data(data, current_datetime)

    # Extract the latest data point for current conditions
    if not df_today.empty:
        current_data = df_today.iloc[-1]
    else:
        st.error("No data available for today.")
        return

    # Current Location
    current_location = 'Prizren, Kosovë'
    st.subheader(f'Current Location: {current_location}')

    # Weather icon and temperature
    col1, col2 = st.columns([3, 1])
    with col1:
        st.image('download.jpg', use_column_width=True)
    with col2:
        st.markdown(f"### {current_data['TC_predicted']:.2f}°C")
        st.markdown(f"#### {current_datetime.strftime('%A, %I:%M:%S %p')}")
        st.markdown('##### Partly Cloudy')

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
                    <h4>Pressure</h4>
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

    # Today's Forecast
    forecast_data_actual_day = calculate_actual_day_forecast(df_today)

    if forecast_data_actual_day:
        st.markdown(
            f"""
            <div style="background-color:#3498db;padding:10px;border-radius:5px">
                <h3 style="color:white">Today's Forecast</h3>
                <div style="display:flex; flex-wrap: wrap;">
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

    # Calculate the 3-day forecast
    forecast_data_3_days = calculate_3_day_forecast(data, current_datetime)

    # Display forecast for the next 3 days
    st.subheader('3 Days Forecast')
    for i in range(3):
        forecast_data_day = {
            'TC_predicted': forecast_data_3_days['TC_predicted'][i],
            'HUM_predicted': forecast_data_3_days['HUM_predicted'][i],
            'PRES_predicted': forecast_data_3_days['PRES_predicted'][i],
            'US_predicted': forecast_data_3_days['US_predicted'][i],
            'SOIL1_predicted': forecast_data_3_days['SOIL1_predicted'][i]
        }
        st.markdown(
            f"""
            <div style="background-color:#3498db;padding:10px;border-radius:5px;margin-top:10px;">
                <h3 style="color:white">{(current_datetime + timedelta(days=i+1)).strftime('%A')}</h3>
                <div style="display:flex; flex-wrap: wrap;">
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

    # Display data visualization options
    st.sidebar.title("Data Visualization")
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Line Chart", "Bar Chart"])
    column_to_plot = st.sidebar.selectbox("Select Column", ["TC_predicted", "HUM_predicted", "PRES_predicted", "US_predicted", "SOIL1_predicted"])

    if chart_type == "Line Chart":
        st.subheader(f"{column_to_plot} - Line Chart")
        fig, ax = plt.subplots()
        ax.plot(data['timestamp'], data[column_to_plot], label=column_to_plot)
        ax.set_xlabel("Timestamp")
        ax.set_ylabel(column_to_plot)
        ax.legend()
        st.pyplot(fig)

    elif chart_type == "Bar Chart":
        st.subheader(f"{column_to_plot} - Bar Chart")
        fig, ax = plt.subplots()
        ax.bar(data['timestamp'], data[column_to_plot], label=column_to_plot)
        ax.set_xlabel("Timestamp")
        ax.set_ylabel(column_to_plot)
        ax.legend()
        st.pyplot(fig)

    # Display data analytics options
    st.sidebar.title("Data Analytics")
    if st.sidebar.button("Calculate Averages"):
        avg_values = calculate_averages(data)
        st.subheader("Average Values")
        st.write(avg_values)

if __name__ == "__main__":
    main()
