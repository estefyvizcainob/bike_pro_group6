import streamlit as st
import pandas as pd

# Function definition for the data cleaning page
def data_cleaning_page():
    st.markdown(
        """
        <style>
        .section-header {
            font-size: 2rem;
            font-weight: bold;
            color: #000; /* Changed to black */
            padding-bottom: 10px;
            border-bottom: 2px solid #ccc;
            margin-bottom: 20px;
        }
        .expander-title {
            font-weight: bold;
            font-size: 1.2rem;
        }
        .markdown-text {
            color: #555;
            font-size: 1.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Main Section Header
    st.markdown("<div class='section-header'>✨ Comprehensive Data Cleaning and Quality Check</div>", unsafe_allow_html=True)
    st.write("Explore this section to understand the steps taken for data quality assurance, visualization, and preparation for analysis.")

    # Step 1: Load the Data
    data = pd.read_csv('hour.csv')
    st.write("We have loaded the dataset to understand its structure and assess data quality.")

    # Step 2: Initial Data Overview
    with st.expander("📊 Initial Data Overview"):
        st.markdown("<div class='expander-title'>Initial Data Overview</div>", unsafe_allow_html=True)
        st.write("We review the initial dataset to understand its columns and types.")
        st.dataframe(data.head())

    # Step 3: Data Quality Assessment
    with st.expander("🔍 Data Quality Assessment"):
        st.markdown("<div class='expander-title'>Data Quality Assessment</div>", unsafe_allow_html=True)
        st.write("### Data Structure")
        st.write("All features are correctly typed as `int64` or `float64`, with the exception of the `dteday` column, which holds date information.")
        st.write("### Missing Values")
        st.write("No missing values were found in the dataset, ensuring high data quality.")

    # Step 4: Handling Outliers
    with st.expander("⚠️ Handling Outliers and Ensuring Integrity"):
        st.markdown("<div class='expander-title'>Handling Outliers and Ensuring Integrity</div>", unsafe_allow_html=True)
        st.write("We analyze the data for any outliers using visual methods to ensure they don't skew our analysis.")
        st.write("We verified the data for outliers using visual methods like box plots and found no extreme values that would skew our analysis.")

    # Step 5: Verifying Quarter Behavior
    with st.expander("📅 Verifying Quarter Behavior"):
        st.markdown("<div class='expander-title'>Verifying Quarter Behavior</div>", unsafe_allow_html=True)
        st.write("""
        We check if the dataset correctly represents data across quarters, which is important for understanding patterns in bike rentals.
        The dataset is divided by quarters of the year (1: Q1, 2: Q2, 3: Q3, 4: Q4). To validate this, we verified the actual start and end dates for each quarter.
        """)
        quarter_data = pd.DataFrame({
            'quarter': [1, 2, 3, 4],
            'min_day': ['2011-01-01', '2011-04-01', '2011-07-01', '2011-10-01'],
            'max_day': ['2011-03-31', '2011-06-30', '2011-09-30', '2011-12-31']
        })
        st.table(quarter_data)

    # Step 6: Checking for Missing Data in Time Series
    with st.expander("⏰ Checking for Missing Data in Time Series"):
        st.markdown("<div class='expander-title'>Checking for Missing Data in Time Series</div>", unsafe_allow_html=True)
        st.write("""
        Ensuring the time series data has no missing entries is vital for accurate analysis.
        We found some specific date-hour combinations missing from the dataset, which can affect our understanding of bike usage trends.
        """)
        missing_date_hours = pd.DataFrame({
            'dteday': ['2011-01-02', '2011-01-03', '2011-01-03', '2011-01-04', '2011-01-05',
                       '2012-10-30', '2012-11-08', '2012-11-29', '2012-12-24', '2012-12-25'],
            'hr': [5, 2, 3, 3, 3, 12, 3, 3, 4, 3]
        })
        st.table(missing_date_hours)



