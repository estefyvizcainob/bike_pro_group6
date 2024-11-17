import streamlit as st
import pandas as pd
from PIL import Image

def ml_model_page():
    st.title("🚴 Comprehensive Machine Learning Model Creation")

    # Introduction
    st.write("""
    This section explains the creation of a predictive model for estimating the total number of bike users on an hourly basis.
    Below, we outline the steps involved in preparing the data, building the model, and evaluating its performance.
    """)

    # Adjusted R² Introduction
    st.markdown("## 📊 Model Overview: Adjusted R² Metric")
    st.write("""
    The Adjusted R² metric is a refined version of the R² metric that takes into account the number of predictors in the model. 
    It provides a more accurate measure of how well the model generalizes to new data by penalizing the addition of irrelevant features. 
    An Adjusted R² value close to 1 indicates that the model explains a large proportion of the variance in the target variable while considering model complexity.
    """)

    st.markdown("""
    ### Model's Adjusted R² Performance:
    - **Training Data Adjusted R²**: 0.9656 (Gradient Boosting Regressor)
    - **Test Data Adjusted R²**: 0.9488 (Gradient Boosting Regressor)
    """)

    # Separation line with a prompt
    st.write("---")

    # Comparison Table of Adjusted R² for Models
    st.subheader("📊 Comparison of Adjusted R² Across Models")
    st.write("Below is a comparison of the Adjusted R² metric for the Gradient Boosting and Extra Trees Regressor models:")
    comparison_dict = {
        'Model': ['Gradient Boosting Regressor', 'Extra Trees Regressor'],
        'Adjusted R² (Train)': [0.9656, 0.9653],
        'Adjusted R² (Test)': [0.9488, 0.9413]
    }
    comparison_df = pd.DataFrame(comparison_dict)
    st.table(comparison_df)
    st.write("**Note**: While both models show strong performance on training data, the test data metrics indicate potential overfitting in the Extra Trees Regressor, where the model might have learned specific patterns that do not generalize well.")

    # Data Overview
    st.subheader("🔍 Data Overview")
    st.write("The initial dataset was reviewed to identify key features relevant to the analysis.")

    # Feature Selection as a dropdown
    with st.expander("🔧 Feature Selection - Recursive Feature Elimination with Cross-Validation"):
        st.write("""
        We'll start with a shortlist of features that we are interested in using for the model. 
        We dropped certain columns from the dataset due to their redundancy or irrelevance based on the analysis. These include:
        
        - **temp & atemp**: We created lagged versions, so the original columns were removed.
        - **dteday**: Not required as this is not a time series model.
        - **instant**: Used as an index and irrelevant for prediction.
        - **registered & casual**: Directly derived from 'cnt', so not needed.
        - **season**: Dropped due to collinearity with 'mnth'.
        - **hr**: Replaced with hourly averages.
        - **workingday & weekday**: Replaced with hourly averages for working and non-working days.
        - **windspeed & windspeed_binned**: Low correlation with 'cnt', hence dropped.
        """)
        rfe_image = Image.open("rfe.png")
        st.image(rfe_image, caption="RFE Performance vs. Number of Features", use_column_width=True)

        st.write("""
        The process showed an optimal performance increase with 8 selected features:
        - **yr, mnth, weathersit, hum, hourly_avg_workingday, hourly_avg_nonworkingday, temp_expected_1, dry_precip**.
        We opted to drop 'rain_intensity' due to higher correlation with 'weathersit'.
        """)

    # Model Training and Hyperparameter Tuning (shown directly)
    st.subheader("📈 Model Training and Tuning")
    st.write("""
    The model of choice was the Gradient Boosting Regressor, known for its strong predictive capabilities.
    Hyperparameter tuning was performed using RandomizedSearchCV to find the optimal configuration.
    """)

    # Train-Test Split and Pipeline (shown directly)
    st.subheader("🛠️ Train-Test Split and Pipeline")
    st.write("The data was split into training and testing sets, and the model was trained within a pipeline.")

    # Model Performance Metrics
    st.subheader("🏆 Model Performance Metrics")
    st.write("""
    Below are the performance metrics of the Gradient Boosting Regressor model, showcasing its accuracy and predictive capabilities. These metrics are critical for understanding the quality of the model.
    """)

    # Gradient Boosting Metrics Table
    gb_results_dict = {
        'Metric': ['MAE', 'MSE', 'RMSE', 'R2', 'Adjusted R2'],
        'Train': [21.91, 1140.16, 33.77, 0.9656, 0.9656],
        'Test': [25.39, 1617.21, 40.21, 0.9489, 0.9488]
    }
    gb_results_df = pd.DataFrame(gb_results_dict)
    st.table(gb_results_df)

    st.write("The model's performance indicates high accuracy, with a strong Adjusted R² and relatively low errors, showing it is well-suited for predicting the number of bike users.")

    # Predicted vs Actual Values (shown directly)
    st.subheader("🔬 Predicted vs Actual Values - Gradient Boosting Regressor")
    col1, col2 = st.columns(2)
    with col1:
        gb_pred_act_train_image = Image.open("pred_act_train.png")
        st.image(gb_pred_act_train_image, caption="Predicted vs Actual Values (Training Data)", use_column_width=True)
    with col2:
        gb_pred_act_test_image = Image.open("pred_act_test.png")
        st.image(gb_pred_act_test_image, caption="Predicted vs Actual Values (Test Data)", use_column_width=True)

    # Residuals Analysis as a dropdown
    with st.expander("📉 Residuals Analysis - Gradient Boosting"):
        st.write("""
        Residual analysis is crucial for evaluating how well the model's predictions align with the actual data. 
        Ideally, residuals should be randomly scattered around zero with no clear pattern, indicating that the model's predictions are unbiased and that it has captured the underlying structure of the data.
        """)
        col3, col4 = st.columns(2)
        with col3:
            gb_res_train_image = Image.open("res_test.png")
            st.image(gb_res_train_image, caption="Residuals vs Predicted Values (Training Data)", use_column_width=True)
        with col4:
            gb_res_test_image = Image.open("res_test2.png")
            st.image(gb_res_test_image, caption="Residuals vs Predicted Values (Test Data)", use_column_width=True)

    # Residual Distribution Analysis as a dropdown
    with st.expander("📊 Residual Distribution Analysis - Gradient Boosting"):
        st.write("""
        To further understand how well the residuals are distributed, we plotted the distribution for both training and test data. 
        A normal distribution centered around zero with most residuals close to zero indicates a good model fit.
        """)
        col5, col6 = st.columns(2)
        with col5:
            gb_res_dist_train_image = Image.open("red_dis_training.png")
            st.image(gb_res_dist_train_image, caption="Residual Distribution (Training Data)", use_column_width=True)
        with col6:
            gb_res_dist_test_image = Image.open("red_dist_test.png")
            st.image(gb_res_dist_test_image, caption="Residual Distribution (Test Data)", use_column_width=True)

    # Extra Trees Regressor Section
    st.header("🌳 Extra Trees Regressor: Model Training and Tuning")
    st.write("""
    The **Extra Trees Regressor** was also trained and tuned using `RandomizedSearchCV` with hyperparameter optimization.
    """)

    # Displaying Metrics for Extra Trees Regressor
    st.subheader("📋 Extra Trees Performance Metrics")
    etr_results_dict = {
        'Metric': ['MAE', 'MSE', 'RMSE', 'R2', 'Adjusted R2'],
        'Train': [22.50, 1152.22, 33.94, 0.9653, 0.9653],
        'Test': [28.59, 1854.26, 43.06, 0.9414, 0.9413]
    }
    etr_results_df = pd.DataFrame(etr_results_dict)
    st.table(etr_results_df)
    st.write("**Note**: The Extra Trees Regressor shows slightly lower performance on test data compared to training data, indicating potential overfitting. This can happen when the model captures specific patterns in the training data that do not generalize well.")

    # Predicted vs Actual Values - Extra Trees Regressor
    st.subheader("🔬 Predicted vs Actual Values - Extra Trees Regressor")
    col7, col8 = st.columns(2)
    with col7:
        etr_pred_act_train_image = Image.open("extra_tree_pred_actual_train.png")
        st.image(etr_pred_act_train_image, caption="Predicted vs Actual Values (Training Data)", use_column_width=True)
    with col8:
        etr_pred_act_test_image = Image.open("extra_tree_pred_act_test.png")
        st.image(etr_pred_act_test_image, caption="Predicted vs Actual Values (Test Data)", use_column_width=True)

    # Residuals Analysis - Extra Trees
    with st.expander("📉 Residuals Analysis - Extra Trees"):
        st.write("""
        As expected, there is no even distribution around 0, as there are underpredictions for higher values and overpredictions for lower values.
        """)
        col9, col10 = st.columns(2)
        with col9:
            etr_res_train_image = Image.open("extra_tree_resd_train.png")
            st.image(etr_res_train_image, caption="Residuals vs Predicted Values (Training Data)", use_column_width=True)
        with col10:
            etr_res_test_image = Image.open("extra_tree_resd_test.png")
            st.image(etr_res_test_image, caption="Residuals vs Predicted Values (Test Data)", use_column_width=True)

    # Residual Distribution Analysis - Extra Trees
    with st.expander("📊 Residual Distribution Analysis - Extra Trees"):
        st.write("""
        This shows that our model in general is slightly biased towards overpredictions as the the distribution seems to be skewed left from the mean. The reason why average residuals are still close to 0 is likely due to the fact that, as mentioned earlier, the model underpredicts for higher values which affects the average residuals, this can be seen on this graph as well.
        """)
        col11, col12 = st.columns(2)
        with col11:
            etr_res_dist_train_image = Image.open("extra_tree_dist_train.png")
            st.image(etr_res_dist_train_image, caption="Residual Distribution (Training Data)", use_column_width=True)
        with col12:
            etr_res_dist_test_image = Image.open("extra_tree_dist_test.png")
            st.image(etr_res_dist_test_image, caption="Residual Distribution (Test Data)", use_column_width=True)


# Call the function in your main app
if __name__ == "__main__":
    ml_model_page()


