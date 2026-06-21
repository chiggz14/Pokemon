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
    df = pd.read_excel("pokemon.xlsx")
    
    # Create combined type column
    df["Type Combined"] = df["Type1"].fillna('') + " / " + df["Type2"].fillna('')
    df["Type Combined"] = df["Type Combined"].str.replace(" / $", "", regex=True)
    
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

# Text filter - Pokemon
pokemon_filter = st.sidebar.text_input("Search Pokemon")

# Text filter - Type Combined
type_filter = st.sidebar.text_input("Search Type (Combined)")

# -----------------------------
# TYPE BUTTON FILTERS
# -----------------------------
st.sidebar.subheader("Filter by Type1")

unique_types = sorted(df["Type1"].dropna().unique())

selected_type = st.sidebar.radio(
    "Select Type1",
    options=["All"] + list(unique_types)
)

# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered_df = df.copy()

# Pokemon filter
if pokemon_filter:
    filtered_df = filtered_df[
        filtered_df["Pokemon"].str.contains(pokemon_filter, case=False, na=False)
    ]

# Type combined filter
if type_filter:
    filtered_df = filtered_df[
        filtered_df["Type Combined"].str.contains(type_filter, case=False, na=False)
    ]

# Type button filter
if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["Type1"] == selected_type
    ]

# -----------------------------
# DISPLAY TABLE
# -----------------------------
st.subheader("Pokemon Table")

st.dataframe(filtered_df, use_container_width=True)

# -----------------------------
# SUMMARY INFO
# -----------------------------
st.write(f"Showing {len(filtered_df)} Pokemon")