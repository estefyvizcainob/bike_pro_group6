import streamlit as st

def business_insights_page():
    # Page Title and Introduction
    st.title("🚲 Business Analysis, Insights, and Recommendations for Bike Rental Operations")
    st.write("""
    This report highlights key findings from our analysis of bike rental patterns and provides actionable recommendations 
    to optimize operations. By analyzing temporal trends, weather impacts, and peak usage, we identified opportunities to 
    improve bike availability, maintenance scheduling, and operational efficiency.
    """)

    # Main Takeaways
    st.markdown("## 🌟 Main Takeaways")
    st.write("""
    - **🛠️ Maintenance Scheduling**: Optimize maintenance during nighttime hours to reduce disruption.
    - **🚴‍♂️ Fleet Optimization**: Expand the fleet during peak hours to handle surges and cover maintenance overlaps.
    - **🔄 Strategic Reallocation**: Reallocate bikes dynamically to meet peak demand and adjust for weekend usage.
    """)

    st.write("For more details on each insight, expand the sections below:")

    # Insight 1: Maintenance Scheduling and Bike Availability
    with st.expander("1. Maintenance Scheduling and Bike Availability 🛠️"):
        st.write("""
        **Insight:** Our analysis of bike usage by hour and season revealed distinct peaks in demand, especially during 
        morning (7–9 AM) and evening (5–7 PM) commuting hours on working days, and steady midday usage (11 AM–5 PM) on 
        non-working days.

        **Key Observations:**
        - **Seasonal Influence**: The highest average counts occurred during summer months (June–August), with weekends showing increased recreational demand.
        - **Nighttime Lows**: Usage between midnight and 5 AM remained consistently low across all months and days, making it an ideal time for maintenance.
        
        **Recommendation:**
        - **Maintenance Timing**: Schedule regular maintenance during nighttime hours (12 AM–5 AM) when demand is lowest. For peak seasons, allocate a percentage of the fleet for preventive maintenance overnight to avoid disruptions.
        - **Seasonal Preparations**: Conduct thorough fleet inspections and repairs in late winter (February–March) to prepare for the summer surge.
        """)

    # Insight 2: Bike Fleet Optimization and Purchasing Strategy
    with st.expander("2. Bike Fleet Optimization and Purchasing Strategy 🚴‍♂️"):
        st.write("""
        **Insight:** The analysis of maximum hourly bike counts across the dataset revealed that demand occasionally reaches 
        near-capacity levels, particularly during peak commuting hours in summer.

        **Key Observations:**
        - **Hourly Maxima**: Some hours, especially during rush periods, approached the upper limit of the current bike fleet.
        - **Maintenance Overlap**: During peak hours, even a small portion of bikes being unavailable for maintenance could lead to unmet demand and lost revenue.
        
        **Recommendation:**
        - **Fleet Expansion**: If the fleet is consistently operating near maximum capacity during peak hours, consider purchasing a percentage more bikes to handle surges and cover maintenance overlaps.
        - **Dynamic Maintenance**: Implement a rotation system where only a fraction of bikes in high-demand areas are sent for maintenance during peak seasons.
        - **Data Tracking**: Incorporate data on location-specific usage in the future to optimize bike reallocation strategies further.
        """)

    # Insight 3: Strategic Reallocation of Bikes
    with st.expander("3. Strategic Reallocation of Bikes 🔄"):
        st.write("""
        **Insight:** While we lack location-specific data, temporal patterns suggest opportunities to reallocate bikes 
        dynamically across different time windows.

        **Key Observations:**
        - **Rush Hour Clusters**: Demand surges in the morning and evening but drops sharply midday on working days. On weekends, demand rises steadily through the day.
        - **Operational Downtime**: Bikes in areas with low demand during off-peak hours could be strategically moved to high-demand zones for the next surge.
        
        **Recommendation:**
        - **Rush Hour Redistribution**: Ensure that bikes are concentrated in high-traffic areas before 7 AM and again before 4 PM on working days to meet commuter demand.
        - **Weekend Strategy**: Allocate bikes evenly across stations for steady recreational usage on non-working days.
        - **Future Integration**: Consider incorporating GPS data or station-level demand in future analyses to refine reallocation efforts.
        """)

    # Conclusion
    st.subheader("Conclusion")
    st.write("""
    By analyzing bike usage patterns, we identified actionable insights to improve bike rental operations:
    1. 🛠️ Schedule maintenance during nighttime and off-peak hours to minimize disruptions.
    2. 🚴‍♂️ Expand the fleet by a percentage to handle peak demand and maintenance overlaps.
    3. 🔄 Dynamically reallocate bikes based on temporal usage patterns to maximize availability during peak hours.
    These strategies, supported by our analysis and visual evidence, will help ensure customer satisfaction, reduce 
    downtime, and optimize fleet operations for sustained growth in bike rentals.
    """)

    # Add the image at the end
    st.image("business_insight3.png", caption="Supporting Visuals for Business Insights")


 



