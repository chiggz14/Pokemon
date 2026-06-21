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
    df = pd.read_excel("Pokemon.xlsx")
    
    # Create combined type column
    df["Type Combined"] = df["Type1"].fillna('') + " / " + df["Type2"].fillna('')
    df["Type Combined"] = df["Type Combined"].str.replace(" / $", "", regex=True)
    
    return df

df = load_data()
