import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_stats

st.title("Your Stats")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in from the home page.")
else:
    response = get_stats()
    if response and response.status_code == 200:
        stats = response.json()
        
        # Display total poops
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
        
        # Show raw data in a table
        st.subheader("Raw Data")
        df = pd.DataFrame(stats["daily_counts"])
        st.dataframe(df)
    else:
        st.error("Error fetching stats.")

