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
    
    # Create Type Combined column
    df["Type Combined"] = df["Type1"].fillna('') + " / " + df["Type2"].fillna('')
    df["Type Combined"] = df["Type Combined"].str.replace(" / $", "", regex=True)
    
    return df

df = load_data()

# -------------------------
# FILTER (Type1 values → Type Combined logic)
# -------------------------
st.sidebar.subheader("Filter by Type")

# Unique Type1 values (buttons source)
type1_values = sorted(df["Type1"].dropna().unique())

selected_type = st.sidebar.radio(
    "Select Type",
    options=["All"] + list(type1_values)
)

# -------------------------
# APPLY FILTER
# -------------------------
filtered_df = df.copy()

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["Type Combined"].str.contains(selected_type, case=False, na=False)
    ]

# -------------------------
# DISPLAY
# -------------------------
st.subheader("Pokemon Data")
st.dataframe(filtered_df)

st.write(f"Showing {len(filtered_df)} rows")
