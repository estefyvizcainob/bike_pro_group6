import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Load the machine learning pipeline (already saved)
gbr_pipeline = joblib.load('gbr_pipeline.pkl')

# Load embedded CSV data
workingday_counts = pd.read_csv('workingday_counts_with_weekday.csv')
non_workingday_counts = pd.read_csv('non_workingday_counts_with_weekday.csv')

# Convert them to dictionaries for easier access
workingday_counts_dict = workingday_counts.set_index(['mnth', 'weekday', 'hr'])['cnt'].to_dict()
non_workingday_counts_dict = non_workingday_counts.set_index(['mnth', 'weekday', 'hr'])['cnt'].to_dict()

# Function to calculate the features
def calculate_features(df, workingday_counts, non_workingday_counts):
    # Map 'yr' based on the user input (0 = 2011, 1 = 2012, 2 = 2013)
    df['yr'] = df['yr'].map({0: 0, 1: 1, 2: 2})

    # 'dry_precip' feature
    df['dry_precip'] = df['weathersit'].apply(lambda x: 1 if x in [1, 2] else 2)

    # Hourly avg workingday and non-workingday calculation
    def map_hourly_avg(row):
        # Check if it's a non-working day (weekdays 1 to 5) and use Saturday's (weekday == 6) data
        if row['workingday'] == 0 and row['weekday'] in [1, 2, 3, 4, 5]:
            return non_workingday_counts.get((row['mnth'], 6, row['hr']), 0)  # Use Saturday's data for weekdays 1-5
        elif row['workingday'] == 1:
            return workingday_counts.get((row['mnth'], row['weekday'], row['hr']), 0)
        else:
            return non_workingday_counts.get((row['mnth'], row['weekday'], row['hr']), 0)

    # Apply the feature calculation
    df['hourly_avg_workingday'] = df.apply(lambda row: map_hourly_avg(row) if row['workingday'] == 1 else 0, axis=1)
    df['hourly_avg_nonworkingday'] = df.apply(lambda row: map_hourly_avg(row) if row['workingday'] == 0 else 0, axis=1)

    # Prepare the final features for prediction
    return df[['yr', 'mnth', 'hum', 'hourly_avg_workingday', 'hourly_avg_nonworkingday', 'temp_expected_1', 'dry_precip']]

# Streamlit interface
st.title('Bike Usage Prediction')

# Input form for users
st.sidebar.header('Input Parameters')
temp_expected_1 = st.sidebar.number_input('Temperature expected for the next hour', min_value=-20, max_value=50, value=20)
mnth = st.sidebar.selectbox('Month', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], index=0)
hr = st.sidebar.selectbox('Hour', options=[i for i in range(24)], index=0)
weekday = st.sidebar.selectbox('Weekday (0: Sunday, 6: Saturday)', options=[i for i in range(7)], index=0)  # Weekday input (0=Sunday, 6=Saturday)

# Restrict workingday selection based on weekday input
workingday_options = [0, 1]  # Default options for workingday
if weekday == 0 or weekday == 6:  # If Sunday or Saturday, set workingday to 0 (non-working day)
    workingday_options = [0]  # Only allow non-working day

workingday = st.sidebar.selectbox('Working Day', options=workingday_options, index=0)  # 1 for working day, 0 for non-working day
hum = st.sidebar.number_input('Humidity', min_value=0, max_value=100, value=50)
weathersit = st.sidebar.selectbox('Weather Situation', options=[1, 2, 3, 4], index=0)  # 1: Clear, 2: Cloudy, 3: Rain, 4: Snow (or other)
year = st.sidebar.selectbox('Year', options=[0, 1, 2], index=2)  # 0 = 2011, 1 = 2012, 2 = 2013

# Create the base input data
base_input_data = pd.DataFrame({
    'temp_expected_1': [temp_expected_1],
    'mnth': [mnth],
    'workingday': [workingday],
    'hum': [hum],
    'weathersit': [weathersit],
    'yr': [year],
    'weekday': [weekday],  # Include weekday in the input data
})

# Calculate hourly predictions for the selected day
hourly_predictions = []
for hour in range(24):
    input_data = base_input_data.copy()
    input_data['hr'] = hour
    input_data = calculate_features(input_data, workingday_counts_dict, non_workingday_counts_dict)
    input_data.columns = input_data.columns.str.lower()
    
    # Generate prediction and apply clipping
    prediction = gbr_pipeline.predict(input_data)[0]
    clipped_prediction = max(0, prediction)  # Ensure non-negative predictions
    hourly_predictions.append(clipped_prediction)

# Highlight the selected hour
selected_hour_prediction = int(round(hourly_predictions[hr]))

# Calculate min and max predictions for the day
min_prediction = int(round(min(hourly_predictions)))
max_prediction = int(round(max(hourly_predictions)))

# Displaying results
st.subheader('Prediction for Selected Hour')
st.write(f"Predicted bike usage for {hr}:00 is {selected_hour_prediction} bikes.")

# Displaying min and max predictions
st.subheader('Daily Prediction Summary')
st.write(f"Minimum predicted bike usage for the day: {min_prediction} bikes.")
st.write(f"Maximum predicted bike usage for the day: {max_prediction} bikes.")

# Create a DataFrame for Plotly
hourly_df = pd.DataFrame({
    'Hour': list(range(24)),
    'Predicted Count': [int(round(pred)) for pred in hourly_predictions],
})

# Assign a color to the selected hour for better visualization
hourly_df['Color'] = ['Selected Hour' if h == hr else 'Other Hours' for h in hourly_df['Hour']]

# Plot with Plotly Express
st.subheader('Predictions for Each Hour of the Day')

fig = px.bar(
    hourly_df,
    x='Hour',
    y='Predicted Count',
    color='Color',
    color_discrete_map={'Selected Hour': 'red', 'Other Hours': 'blue'},
    title='Hourly Predictions'
)

# Display the Plot
st.plotly_chart(fig)