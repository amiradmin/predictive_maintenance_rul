import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time
import numpy as np

# Dashboard title
st.title("Factory Predictive Maintenance Dashboard (RUL & Predicted Failure Date)")

# Project root path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

# Path to CSV log
LOG_FILE = os.path.join(PROJECT_ROOT, "data", "sensor_logs.csv")

# Use session state to manage refresh and data
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
if 'df' not in st.session_state:
    st.session_state.df = None


# Function to generate sample data if CSV doesn't exist or is invalid
def generate_sample_data():
    st.warning("Generating sample data for demonstration...")

    # Create sample data for 3 machines
    machines = ['Machine_001', 'Machine_002', 'Machine_003']
    data = []

    for i in range(100):  # 100 data points
        timestamp = datetime.now() - pd.Timedelta(hours=i)
        for machine in machines:
            # Base values with some randomness
            temp = 70 + np.random.normal(0, 5)
            vibration = 0.5 + np.random.normal(0, 0.1)
            pressure = 100 + np.random.normal(0, 10)
            run_hours = 500 + i * 2
            rul_hours = max(0, 1000 - run_hours - np.random.randint(0, 100))

            # Calculate predicted failure date
            failure_date = timestamp + pd.Timedelta(hours=rul_hours)

            data.append({
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'machine_id': machine,
                'temperature': temp,
                'vibration': vibration,
                'pressure': pressure,
                'run_hours': run_hours,
                'rul_hours': rul_hours,
                'predicted_failure_date': failure_date.strftime('%Y-%m-%d %H:%M:%S')
            })

    return pd.DataFrame(data)


# Safe datetime conversion function
def safe_datetime_conversion(series, format='mixed'):
    try:
        return pd.to_datetime(series, format=format, errors='coerce')
    except:
        return pd.to_datetime(series, errors='coerce')


# Safe numeric conversion function
def safe_numeric_conversion(series):
    try:
        return pd.to_numeric(series, errors='coerce')
    except:
        return series


# Load CSV safely or generate sample data
@st.cache_data(ttl=5)
def load_data(file_path):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            st.warning(f"File not found: {file_path}")
            return generate_sample_data()

        # Try to read the CSV
        df = pd.read_csv(file_path, on_bad_lines='skip')

        # Check if we have the expected columns
        expected_cols = ["timestamp", "machine_id", "temperature", "vibration", "pressure",
                         "run_hours", "rul_hours", "predicted_failure_date"]

        missing_cols = [col for col in expected_cols if col not in df.columns]

        if missing_cols:
            st.warning(f"CSV is missing expected columns: {', '.join(missing_cols)}")
            st.info("Please check your CSV format or use the sample data generator below.")
            return generate_sample_data()

        return df

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return generate_sample_data()


# Auto-refresh every 5 seconds
refresh_interval = 5  # seconds
if time.time() - st.session_state.last_refresh > refresh_interval:
    st.session_state.last_refresh = time.time()
    st.session_state.df = None  # Clear cached data to force reload
    st.rerun()

# Load data
if st.session_state.df is None:
    st.session_state.df = load_data(LOG_FILE)

df = st.session_state.df

if df.empty:
    st.warning("Data is empty. Generating sample data...")
    df = generate_sample_data()
    st.session_state.df = df

# Convert timestamp to datetime for better handling with error tolerance
if 'timestamp' in df.columns:
    df['timestamp'] = safe_datetime_conversion(df['timestamp'])
if 'predicted_failure_date' in df.columns:
    df['predicted_failure_date'] = safe_datetime_conversion(df['predicted_failure_date'])

# Convert numeric columns to proper numeric types
numeric_columns = ['temperature', 'vibration', 'pressure', 'run_hours', 'rul_hours']
for col in numeric_columns:
    if col in df.columns:
        df[col] = safe_numeric_conversion(df[col])

# Show data info
st.sidebar.subheader("Data Information")
st.sidebar.write(f"Total records: {len(df)}")
if 'machine_id' in df.columns:
    st.sidebar.write(f"Machines: {df['machine_id'].nunique()}")
if 'timestamp' in df.columns:
    valid_timestamps = df['timestamp'].notna()
    if valid_timestamps.any():
        st.sidebar.write(
            f"Time range: {df.loc[valid_timestamps, 'timestamp'].min()} to {df.loc[valid_timestamps, 'timestamp'].max()}")
    else:
        st.sidebar.write("No valid timestamps found")

# Show data types for debugging
st.sidebar.subheader("Data Types")
for col in df.columns:
    st.sidebar.write(f"{col}: {df[col].dtype}")

