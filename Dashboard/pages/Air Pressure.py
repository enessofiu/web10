import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to construct the file path
def get_file_path(filename):
    """
    Constructs the absolute path to the data file.

    Args:
        filename (str): The name of the data file (e.g., "cleaned_data.csv").

    Returns:
        str: The absolute path to the data file.
    """
    return os.path.join(current_dir, filename)

# Define the filename
data_file = "cleaned_data.csv"


# Function to load the data
@st.cache_data
def load_data(file_path):
    """
    Loads the data from the specified file path.

    Args:
        file_path (str): The absolute path to the data file.

    Returns:
        pandas.DataFrame: The loaded data as a pandas DataFrame.
    """
    data = pd.read_csv(file_path)
    # Add any necessary data processing steps here (e.g., handling missing values)
    # ...
    return data


# Load the data using the function
data = load_data(get_file_path(data_file))

# Data processing (assuming the 'timestamp' column exists)
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Filter for Air Pressure (PRES)
pres_data = data[['timestamp', 'PRES']]

# Page title
st.title("Air Pressure (PRES) Visualizations")

# Arrange buttons in a single row
col1, col2, col3, col4 = st.columns(4)

# Button to show Line Chart
if col1.button("Show Air Pressure Over Time"):
    st.markdown("<div class='card'><h3>Air Pressure Over Time</h3></div>", unsafe_allow_html=True)
    st.line_chart(pres_data.set_index('timestamp')['PRES'])

# Button to show Bar Chart
if col2.button("Show Air Pressure Distribution"):
    st.markdown("<div class='card'><h3>Air Pressure Distribution</h3></div>", unsafe_allow_html=True)
    st.bar_chart(pres_data.set_index('timestamp')['PRES'])

# Button to show Pie Chart
if col3.button("Show Air Pressure Proportions"):
    st.markdown("<div class='card'><h3>Air Pressure Proportions</h3></div>", unsafe_allow_html=True)
    pres_bins = pd.cut(pres_data['PRES'], bins=5)
    pres_pie_data = pres_bins.value_counts().reset_index()
    pres_pie_data.columns = ['Air Pressure Range', 'Count']  # Rename columns
    fig, ax = plt.subplots()
    ax.pie(pres_pie_data['Count'], labels=pres_pie_data['Air Pressure Range'], autopct='%1.1f%%')
    st.pyplot(fig)

# Button to show Scatter Plot
if col4.button("Show Air Pressure Scatter Plot"):
    st.markdown("<div class='card'><h3>Air Pressure Scatter Plot</h3></div>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    sns.scatterplot(x='timestamp', y='PRES', data=pres_data, ax=ax)
    st.pyplot(fig)

st.markdown("<footer>Smart Agriculture Dashboard © 2024</footer>", unsafe_allow_html=True)
