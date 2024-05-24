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
    This function retrieves the data path from an environment variable or a default location.

    Returns:
        str: Path to the CSV file.
    """
    data_path = os.environ.get("DATA_PATH", "./cleaned_data.csv")
    return data_path


# Load custom CSS
css_file_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the data path
data_path = get_data_path()

# Load the data
data = load_data(get_file_path(data_path))
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Filter for Ultrasound (US)
us_data = data[['timestamp', 'US']]

# Page title
st.title("Ultrasound (US) Visualizations")

# Line Chart
st.markdown("<div class='card'><h3>Ultrasound Over Time</h3></div>", unsafe_allow_html=True)
st.line_chart(us_data.set_index('timestamp')['US'])

# Bar Chart
st.markdown("<div class='card'><h3>Ultrasound Distribution</h3></div>", unsafe_allow_html=True)
st.bar_chart(us_data.set_index('timestamp')['US'])

# Pie Chart
st.markdown("<div class='card'><h3>Ultrasound Proportions</h3></div>", unsafe_allow_html=True)
us_bins = pd.cut(us_data['US'], bins=5)
us_pie_data = us_bins.value_counts().reset_index()
us_pie_data.columns = ['Ultrasound Range', 'Count']  # Rename columns
fig, ax = plt.subplots()
ax.pie(us_pie_data['Count'], labels=us_pie_data['Ultrasound Range'], autopct='%1.1f%%')
st.pyplot(fig)

# Scatter Plot
st.markdown("<div class='card'><h3>Ultrasound Scatter Plot</h3></div>", unsafe_allow_html=True)
fig, ax = plt.subplots()
sns.scatterplot(x='timestamp', y='US', data=us_data, ax=ax)
st.pyplot(fig)

st.markdown("<footer>Smart Agriculture Dashboard © 2024</footer>", unsafe_allow_html=True)