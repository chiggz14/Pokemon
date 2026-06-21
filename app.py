import streamlit as st
import pandas as pd

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Pokemon Dashboard", layout="wide")

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
# SIDEBAR - MULTI SELECT FILTER
# -------------------------
st.sidebar.header("Filters")

# Get unique Type1 values
type1_values = sorted(df["Type1"].dropna().unique())

selected_types = st.sidebar.multiselect(
    "Select one or more Types",
    options=type1_values
)

# -------------------------
# APPLY FILTER (STRICT AND LOGIC)
# -------------------------
filtered_df = df.copy()

if selected_types:
    filtered_df = df[
        df.apply(
            lambda row: all(
                t in [row["Type1"], row["Type2"]] for t in selected_types
            ),
            axis=1
        )
    ]

# -------------------------
# DISPLAY DATA
# -------------------------
st.subheader("Pokemon Data")

