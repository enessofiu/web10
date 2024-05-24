import streamlit as st
import pandas as pd
import os
from prophet import Prophet

# Function to retrieve the data path
def get_data_path():
    """
    This function retrieves the data path, assuming it's stored within your deployed app.

    Returns:
        str: Path to the CSV file (relative to your app's location).
    """
    # Assuming your CSV file is named "predicted_data_2024.csv" and located within the app directory
    data_path = "predicted_data_2024.csv"
    return data_path

# Function to get the absolute path to the current directory
def get_file_path(filename):
    """
    Constructs the absolute path to the data file.

    Args:
        filename (str): The name of the data file (e.g., "cleaned_data.csv").

    Returns:
        str: The absolute path to the data file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)

# Prophet prediction code
def generate_predictions():
    # Load the dataset
    df = pd.read_csv(get_file_path('cleaned_data.csv'))

    # Convert timestamp to datetime and handle timezones consistently
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)

    # Ensure correct data types and check for missing values
    df = df.fillna(method='ffill')  # Forward fill missing values

    # Specify the columns in the original dataset that you want to predict
    sensors = ['TC', 'HUM', 'PRES', 'US', 'SOIL1']

    # Resample data to hourly averages
    df.set_index('timestamp', inplace=True)
    hourly_data = df.resample('H').mean().reset_index()

    # Placeholder DataFrame to store 2023 yhat values
    yhat_2023 = pd.DataFrame()

    # Iterate through columns for prediction
    for sensor in sensors:
        # Create DataFrame for current column
        sensor_data = pd.DataFrame({'ds': hourly_data['timestamp'], 'y': hourly_data[sensor]})

        # Remove outliers using IQR
        Q1 = sensor_data['y'].quantile(0.25)
        Q3 = sensor_data['y'].quantile(0.75)
        IQR = Q3 - Q1
        sensor_data = sensor_data[(sensor_data['y'] >= (Q1 - 1.5 * IQR)) & (sensor_data['y'] <= (Q3 + 1.5 * IQR))]

        # Print sensor_data for inspection (optional)
        print(sensor_data.head())

        # Create Prophet model with potential hyperparameter tuning
        model = Prophet(
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10,
            yearly_seasonality=True,
            daily_seasonality=True
        )

        # Fit the model
        model.fit(sensor_data)

        # Create future DataFrame for 2023 with consistent timezone handling
        future_2023 = model.make_future_dataframe(periods=8760 - len(sensor_data), freq='H')  # Ensure we have 8760 hours for a full year
        future_2023['ds'] = future_2023['ds'].dt.tz_localize(None)  # Remove timezone if needed

        # Make predictions for 2023
        forecast_2023 = model.predict(future_2023)

        # Extract yhat values for 2023
        yhat_2023[sensor + '_yhat'] = forecast_2023['yhat'].values

    # Create prediction DataFrame with hourly frequency for 2024
    prediction_data = pd.DataFrame(index=pd.date_range('2024-01-01 00:00:00', '2024-12-31 23:00:00', freq='H'))
    prediction_data['timestamp'] = prediction_data.index

    # Repeat the 2023 yhat values for 2024
    repeats = int(len(prediction_data) / len(yhat_2023)) + 1
    yhat_2023_repeated = pd.concat([yhat_2023] * repeats, ignore_index=True).iloc[:len(prediction_data)]

    # Add the repeated yhat values to the prediction DataFrame
    for sensor in sensors:
        prediction_data[sensor + '_predicted'] = yhat_2023_repeated[sensor + '_yhat'].values

    # Save predictions to CSV
    prediction_data.to_csv(get_file_path('predicted_data_2024.csv'), index=False)

    # Print the head of the predictions dataset
    print(prediction_data.head())

    print('Predictions complete. The result is saved in predicted_data_2024.csv')

# Check if prediction file exists; if not, generate predictions
if not os.path.exists(get_file_path(get_data_path())):
    generate_predictions()

# Load custom CSS (assuming your CSS file is named "styles.css")
css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the data path (assuming the file is within the app)
data_path = get_data_path()

# Load the data
data = pd.read_csv(get_file_path(data_path))

# Convert timestamp column to datetime (assuming consistent format)
data["timestamp"] = pd.to_datetime(data["timestamp"])

# Sidebar for date/time selection
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", data["timestamp"].min())
end_date = st.sidebar.date_input("End Date", data["timestamp"].max())

# Check if the start and end dates are the same
if start_date == end_date:
    st.sidebar.write("Select hours for the same day:")
    start_time = st.sidebar.time_input("Start Time", pd.to_datetime(data['timestamp']).min().time())
    end_time = st.sidebar.time_input("End Time", pd.to_datetime(data['timestamp']).max().time())
else:
    start_time = pd.to_datetime(data['timestamp']).min().time()
    end_time = pd.to_datetime(data['timestamp']).max().time()

# Sidebar for parameter selection
parameter_dict = {
    "TC_predicted": "Temperature",
    "HUM_predicted": "Humidity",
    "PRES_predicted": "Air Pressure",
    "US_predicted": "Ultrasound",
    "SOIL1_predicted": "Soil Moisture"
}
parameter = st.sidebar.selectbox("Parameter", list(parameter_dict.keys()), format_func=lambda x: parameter_dict[x])

# Filter data based on date and time selection
if start_date == end_date:
    filtered_data = data[
        (data["timestamp"] >= pd.to_datetime(f"{start_date} {start_time}")) &
        (data["timestamp"] <= pd.to_datetime(f"{end_date} {end_time}"))
    ]
else:
    filtered_data = data[
        (data["timestamp"] >= pd.to_datetime(f"{start_date} {start_time}")) &
        (data["timestamp"] <= pd.to_datetime(f"{end_date} {end_time}"))
    ]

# Display filtered data
st.markdown(f"<div class='main'><h2>{parameter_dict[parameter]} Data from {start_date} to {end_date}</h2></div>", unsafe_allow_html=True)
st.line_chart(filtered_data.set_index("timestamp")[parameter])

# Display min and max values
min_value = filtered_data[parameter].min()
max_value = filtered_data[parameter].max()
st.markdown(f"<div class='card'><p>Min {parameter_dict[parameter]}: {min_value}</p><p>Max {parameter_dict[parameter]}: {max_value}</p></div>", unsafe_allow_html=True)

st.markdown("<footer>Smart Agriculture Dashboard © 2024</footer>", unsafe_allow_html=True)
