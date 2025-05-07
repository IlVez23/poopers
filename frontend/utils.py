import requests
import streamlit as st
import os
from datetime import datetime

# Hardcode the API URL
API_URL = "https://poopers-backend.onrender.com"
st.write(f"Debug: Using API URL: {API_URL}")  # Debug line

def login(username, password):
    try:
        full_url = f"{API_URL}/login"
        st.write(f"Debug: Attempting to connect to: {full_url}")  # Debug line
        response = requests.post(full_url, params={"username": username, "password": password})
        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state["token"] = token
            st.session_state["logged_in"] = True
            st.success("Login successful")
        else:
            st.error(f"Login failed: {response.text}")
    except Exception as e:
        st.error(f"Login error: {str(e)}")

def signup(username, password):
    try:
        full_url = f"{API_URL}/signup"
        st.write(f"Debug: Attempting to connect to: {full_url}")  # Debug line
        response = requests.post(full_url, params={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Signup successful!")
            return response.json()
        else:
            st.error(f"Signup failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Signup error: {str(e)}")
        return None


def auth_headers():
    if "token" not in st.session_state or not st.session_state["token"]:
        st.error("You need to log in first")
        st.session_state["logged_in"] = False
        return None
    return {"Authorization": f"Bearer {st.session_state['token']}"}

def post_questionnaire(answers: dict):
    headers = auth_headers()
    if not headers:
        return None
    return requests.post(f"{API_URL}/questionnaire", json=answers, headers=headers)

def post_daily_input(date: str, count: int, poop_type: str, color: str, size: str):
    headers = auth_headers()
    if not headers:
        return None
        
    try:
        # Convert string date to ISO format
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        # Ensure count is an integer
        count = int(count)
        response = requests.post(
            f"{API_URL}/daily_input", 
            json={
                "poop_date": date_obj.isoformat(),
                "poop_count": count,
                "poop_type": poop_type,
                "poop_color": color,
                "poop_size": size
            }, 
            headers=headers
        )
        if response.status_code != 200:
            if response.status_code == 403:
                st.error("Your session has expired. Please log in again.")
                st.session_state["logged_in"] = False
                st.session_state["token"] = ""
            else:
                st.error(f"Failed to save input. Status code: {response.status_code}, Error: {response.text}")
            return None
        return response
    except ValueError as e:
        if "date" in str(e):
            st.error(f"Invalid date format. Please use YYYY-MM-DD format.")
        else:
            st.error(f"Invalid count value. Please enter a valid number.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def get_stats():
    headers = auth_headers()
    if not headers:
        return None
    return requests.get(f"{API_URL}/stats", headers=headers)
