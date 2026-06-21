import streamlit as st
import pandas as pd

# -------------------------
# PAGE TITLE
# -------------------------
st.title("📊 Pokemon Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("pokemon.csv")
    return df

df = load_data()

# -------------------------
# DISPLAY DATA
# -------------------------
st.subheader("Pokemon Data")
st.dataframe(df)
