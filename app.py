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
# TYPE1 FILTER (BUTTON STYLE)
# -------------------------
st.sidebar.subheader("Filter by Type1")

# Get unique values
type1_values = sorted(df["Type1"].dropna().unique())

# Create radio (button-like selector)
selected_type = st.sidebar.radio(
    "Select Type1",
    options=["All"] + list(type1_values)
)

# -------------------------
# APPLY FILTER
# -------------------------
filtered_df = df.copy()

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["Type1"] == selected_type]

# -------------------------
# DISPLAY DATA
# -------------------------
st.subheader("Pokemon Data")
st.dataframe(filtered_df)

st.write(f"Showing {len(filtered_df)} rows")
