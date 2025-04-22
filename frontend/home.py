import requests
import streamlit as st
from utils import login, signup, post_questionnaire, auth_headers, post_daily_input, get_stats
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.title("Welcome")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.subheader("Login / Signup")
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            login(username, password)

    with tab2:
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Signup"):
            signup(new_user, new_pass)

else:
    st.success("You are logged in.")
    
    # Add logout button
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["token"] = ""
        st.experimental_rerun()

    st.title("🚽 Poop Tracker")

    # Create tabs for input and stats
    tab1, tab2 = st.tabs(["Daily Input", "Statistics"])
    
    with tab1:
        st.header("Daily Input")
        
        # Date input
        poop_date = st.date_input("Date", datetime.now())
        
        # Number input for count
        poop_count = st.number_input("Number of poops", min_value=0, max_value=10, value=1)
        
        # Selectboxes for type, color, and size
        poop_type = st.selectbox("Type", ["Normal", "Hard", "Soft", "Liquid"])
        poop_color = st.selectbox("Color", ["Brown", "Dark Brown", "Light Brown", "Green", "Yellow", "Red"])
        poop_size = st.selectbox("Size", ["Small", "Medium", "Large"])
        
        if st.button("Submit"):
            response = post_daily_input(
                poop_date.strftime("%Y-%m-%d"),
                poop_count,
                poop_type,
                poop_color,
                poop_size
            )
            
            if response and response.status_code == 200:
                st.success("Input saved successfully!")
            elif response:
                st.error(f"Failed to save input. Status code: {response.status_code}, Error: {response.text}")
    
    with tab2:
        st.header("Your Poop Statistics")
        
        # Fetch stats from backend
        response = get_stats()
        
        if response and response.status_code == 200:
            stats = response.json()
            
            # Display total poops with a big number
            st.metric("Total Poops", stats["total_poops"])
            
            # Create two columns for most common type and color
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Most Common Type", stats["most_common_type"])
            with col2:
                st.metric("Most Common Color", stats["most_common_color"])
            
            # Create daily count line chart
            if stats["daily_counts"]:
                df = pd.DataFrame(stats["daily_counts"])
                df["date"] = pd.to_datetime(df["date"])
                
                fig = px.line(df, x="date", y="count", 
                            title="Daily Poop Count Over Time",
                            labels={"date": "Date", "count": "Number of Poops"})
                fig.update_traces(mode="lines+markers")
                st.plotly_chart(fig, use_container_width=True)
            
            # Create distribution charts
            col3, col4 = st.columns(2)
            
            with col3:
                # Poop type distribution
                if stats["type_distribution"]:
                    df_type = pd.DataFrame(stats["type_distribution"])
                    fig_type = px.pie(
                        df_type,
                        values="count",
                        names="type",
                        title="Poop Type Distribution",
                        hover_data=["percentage"],
                        labels={"percentage": "Percentage"}
                    )
                    st.plotly_chart(fig_type, use_container_width=True)
            
            with col4:
                # Poop color distribution
                if stats["color_distribution"]:
                    df_color = pd.DataFrame(stats["color_distribution"])
                    fig_color = px.pie(
                        df_color,
                        values="count",
                        names="color",
                        title="Poop Color Distribution",
                        hover_data=["percentage"],
                        labels={"percentage": "Percentage"}
                    )
                    st.plotly_chart(fig_color, use_container_width=True)
        
        else:
            st.error("Failed to fetch statistics")
    
    # Logout button
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["token"] = ""
        st.experimental_rerun()
