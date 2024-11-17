import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def eda_page():
    # Load data
    data = pd.read_csv('hour.csv')

    st.title("✨ Comprehensive Exploratory Data Analysis")
    st.markdown("---")
    st.markdown("<p>In this section, we will explore the dataset to understand the patterns, relationships, and insights within the data.</p>", unsafe_allow_html=True)

    # Highlighting Final Features
    st.markdown("""
    <div style="background-color:#e8f5e9; padding: 10px; border-radius: 5px;">
    <h3>✨ Final Selected Features for Modeling</h3>
    <p>After extensive EDA, the following features were selected for modeling:</p>
    <ul>
        <li><code>yr</code>: The year, indicating a change over time.</li>
        <li><code>mnth</code>: The month, capturing seasonal variations.</li>
        <li><code>weathersit</code>: The weather situation, grouped to identify the impact of weather on bike rentals.</li>
        <li><code>hum</code>: The humidity level, included for its impact on outdoor activities.</li>
        <li><code>hourly_avg_workingday</code>: Average rental count per hour on working days.</li>
        <li><code>hourly_avg_nonworkingday</code>: Average rental count per hour on non-working days.</li>
        <li><code>temp_expected_1</code>: 1-hour lagged temperature to capture the immediate effect of temperature on rentals.</li>
    </ul>
    <p>These features were chosen based on their correlation with the target variable and practical significance in predictive modeling.</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. General Overview
    st.header("📊 General Overview")
    
    # Denormalizing Data Section
    with st.expander("Denormalizing Data for Clarity"):
        st.subheader("Denormalizing Data for Clarity")
        st.markdown("""
        The following features were denormalized to their original scale for easier interpretation:
        - `temp` was multiplied by 41
        - `atemp` was multiplied by 50
        - `hum` was multiplied by 100
        - `windspeed` was multiplied by 67
        """, unsafe_allow_html=True)

    # Distribution of Target Variable
    with st.expander("Distribution of Target Variable (Count of Bikes)"):
        st.subheader("Distribution of Target Variable (Count of Bikes)")
        st.markdown("""
        <p>The <code>cnt</code> column represents the total count of bike rentals per hour. Analyzing its distribution provides insights into typical rental volumes and helps identify potential skewness in the data.</p>
        
        **Implications:**
        - Highlights periods of high and low demand.
        - Informs data transformations that may be needed for modeling.
        """, unsafe_allow_html=True)

        plt.figure(figsize=(10, 6))
        sns.histplot(data['cnt'], bins=100, kde=True)
        plt.title('Distribution of Bike Counts (cnt)')
        plt.xlabel('Bike Count')
        plt.ylabel('Frequency')
        st.pyplot(plt)

    # Instances where Count <= 5 Analysis
    with st.expander("Instances with Very Low Count (<= 5)"):
        st.subheader("Instances where Count <= 5 Analysis")
        st.markdown("""
        <p>This analysis highlights the distribution and frequency of instances with very low bike rental counts to uncover patterns related to specific hours or conditions.</p>
        
        **Observations:**
        - Large spikes in lower counts may indicate specific conditions or times leading to low rentals.
        """, unsafe_allow_html=True)

        filtered_data = data[data['cnt'] <= 5]
        freq = filtered_data.groupby(['hr', 'mnth']).size().reset_index(name='frequency')
        filtered_data = filtered_data.merge(freq, on=['hr', 'mnth'], how='left')

        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='hr', y='mnth', data=filtered_data, hue='frequency', palette='viridis', size='frequency', sizes=(20, 200))
        plt.title('Instances where Count <= 5')
        plt.xlabel('Hour')
        plt.ylabel('Month')
        plt.legend(title='Frequency', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        
        st.write("Low count values are observed across all months and are more frequent during nighttime hours.")


    with st.expander("Analysis of Hours with Count <= 5"):
        st.subheader("🕵️‍♂️ Analysis of Hours with Count <= 5")
        st.markdown("""
        This section breaks down the frequency of bike rentals when the count is 5 or less, observed across different months.
        
        **Key Observations:**
        - The highest frequency of hours with low counts is typically around 3 and 4 in the morning.
        - Colder months show a higher occurrence of low rental counts.
        """)
        
        # Display the image for low counts
        st.image("distribution_hour_minus5.png", caption="Distribution of Hours when Count <= 5 Monthly")

        # Final statement for this section
        st.write("These insights will guide feature engineering and model preparation, ensuring that the influence of low rental counts is adequately accounted for.")


        # Expander for Relations Between Features and Target
    with st.expander("Relation Between Hour (hr) and Count (cnt)"):
        st.subheader("Relation Between Features and Target")
        st.markdown("""
        <p>This boxplot shows how bike rental counts vary throughout the day, helping identify peak and low-demand hours.</p>
        
        **Key Findings:**
        - Peak hours are observed during typical commute times (morning and evening rush hours).
        - This insight could guide the development of new features that capture these rush hour patterns.
        """, unsafe_allow_html=True)

        # Display the saved image for this analysis
        st.image("features_targer_relat.png", caption="Hour (hr) vs. Count (cnt)", use_column_width=True)
        st.write("The plot highlights the morning and evening rush hours as peak times for bike rentals, indicating a potential feature for model optimization.")

         # Expander for Deep Dive into Weekly Patterns
    with st.expander("Average Count by Hour for Each Weekday"):
        st.subheader("Average Count by Hour for Each Weekday")
        st.markdown("""
        This visualization breaks down the average bike count for each hour, analyzed by the day of the week. This helps identify weekday versus weekend patterns.
        """)
        st.image('deep_weekeng_pattern.png', caption='Average Count by Hour for Each Weekday')
        st.write("""
        **Analysis**:
        - Weekdays (Monday to Friday) follow a similar rental pattern, typically peaking during commute times.
        - Saturday and Sunday show different rental behaviors, with more balanced or shifted peak times.
        - These observations support the potential need for weekday-specific features to enhance model performance.
        """)
   



    #--------------------------------------------------

    # 2. Detailed Analysis by Areas
    st.header("🕰️ Detailed Analysis by Time")
    
    # Hourly Analysis on Working and Non-Working Days
    with st.expander("Hourly Analysis on Working and Non-Working Days"):
        st.subheader("Difference between Working and Non-Working Days")
        st.markdown("""
        <p>This section compares bike rental counts on working days versus non-working days to uncover patterns that could inform feature engineering.</p>
        
        **Observations:**
        - Different rental patterns are observed, with peaks at varying times on working versus non-working days.
        """, unsafe_allow_html=True)

        fig, ax = plt.subplots(1, 2, figsize=(16, 8))
        sns.boxplot(data=data[data['workingday'] == 1], x='hr', y='cnt', ax=ax[0], color="lightblue")
        ax[0].set_title("Count Distribution by Hour on Working Days")
        ax[0].set_xlabel("Hour")
        ax[0].set_ylabel("Count")
        sns.boxplot(data=data[data['workingday'] == 0], x='hr', y='cnt', ax=ax[1], color="orange")
        ax[1].set_title("Count Distribution by Hour on Non-Working Days")
        ax[1].set_xlabel("Hour")
        ax[1].set_ylabel("Count")
        plt.tight_layout()
        st.pyplot(fig)

    # Hourly Averages for Working and Non-Working Days
    with st.expander("Hourly Averages for Working and Non-Working Days"):
        st.subheader("Hourly Averages for Working and Non-Working Days")
        st.markdown("""
        This analysis calculates average bike counts per hour and month for both working and non-working days.
        
        **Insights:**
        - Consistent rental peaks during commute hours on working days.
        - More evenly distributed peaks on non-working days.
        """, unsafe_allow_html=True)

        workingday_counts = data[data['workingday'] == 1].groupby(['mnth', 'hr'])['cnt'].mean()
        non_workingday_counts = data[data['workingday'] == 0].groupby(['mnth', 'hr'])['cnt'].mean()

        def map_hourly_avg(row):
            if row['workingday'] == 1:
                return workingday_counts.get((row['mnth'], row['hr']), 0)
            else:
                return non_workingday_counts.get((row['mnth'], row['hr']), 0)

        data['hourly_avg_workingday'] = data.apply(lambda row: map_hourly_avg(row) if row['workingday'] == 1 else 0, axis=1)
        data['hourly_avg_nonworkingday'] = data.apply(lambda row: map_hourly_avg(row) if row['workingday'] == 0 else 0, axis=1)

        g = sns.FacetGrid(data[data['workingday'] == 1], col="mnth", col_wrap=4, height=4, aspect=1.5)
        g.map_dataframe(sns.barplot, x='hr', y='cnt', color='blue', alpha=0.6, label='Count (cnt)')
        g.map_dataframe(sns.lineplot, x='hr', y='hourly_avg_workingday', color='skyblue', linewidth=2, label='Hourly Avg (Working Day)')
        g.set_titles("Working Days - Month {col_name}")
        g.set_axis_labels("Hour", "Count")
        g.add_legend()
        plt.subplots_adjust(top=1)
        g.fig.suptitle("Hourly Count and Average on Working Days by Month")
        st.pyplot(g.fig)

        g = sns.FacetGrid(data[data['workingday'] == 0], col="mnth", col_wrap=4, height=4, aspect=1.5)
        g.map_dataframe(sns.barplot, x='hr', y='cnt', color='orange', alpha=0.6, label='Count (cnt)')
        g.map_dataframe(sns.lineplot, x='hr', y='hourly_avg_nonworkingday', color='peachpuff', linewidth=2, label='Hourly Avg (Non-Working Day)')
        g.set_titles("Non-Working Days - Month {col_name}")
        g.set_axis_labels("Hour", "Count")
        g.add_legend()
        plt.subplots_adjust(top=1)
        g.fig.suptitle("Hourly Count and Average on Non-Working Days by Month")
        st.pyplot(g.fig)

    # 3. Weather Analysis
    st.header("🌦️ Weather and Temperature Analysis")
    
    # Boxplot Analysis of Weather Variables and Count
    with st.expander("☁Relationship Between Weather Variables and Count"):
        st.subheader("Weather Impact on Bike Rentals")
        st.markdown("""
        This analysis shows how weather-related variables (temperature, humidity, apparent temperature, and windspeed) affect bike rentals.
        """)
    
        variables = ['temp', 'hum', 'atemp', 'windspeed']
        fig, axes = plt.subplots(2, 2, figsize=(16, 16))
        axes = axes.flatten()

        for i, var in enumerate(variables):
            sns.boxplot(data=data, x=var, y='cnt', ax=axes[i])
            x_axis_values = range(0, len(data[var].unique()), 5)
            axes[i].set_xticks(x_axis_values)
            axes[i].set_xticklabels([int(x) for x in axes[i].get_xticks()])
        plt.tight_layout()
        st.pyplot(fig)

        st.write("""
        **Key Insights:**
        - Bike counts generally increase with temperature but drop for extreme heat.
        - Humidity appears to have a negative impact on bike rentals, potentially due to rain or storms.
        """)

    # Expander for creating windspeed category
    with st.expander("Creating a Windspeed Category"):
        st.subheader("Categorizing Windspeed for Analysis")
        st.markdown("""
        To analyze the impact of windspeed on bike rentals, we categorized windspeed values into two main bins:
        - **Category 1**: Windspeed ≤ 40 (Regular conditions)
        - **Category 2**: Windspeed > 40 (High winds)

        This categorization helps identify whether higher winds significantly affect the rental counts compared to lower wind conditions.
        """, unsafe_allow_html=True)
    
                # Explanation for code logic
        st.write("""
        **Approach**:
        - We used `pd.cut()` to create the `windspeed_binned` feature, which segments the data based on the specified bins.
        - This method allows us to observe differences in bike rental patterns when windspeed surpasses the threshold of 40.
        """)

        # Expander for the windspeed binned analysis
    with st.expander("Effect of Windspeed_Binned on Count"):
        st.subheader("📊 Effect of Windspeed_Binned on Count")
        st.markdown("""
        This section examines the impact of categorized windspeed (binned) on bike rental counts.
        
        **Analysis:**
        - The plot below compares bike counts across two categories of windspeed.
        - It appears that there is no significant difference in the average counts between the two binned windspeed categories.
        - Contrary to expectations, categorized high windspeeds do not show a considerable impact on the average bike count, suggesting further investigation is needed.
        """, unsafe_allow_html=True)

        # Display the image of the plot
        st.image("wind_binned.png", caption="Effect of Windspeed_Binned on Count", use_column_width=True)

    # Histogram of Windspeed Distribution
    with st.expander("Distribution of Windspeed"):
        st.subheader("Windspeed Distribution Analysis")
        st.markdown("""
        This section visualizes the distribution of windspeed in the dataset to understand its effect on bike rentals.
        
        **Insights:**
        - Most windspeed data points are below 40, with very few observations above this level
                - High windspeed values are less common, indicating potential outliers or extreme conditions in the data.
        """, unsafe_allow_html=True)

        plt.figure(figsize=(10, 6))
        sns.histplot(data['windspeed'], kde=True, bins=60, color='blue')
        plt.xlabel('Windspeed')
        plt.ylabel('Frequency')
        plt.title('Distribution of Windspeeds')
        st.pyplot(plt)

        # Count data points above and below the threshold of 40
        count_above = (data['windspeed'] > 40).sum()
        count_below = (data['windspeed'] <= 40).sum()
        st.write(f"**Number of records**: Windspeed > 40: {count_above}, Windspeed ≤ 40: {count_below}")

    # Average Count by Windspeed Analysis
    with st.expander("Average Count by Windspeed Analysis"):
        st.subheader("Average Bike Count by Windspeed")
        st.markdown("""
        This analysis explores how average bike rental counts change with varying levels of windspeed.
        
        **Key Observations:**
        - There is a peak in average bike count at specific high windspeed levels.
        - Outliers in high windspeed values may skew the overall average, suggesting potential data variability.
        """, unsafe_allow_html=True)

        # Calculate average count by windspeed
        average_count_by_windspeed = data.groupby('windspeed')['cnt'].mean().reset_index()

        # Plotting the average bike count by windspeed
        plt.figure(figsize=(16, 8))
        sns.lineplot(x='windspeed', y='cnt', data=average_count_by_windspeed)
        plt.xlabel('Windspeed')
        plt.ylabel('Average Bike Count')
        plt.title('Average Bike Count by Windspeed')
        max_windspeed = int(data['windspeed'].max())
        plt.xticks(range(0, max_windspeed + 1, 2))  # Adjust step size if needed
        st.pyplot(plt)

        st.write("""
        **Summary**: The highest windspeed values show noticeable peaks, which could impact average bike count analysis due to limited data. Care should be taken to evaluate how these peaks affect overall trends.
        """)

        # Expander for the high windspeed analysis
    with st.expander("Counts for Windspeeds Above 40 Analysis"):
        st.subheader("🌬️ Counts for Windspeeds Above 40")
        st.markdown("""
        This section explores the relationship between bike counts and high windspeed values above 40.
        
        **Analysis:**
        - The scatter plot below shows bike rental counts at windspeed levels exceeding 40.
        - It highlights that there is limited data for these high windspeed observations, suggesting that any average computed will be significantly influenced by these few data points.
        - The variability in count values at these windspeed levels confirms the need for careful consideration when deciding to include `windspeed_binned`, `windspeed`, or neither as a feature in further analysis.
        """, unsafe_allow_html=True)

        # Display the image of the plot
        st.image("count_windspeed.png", caption="Counts for Windspeeds Above 40", use_column_width=True)

    # 4. Correlation Analysis
    st.header("🔗 Correlation Analysis")
    
    # Correlation Matrix Analysis
    with st.expander("Correlation Matrix Overview"):
        st.subheader("Exploring Relationships Between Variables")
        st.markdown("""
        This section shows the correlation between numerical features in the dataset using a correlation matrix. Understanding these relationships helps with feature selection and model building.
        """, unsafe_allow_html=True)

        # Display correlation matrix image
        st.image('output_corre_matrix.png', caption='Correlation Matrix Analysis', use_column_width=True)

        st.write("""
        **Key Insights from the Correlation Matrix:**
        - Variables like `registered` and `cnt` show strong positive correlations.
        - The `windspeed_binned` variable displays lower correlations compared to continuous `windspeed`, potentially impacting predictive power.
        - `temp` and `atemp` have high correlations with each other as expected, indicating redundancy in these features.
        """)

    # Conclusion for Correlation Analysis
        st.write("""
        **Conclusion**: The findings highlight that while `windspeed_binned` might be useful, its impact should be tested against continuous `windspeed` to verify effectiveness. Also, the correlation between temperature variables implies that only one should be chosen to avoid multicollinearity.
        """)

    # 5. Lagged Variables
    st.header("🕒 Lagged Variable Analysis")
    
    # Lagged Temperature Analysis
    with st.expander("Lagged Temperature Impact on Rentals"):
        st.subheader("Lagged Variables Analysis")
        st.markdown("""
        By shifting temperature values to create lagged features, we examine their impact on bike rental counts.
        
        **Key Observations:**
        - The 1-hour lagged temperature shows the highest correlation, possibly because people consider current weather before renting bikes.
        - The correlation diminishes with increased lag time, suggesting the immediacy of temperature data is more relevant.
        """, unsafe_allow_html=True)

        # Display lagged correlation bar chart image
        st.image("lagged_histogram.png", caption="Correlation of Temperature, Apparent Temperature, and Lagged Features with Count (cnt)")

    # Temperature Feature Correlation Matrix
    with st.expander("📊 Detailed Temperature Feature Correlation Matrix"):
        st.subheader("Temperature Feature Correlation Matrix")
        st.markdown("""
        We analyze the correlation matrix of lagged temperature features to identify multicollinearity and determine the most impactful variable.
        """, unsafe_allow_html=True)

        # Display correlation matrix for lagged temperature features
        st.image("corre_lagged.png", caption="Correlation Matrix of Temperature Features and Count (cnt)")

        st.write("""
        **Insights:**
        - Significant multicollinearity among lagged features suggests selecting only the most relevant variable to avoid redundancy.
        - The 1-hour lagged temperature (`temp_expected_1`) showed the highest correlation, making it a prime candidate for further model testing.
        """)

    st.header("🌧️ Analysis of Weather Situation and Its Impact on Count")
    
    # Expander for Weather Situation Analysis 1
    with st.expander("Initial Weather Situation Analysis"):
        st.subheader("Effect of Weather Situation on Count")
        st.markdown("""
        In this analysis, we explore the distribution of bike rental counts across different weather situations (`weathersit`). The categories are:
        - `1`: Clear or mostly clear skies
        - `2`: Partly cloudy skies
        - `3`: Light precipitation
        - `4`: Heavy precipitation
        
        **Insights:**
        - `weathersit` categories 1 and 2 display a similar pattern with relatively higher rental counts.
        - Categories 3 and 4, which indicate precipitation, show lower counts, likely due to less favorable weather for bike rentals.
        """)

        # Insert the image file for the initial weather analysis
        st.image('weathersit1.png', caption="Boxplot of `weathersit` and Count", use_column_width=True)

        st.markdown("""
        Given the similar behavior of categories 1 and 2, and categories 3 and 4, we decided to combine them into a simpler feature.
        """)

    # Expander for Binned Weather Situation Analysis
    with st.expander("Binned Weather Situation Analysis"):
        st.subheader("Simplified Weather Situation (Dry vs. Precipitation)")
        st.markdown("""
        To simplify modeling, we created a new feature called `dry_precip`:
        - `1`: Dry weather (`weathersit` 1 and 2)
        - `2`: Precipitation (`weathersit` 3 and 4)

        This helps reduce the complexity of handling multiple categories and focuses on whether precipitation impacts bike rentals.
        """)

        # Insert the image file for the simplified binned weather analysis
        st.image('weathersit2.png', caption="Boxplot of `dry_precip` and Count", use_column_width=True)

        st.write("""
        **Observations:**
        - Dry weather conditions (category 1) tend to have higher rental counts.
        - The presence of precipitation (category 2) correlates with a notable drop in rentals.
        """)

    with st.expander("Correlation Analysis for Weather and Precipitation"):
        st.subheader("Correlation Insights Between Weather Features and Bike Rentals")
        st.markdown("""
        This section presents a heatmap that illustrates the correlation between `cnt` (bike rental counts), the original `weathersit` feature, and the new `dry_precip` variable. The goal is to identify which feature may better represent weather-related influences on bike rentals.
        """, unsafe_allow_html=True)

    # Display the correlation image
        st.image('correlation_presipitation.png', caption='Correlation Heatmap for Weather Variables and Count (cnt)', use_column_width=True)

    # Client-focused summary
        st.write("""
        **Key Insights**:
        - The correlation heatmap indicates that both `weathersit` and `dry_precip` exhibit similar correlations with `cnt`, which aligns with expectations.
        - Further testing in predictive models will determine if the simpler `dry_precip` variable or the original `weathersit` provides better performance.
        """)


    with st.expander("Precipitation Intensity Bins Analysis"):
        st.markdown("""
        <h3>Understanding Precipitation Intensity Bins</h3>
        <p>We categorized precipitation levels into three bins based on the <code>weathersit</code> variable:</p>
        <ul>
            <li><strong>1</strong>: Represents dry conditions (weathersit 1 and 2).</li>
            <li><strong>2</strong>: Indicates mild precipitation (weathersit 3).</li>
            <li><strong>3</strong>: Denotes heavy precipitation (weathersit 4).</li>
        </ul>
        <p>Visualizing the distribution of bike counts across these bins provides insights into how different precipitation levels impact bike rentals.</p>
        """, unsafe_allow_html=True)
        
        # Display the saved image
        st.image("preci_bin.png", caption="Precipitation Intensity Bins Effect on Count", use_column_width=True)

        st.write("""
        **Key Insights:**
        - The distribution indicates that dry conditions (bin 1) show higher bike counts.
        - Bins 2 and 3, representing precipitation, show a clear decline in bike counts, with heavy precipitation having the lowest counts.
        - This analysis supports the decision to create distinct bins for better predictive modeling.
        """)
    with st.expander("Frequency Distribution of Weather Situations"):
        st.subheader("Distribution Analysis of Weather Situations")
    
        # Display the image
        st.image("bins_histogram.png", caption="Frequency Distribution of Weather Situation (weathersit)")
    
    # Add insights explanation
        st.markdown("""
        The frequency distribution of weather situations shows that:
        - Weather situation 1 (Clear) has the highest count with 11,413 occurrences.
        - Weather situation 2 (Cloudy) follows with 4,544 observations.
        - Situations with precipitation (3 and 4) are significantly less frequent, with 1,419 for situation 3.
    
        **Conclusion**:
        The limited data for weather situation 4 suggests that it may not be significant for modeling due to its minimal representation. This justifies not considering the `precip_intensity` feature in further analysis.
        """)






