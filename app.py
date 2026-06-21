import streamlit as st
import pandas as pd

st.title("📊 Pokemon Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("pokemon.csv")
    
    df["Type Combined"] = df["Type1"].fillna('') + " / " + df["Type2"].fillna('')
    df["Type Combined"] = df["Type Combined"].str.replace(" / $", "", regex=True)
    
    return df

df = load_data()

# -------------------------
# MULTI-SELECT FILTER
# -------------------------
st.sidebar.subheader("Filter by Type")

type1_values = sorted(df["Type1"].dropna().unique())

selected_types = st.sidebar.multiselect(
    "Select Types",
    options=type1_values
)

# -------------------------
# APPLY FILTER
# -------------------------
filtered_df = df.copy()

if selected_types:
    pattern = "|".join(selected_types)
    filtered_df = filtered_df[
        filtered_df["Type Combined"].str.contains(pattern, case=False, na=False)
    ]

# -------------------------
# DISPLAY
# -------------------------
st.dataframe(filtered_df)

st.write(f"Showing {len(filtered_df)} rows")
