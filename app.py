import streamlit as st
import pandas as pd

st.title("Badminton Dashboard Working!")

df = pd.read_csv("data/bwf_ms_matches.csv")

st.write("Data loaded successfully")
st.write(df.head())