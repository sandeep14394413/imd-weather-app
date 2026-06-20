from datetime import date, timedelta
import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000")
INDIAN_STATES = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Delhi",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
]


st.set_page_config(page_title="India Weather Forecast", layout="wide")
st.title("India Weather Forecast")

with st.sidebar:
    st.header("Account")
    mode = st.radio("Mode", ["Login", "Sign up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    full_name = st.text_input("Full name") if mode == "Sign up" else None
    home_state = st.selectbox("Home state", INDIAN_STATES) if mode == "Sign up" else None

    if st.button(mode):
        endpoint = "/auth/signup" if mode == "Sign up" else "/auth/login"
        payload = {"email": email, "password": password}
        if mode == "Sign up":
            payload.update({"full_name": full_name, "home_state": home_state})
        response = requests.post(f"{API_URL}{endpoint}", json=payload, timeout=20)
        if response.ok:
            st.session_state["token"] = response.json()["access_token"]
            st.success("Signed in")
        else:
            st.error(response.text)

st.subheader("Forecast")
col1, col2, col3 = st.columns(3)
with col1:
    state = st.selectbox("State", INDIAN_STATES)
with col2:
    district = st.text_input("District / city", placeholder="Optional")
with col3:
    target_date = st.date_input(
        "Target date",
        value=date.today() + timedelta(days=1),
        min_value=date.today(),
    )

if st.button("Predict weather", type="primary"):
    payload = {
        "state": state,
        "district": district or None,
        "target_date": target_date.isoformat(),
    }
    response = requests.post(f"{API_URL}/forecast", json=payload, timeout=30)
    if response.ok:
        data = response.json()
        m1, m2, m3 = st.columns(3)
        m1.metric("Maximum temperature", f"{data['tmax_c']:.1f} C")
        m2.metric("Minimum temperature", "N/A" if data["tmin_c"] is None else f"{data['tmin_c']:.1f} C")
        m3.metric("Rainfall", "N/A" if data["rainfall_mm"] is None else f"{data['rainfall_mm']:.1f} mm")
        st.info(f"{data['forecast_type']} forecast, confidence: {data['confidence']}. {data['note']}")
    else:
        st.error(response.text)
