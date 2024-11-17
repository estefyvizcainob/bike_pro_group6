import streamlit as st

def introduction_page():
    # Add custom CSS for styling
    st.markdown(
        """
        <style>
        .main {
            background-color: #f9fafb; /* Light grey */
        }
        h1 {
            font-family: 'Georgia', serif;
            font-size: 48px;
            color: #2c3e50; /* Dark blue for the main title */
            text-align: center;
            margin-bottom: 0.5em;
        }
        h2 {
            color: #34495e; /* Subtle blue-gray for subtitles */
            font-family: 'Arial', sans-serif;
            margin-top: 1.5em;
            text-align: center;
        }
        .member-name {
            font-size: 22px;
            color: #2c3e50; /* Consistent dark blue */
            margin: 10px;
            font-weight: bold;
        }
        .introduction-text {
            font-size: 18px;
            color: #4a4a4a; /* Gray for readable text */
            line-height: 1.6;
            margin-bottom: 1.5em;
            text-align: justify;
        }
        .highlight {
            background-color: #e8f5e9; /* Light green background for emphasis */
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .team-section {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
            text-align: center;
        }
        .team-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page content
    st.title("🚴‍♂️ Advanced Bike Sharing Analysis and Prediction Tool")
    st.image("bike.jpg", use_column_width=True, caption="Understanding Bike Sharing Trends in Washington D.C.")

    st.subheader("Introduction")
    st.markdown("""
    <div class='introduction-text'>
    The city administration of Washington D.C. seeks to enhance their bike-sharing services through data-driven insights.
    This interactive app presents an extensive analysis of the bike-sharing service usage patterns and predictive modeling 
    based on data from 2011 and 2012. Explore the sections for detailed insights on factors affecting bike usage, daily 
    patterns, and future projections. Whether you are a policymaker, data enthusiast, or a curious user, this app offers 
    comprehensive knowledge to understand and improve bike-sharing experiences.
    </div>
    """, unsafe_allow_html=True)


    st.subheader("Meet the Team:")
    st.markdown("""
    <div class='team-container'>
        <div class='team-section'>
            <p class='member-name'>Matteo Becchis</p>
            <p class='member-name'>James Dieter Clayfield</p>
            <p class='member-name'>Tom Jansen</p>
            <p class='member-name'>Yousef Rimawi</p>
            <p class='member-name'>Luke Mercouris</p>
            <p class='member-name'>Estefanía Vizcaíno</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="border:1px solid #d4d4d4; margin: 20px 0;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <p class='introduction-text'>
    We invite you to explore the different sections of the app to uncover insights and see how data can make a real 
    impact on urban planning and daily life.
    </p>
    """, unsafe_allow_html=True)

