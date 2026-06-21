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

# ---- TYPE FILTER
type_values = sorted(df["Type1"].dropna().unique())

selected_types = st.sidebar.multiselect(
    "Select Type(s)",
    options=type_values
)

# ---- GENERATION FILTER
generation_values = sorted(df["Generation"].dropna().unique())

selected_generations = st.sidebar.multiselect(
    "Select Generation(s)",
    options=generation_values
)

# ---- POKEMON EXCLUDE FILTER (PARTIAL MATCH)
st.sidebar.subheader("Exclude Pokemon")

pokemon_input = st.sidebar.text_area(
    "Exclude Pokemon (use ':' separator, supports partial match e.g. 'char:pika')"
)

# -------------------------
# APPLY FILTERS
# -------------------------
filtered_df = df.copy()

# ---- TYPE FILTER (AND logic)
if selected_types:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: all(
                t in [row["Type1"], row["Type2"]] for t in selected_types
            ),
            axis=1
        )
    ]

# ---- GENERATION FILTER
if selected_generations:
    filtered_df = filtered_df[
        filtered_df["Generation"].isin(selected_generations)
    ]

# ---- POKEMON EXCLUDE FILTER (PARTIAL MATCH)
if pokemon_input:
    # Split using ":" and clean input
    names_list = [
        name.strip()
        for name in pokemon_input.split(":")
        if name.strip()
    ]

    if names_list:
        # Create regex pattern for partial matching
        pattern = "|".join(names_list)

        # Exclude matches
        filtered_df = filtered_df[
            ~filtered_df["Pokemon"].str.contains(pattern, case=False, na=False)
        ]

# -------------------------
# DISPLAY DATA
# -------------------------
st.subheader("Pokemon Data")

st.dataframe(filtered_df, use_container_width=True)

st.write(f"Showing {len(filtered_df)} rows")

# -------------------------
# ACTIVE FILTERS DISPLAY
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

if pokemon_input:
    st.write(f"Excluded patterns: {pokemon_input}")
else:
    st.write("Pokemon: None excluded")




# -------------------------
# COPYABLE LIST OUTPUT
# -------------------------
st.subheader("Filtered Pokemon List (Copy Friendly)")

# Get list of Pokemon names
pokemon_list = filtered_df["Pokemon"].dropna().tolist()

# Convert to newline-separated string
pokemon_text = "\n".join(pokemon_list)

# Display in text area for easy copy
st.text_area(
    "Copy this list:",
    value=pokemon_text,
    height=250
)

