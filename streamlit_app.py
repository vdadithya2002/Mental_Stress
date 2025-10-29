# streamlit_app.py
import streamlit as st

st.title("Hyderabad Stress Zone Dashboard")
st.dataframe(df)
st.map(df[['lat', 'lon']])