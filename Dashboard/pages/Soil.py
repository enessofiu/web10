import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set page configuration to wide mode
st.set_page_config(page_title="Smart Agriculture Dashboard", layout="wide")


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

def load_data(file_path):
    """
    Loads the data from the specified file path.

    Args:
        file_path (str): The absolute path to the data file.

    Returns:
        pandas.DataFrame: The loaded data as a pandas DataFrame.
    """
    return pd.read_csv(file_path)

def get_data_path():
    """
    This function retrieves the data path, assuming it's stored within your deployed app.

    Returns:
        str: Path to the CSV file (relative to your app's location).
    """
    # Assuming your CSV file is named "cleaned_data.csv" and located within the app directory
    data_path = "cleaned_data.csv"
    return data_path

# Load custom CSS
css_file_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the data path (assuming the file is within the app)
data_path = get_data_path()

# Load the data
data = load_data(get_file_path(data_path))
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Filter for Soil Moisture (SOIL1)
soil_data = data[['timestamp', 'SOIL1']]

# Page title
st.markdown("<div class='header'>Soil Moisture (SOIL1) Visualizations</div>", unsafe_allow_html=True)

# Page title
st.markdown("<div class='card'><h3>Choose a Visualizations</h3></div>", unsafe_allow_html=True)

# Initialize or get the session state to track the current chart type
if 'current_chart' not in st.session_state:
    st.session_state.current_chart = 'line'

# Arrange buttons in a single row
col1, col2, col3, col4 = st.columns(4)

# Button to show Line Chart
if col1.button("Show Line Chart"):
    st.session_state.current_chart = 'line'

# Button to show Bar Chart
if col2.button("Show Soil Moisture Distribution"):
    st.session_state.current_chart = 'bar'

# Button to show Pie Chart
if col3.button("Show Soil Moisture Proportions"):
    st.session_state.current_chart = 'pie'

# Button to show Scatter Plot
if col4.button("Show Soil Moisture Scatter Plot"):
    st.session_state.current_chart = 'scatter'

# Display the corresponding chart based on the current chart type
if st.session_state.current_chart == 'line':
    st.markdown("<div class='card'><h3>Soil Moisture Over Time</h3></div>", unsafe_allow_html=True)
    st.line_chart(soil_data.set_index('timestamp')['SOIL1'],color='#365341')

elif st.session_state.current_chart == 'bar':
    st.markdown("<div class='card'><h3>Soil Moisture Distribution</h3></div>", unsafe_allow_html=True)
    st.bar_chart(soil_data.set_index('timestamp')['SOIL1'],color='#365341')

elif st.session_state.current_chart == 'pie':
    st.markdown("<div class='card'><h3>Soil Moisture Proportions</h3></div>", unsafe_allow_html=True)
    soil_bins = pd.cut(soil_data['SOIL1'], bins=5)
    soil_pie_data = soil_bins.value_counts().reset_index()
    soil_pie_data.columns = ['Soil Moisture Range', 'Count']
    fig, ax = plt.subplots()
    ax.pie(soil_pie_data['Count'], labels=soil_pie_data['Soil Moisture Range'], autopct='%1.1f%%')
    st.pyplot(fig)

elif st.session_state.current_chart == 'scatter':
    st.markdown("<div class='card'><h3>Soil Moisture Scatter Plot</h3></div>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    sns.scatterplot(x='timestamp', y='SOIL1', data=soil_data, ax=ax)
    st.pyplot(fig)

st.markdown("<footer>Smart Agriculture Dashboard © 2024</footer>", unsafe_allow_html=True)
