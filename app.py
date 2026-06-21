import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Pokemon Dashboard", layout="wide")

st.title("📊 Pokemon Dashboard")
# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("pokemon.csv")
    return df

df = load_data()
