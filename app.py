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
    df["Type Combined"] = df["Type1"].fillna("") + " / " + df["Type2"].fillna("")
    df["Type Combined"] = df["Type Combined"].str.replace(" / $", "", regex=True)
    
    return df

df = load_data()

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("Filters")

# ---- TYPE FILTER (multi-select)
type_values = sorted(df["Type1"].dropna().unique())

selected_types = st.sidebar.multiselect(
    "Select Type(s)",
    options=type_values
)

# ---- GENERATION FILTER (multi-select)
generation_values = sorted(df["Generation"].dropna().unique())

selected_generations = st.sidebar.multiselect(
    "Select Generation(s)",
    options=generation_values
)

# -------------------------
# APPLY FILTERS
# -------------------------
filtered_df = df.copy()

# -------------------------
# TYPE FILTER
# -------------------------
if selected_types:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: all(
                t in [row["Type1"], row["Type2"]] for t in selected_types
            ),
            axis=1
        )
    ]

# -------------------------
# GENERATION FILTER
# -------------------------
if selected_generations:
    filtered_df = filtered_df[
        filtered_df["Generation"].isin(selected_generations)
    ]

# -------------------------
# POKEMON NAME FILTER
# -------------------------
if pokemon_input:
    names_list = [
        name.strip()
        for name in pokemon_input.replace("\n", ",").split(",")
        if name.strip()
    ]

    filtered_df = filtered_df[
        filtered_df["Pokemon"].str.lower().isin(
            [name.lower() for name in names_list]
        )
    ]
# -------------------------
# DISPLAY
# -------------------------
st.subheader("Pokemon Data")

st.dataframe(filtered_df, use_container_width=True)

st.write(f"Showing {len(filtered_df)} rows")

# -------------------------
# SHOW ACTIVE FILTERS
# -------------------------
st.markdown("### Active Filters")

if selected_types:
    st.write(f"Types: {', '.join(selected_types)}")
else:
    st.write("Types: All")

if selected_generations:
    st.write(f"Generation: {', '.join(map(str, selected_generations))}")
else:
    st.write("Generation: All")
