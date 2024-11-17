import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

gbr_pipeline = joblib.load('gbr_pipeline.pkl')
workingday_counts = pd.read_csv('workingday_counts_with_weekday.csv')
non_workingday_counts = pd.read_csv('non_workingday_counts_with_weekday.csv')

workingday_counts_dict = workingday_counts.set_index(['mnth', 'weekday', 'hr'])['cnt'].to_dict()
non_workingday_counts_dict = non_workingday_counts.set_index(['mnth', 'weekday', 'hr'])['cnt'].to_dict()

def calculate_features(df, workingday_counts, non_workingday_counts):
    df['yr'] = df['yr'].map({0: 0, 1: 1, 2: 2})
    
    def map_hourly_avg(row):
        if row['workingday'] == 0 and row['weekday'] in [1, 2, 3, 4, 5]:
            return non_workingday_counts.get((row['mnth'], 6, row['hr']), 0)
        elif row['workingday'] == 1:
            return workingday_counts.get((row['mnth'], row['weekday'], row['hr']), 0)
        else:
            return non_workingday_counts.get((row['mnth'], row['weekday'], row['hr']), 0)
    
    df['hourly_avg_workingday'] = df.apply(lambda row: map_hourly_avg(row) if row['workingday'] == 1 else 0, axis=1)
    df['hourly_avg_nonworkingday'] = df.apply(lambda row: map_hourly_avg(row) if row['workingday'] == 0 else 0, axis=1)
    return df[['yr', 'mnth', 'hum', 'hourly_avg_workingday', 'hourly_avg_nonworkingday', 'temp_expected_1', 'weathersit']]

def bike_usage_simulation():
    st.title('🚴‍♂️ Bike Usage Prediction')

    st.markdown("""
    <hr style="border:1px solid #d4d4d4; margin: 20px 0;">
    """, unsafe_allow_html=True)

    st.header('Input Parameters')
    st.markdown("Please fill in the input parameters below to predict bike usage.")

    col1, col2, col3 = st.columns(3)

    with col1:
        temp_expected_1 = st.number_input('Temperature (°C)', min_value=-20, max_value=50, value=20)
        weekday = st.selectbox('Weekday (0: Sunday, 6: Saturday)', options=[i for i in range(7)], format_func=lambda x: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][x])
        hum = st.number_input('Humidity (%)', min_value=0, max_value=100, value=50)

    with col2:
        mnth = st.selectbox('Month', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], format_func=lambda x: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][x - 1])
        hr = st.selectbox('Hour of the Day', options=[i for i in range(24)], format_func=lambda x: f"{x}:00")
        weathersit = st.selectbox('Weather Situation', options=[1, 2, 3, 4], format_func=lambda x: ['Clear', 'Cloudy', 'Light Rain/Snow', 'Heavy Rain/Snow'][x - 1])

    with col3:
        workingday_options = [0, 1]
        if weekday in [0, 6]:
            workingday_options = [0]
        workingday = st.selectbox('Is it a Working Day?', options=workingday_options, format_func=lambda x: 'Yes' if x == 1 else 'No')

    year = 1

    base_input_data = pd.DataFrame({
        'temp_expected_1': [temp_expected_1],
        'mnth': [mnth],
        'workingday': [workingday],
        'hum': [hum],
        'weathersit': [weathersit],
        'yr': [year],
        'weekday': [weekday],
    })

    hourly_predictions = []
    for hour in range(24):
        input_data = base_input_data.copy()
        input_data['hr'] = hour
        input_data = calculate_features(input_data, workingday_counts_dict, non_workingday_counts_dict)
        input_data.columns = input_data.columns.str.lower()
        prediction = gbr_pipeline.predict(input_data)[0]
        clipped_prediction = max(0, prediction)
        hourly_predictions.append(clipped_prediction)

    selected_hour_prediction = int(round(hourly_predictions[hr]))
    min_prediction = int(round(min(hourly_predictions)))
    max_prediction = int(round(max(hourly_predictions)))

    st.markdown("""
    <hr style="border:1px solid #d4d4d4; margin: 20px 0;">
    """, unsafe_allow_html=True)

    st.subheader('🔍 Prediction for Selected Hour')
    st.write(f"*Predicted bike usage for {hr}:00 is {selected_hour_prediction} bikes.*")

    st.subheader('📊 Daily Prediction Summary')
    st.write(f"- *Minimum predicted bike usage for the day*: {min_prediction} bikes.")
    st.write(f"- *Maximum predicted bike usage for the day*: {max_prediction} bikes.")

    st.subheader('⏰ Predictions for Each Hour of the Day')

    hourly_df = pd.DataFrame({
        'Hour': list(range(24)),
        'Predicted Count': [int(round(pred)) for pred in hourly_predictions],
    })

    hourly_df['Color'] = ['Selected Hour' if h == hr else 'Other Hours' for h in hourly_df['Hour']]

    fig = px.bar(
        hourly_df,
        x='Hour',
        y='Predicted Count',
        color='Color',
        color_discrete_map={'Selected Hour': 'red', 'Other Hours': 'blue'},
        title='Hourly Predictions',
        labels={'Hour': 'Hour of the Day', 'Predicted Count': 'Number of Bikes'}
    )

    st.plotly_chart(fig)