# Show latest machine status
st.subheader("Latest Machine Status")
if 'timestamp' in df.columns and 'machine_id' in df.columns:
    latest_data = df.sort_values('timestamp').groupby("machine_id").last().reset_index()
    st.dataframe(latest_data)
else:
    st.warning("Missing timestamp or machine_id columns")

# Highlight machines near failure (RUL < 48 hours)
if 'rul_hours' in df.columns:
    # Ensure rul_hours is numeric
    latest_data['rul_hours'] = safe_numeric_conversion(latest_data['rul_hours'])

    # Check if we have valid numeric data
    if pd.api.types.is_numeric_dtype(latest_data['rul_hours']):
        critical = latest_data[latest_data["rul_hours"] < 48]

        if not critical.empty:
            st.error(f"⚠️ Machines Near Failure! {len(critical)} machine(s) require urgent attention.")
            # Filter out non-numeric rows for display
            display_cols = ["machine_id", "temperature", "vibration", "pressure",
                            "run_hours", "rul_hours", "predicted_failure_date"]
            display_cols = [col for col in display_cols if col in critical.columns]
            st.dataframe(critical[display_cols])
        else:
            st.success("✅ All machines operating normally.")
    else:
        st.warning("RUL data contains non-numeric values that cannot be compared")
        st.write("Sample RUL values:", latest_data["rul_hours"].head().tolist())
else:
    st.warning("RUL data not available")

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["Sensor Trends", "RUL Trends", "Failure Predictions"])

with tab1:
    st.subheader("Sensor Trends")

    if all(col in df.columns for col in ["timestamp", "machine_id"]):
        sensor_cols = [col for col in ["temperature", "vibration", "pressure"] if col in df.columns]

        if sensor_cols:
            sensor_option = st.selectbox("Select Sensor", sensor_cols, key="sensor_select")
            # Ensure the selected sensor column is numeric
            df[sensor_option] = safe_numeric_conversion(df[sensor_option])

            if pd.api.types.is_numeric_dtype(df[sensor_option]):
                pivot_data = df.pivot(index="timestamp", columns="machine_id", values=sensor_option)
                st.line_chart(pivot_data)
            else:
                st.warning(f"Selected sensor data ({sensor_option}) contains non-numeric values")
        else:
            st.warning("No sensor data available")
    else:
        st.warning("Missing required columns for sensor trends")

with tab2:
    if 'rul_hours' in df.columns:
        st.subheader("Remaining Useful Life (RUL) Trend")

        if all(col in df.columns for col in ["timestamp", "machine_id", "rul_hours"]):
            # Ensure rul_hours is numeric
            df['rul_hours'] = safe_numeric_conversion(df['rul_hours'])

            if pd.api.types.is_numeric_dtype(df['rul_hours']):
                rul_pivot = df.pivot(index="timestamp", columns="machine_id", values="rul_hours")
                st.line_chart(rul_pivot)

                # Show RUL summary statistics
                st.subheader("RUL Summary")
                rul_stats = latest_data["rul_hours"].describe()
                st.write(rul_stats)
            else:
                st.warning("RUL data contains non-numeric values")
        else:
            st.warning("Missing required columns for RUL trends")
    else:
        st.warning("RUL data not available")

with tab3:
    st.subheader("Predicted Failure Information")

    if 'predicted_failure_date' in df.columns:
        failure_dates = latest_data[["machine_id", "predicted_failure_date"]].copy()
        failure_dates["predicted_failure_date"] = safe_datetime_conversion(failure_dates["predicted_failure_date"])
        st.dataframe(failure_dates)

        # Calculate days until failure
        if pd.api.types.is_datetime64_any_dtype(failure_dates["predicted_failure_date"]):
            failure_dates["days_until_failure"] = (failure_dates["predicted_failure_date"] - pd.Timestamp.now()).dt.days
            st.subheader("Days Until Failure")
            st.dataframe(failure_dates[["machine_id", "days_until_failure"]])
        else:
            st.warning("Predicted failure dates are not in valid datetime format")
    else:
        st.warning("Predicted failure date data not available")

# Data management section
st.sidebar.subheader("Data Management")
if st.sidebar.button("Generate Sample Data"):
    st.session_state.df = generate_sample_data()
    st.rerun()

if st.sidebar.button("Download Sample CSV Template"):
    sample_df = generate_sample_data()
    csv = sample_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV Template",
        data=csv,
        file_name="sensor_logs_template.csv",
        mime="text/csv"
    )

# Add manual refresh button
if st.button("Refresh Data"):
    st.session_state.df = None
    st.rerun()

# Display last update time
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")