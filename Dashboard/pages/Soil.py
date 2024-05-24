import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

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
    data = pd.read_csv(file_path)
    # Add any necessary data processing steps here (e.g., handling missing values)
    # ...
    return data


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
st.title("Soil Moisture (SOIL1) Visualizations")

# Line Chart (displayed only on the first page load)
st.markdown("<div class='card'><h3>Soil Moisture Over Time</h3></div>", unsafe_allow_html=True)
st.line_chart(soil_data.set_index('timestamp')['SOIL1'])

# Arrange buttons in a single row
col1, col2, col3, col4 = st.columns(4)

# Button to show Bar Chart
if col1.button("Show Soil Moisture Distribution"):
    st.markdown("<div class='card'><h3>Soil Moisture Distribution</h3></div>", unsafe_allow_html=True)
    st.bar_chart(soil_data.set_index('timestamp')['SOIL1'])

# Button to show Pie Chart
if col2.button("Show Soil Moisture Proportions"):
    st.markdown("<div class='card'><h3>Soil Moisture Proportions</h3></div>", unsafe_allow_html=True)
    soil_bins = pd.cut(soil_data['SOIL1'], bins=5)
    soil_pie_data = soil_bins.value_counts().reset_index()
    soil_pie_data.columns = ['Soil Moisture Range', 'Count'] 
    # Rename columns
    fig, ax = plt.subplots()
    ax.pie(soil_pie_data['Count'], labels=soil_pie_data['Soil Moisture Range'], autopct='%1.1f%%')
    st.pyplot(fig)

# Button to show Scatter Plot
if col3.button("Show Soil Moisture Scatter Plot"):
    st.markdown("<div class='card'><h3>Soil Moisture Scatter Plot</h3></div>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    sns.scatterplot(x='timestamp', y='SOIL1', data=soil_data, ax=ax)
    st.pyplot(fig)

st.markdown("<footer>Smart Agriculture Dashboard © 2024</footer>", unsafe_allow_html=True)
