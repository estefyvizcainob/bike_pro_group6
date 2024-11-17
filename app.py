import streamlit as st
from team_intro import introduction_page  # Import for the 'Introduction and Summary' page
from data_cleaning import data_cleaning_page  # Import for the 'Data Cleaning' page
from eda import eda_page  # Import for the 'Exploratory Data Analysis' page
from ml_model import ml_model_page  # Import for the 'ML Model Creation' page
from business_insights import business_insights_page  # Import for the 'Business Insights' page
from simulation import bike_usage_simulation  # Import the 'Simulation' page function

# Main app function
def main():
    st.sidebar.title("Menu")
    selection = st.sidebar.radio(
        "Choose a page:",
        ["Introduction and Summary", "Data Cleaning", "Exploratory Data Analysis",
         "ML Model Creation", "Business Insights", "Simulation"]
    )

    # Page selection logic
    if selection == "Introduction and Summary":
        introduction_page()
    elif selection == "Data Cleaning":
        data_cleaning_page()
    elif selection == "Exploratory Data Analysis":
        eda_page()
    elif selection == "ML Model Creation":
        ml_model_page()
    elif selection == "Business Insights":
        business_insights_page()
    elif selection == "Simulation":
        bike_usage_simulation()  # Calls the simulation page from simulation.py

if __name__ == "__main__":
    main()
