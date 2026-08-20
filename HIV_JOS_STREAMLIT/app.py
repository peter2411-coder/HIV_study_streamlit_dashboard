import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# 1. PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="HIV Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# 2. TITLE
# =========================================================

st.title("📊 HIV Data Analysis Dashboard")

st.subheader("Jos, Plateau State")

st.write(
    "Interactive analysis of an HIV study dataset "
    "from Jos, Plateau State."
)

st.divider()


# =========================================================
# 3. LOAD THE DATASET
# =========================================================

file_path = "data/HIV JOS STUDY.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="Cleaned data"
)


# =========================================================
# 4. BASIC DATA CLEANING
# =========================================================

# Convert important columns to numbers
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

df["CD4 Count"] = pd.to_numeric(
    df["CD4 Count"],
    errors="coerce"
)

df["Viral_load"] = pd.to_numeric(
    df["Viral_load"],
    errors="coerce"
)


# Remove rows where Age is missing
df = df.dropna(subset=["Age"])


# =========================================================
# 5. SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Dashboard Filters")

st.sidebar.write(
    "Use the options below to filter the data."
)


# Gender filter
gender_options = ["All"] + sorted(
    df["Gender"].dropna().astype(str).unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)


# LGA filter
lga_options = ["All"] + sorted(
    df["LGA"].dropna().astype(str).unique().tolist()
)

selected_lga = st.sidebar.selectbox(
    "LGA",
    lga_options
)


# Age group filter
age_group_options = ["All"] + sorted(
    df["Age_group"].dropna().astype(str).unique().tolist()
)

selected_age_group = st.sidebar.selectbox(
    "Age Group",
    age_group_options
)


# Treatment filter
treatment_options = ["All"] + sorted(
    df["Treatment_Status"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_treatment = st.sidebar.selectbox(
    "Treatment Status",
    treatment_options
)


# Outcome filter
outcome_options = ["All"] + sorted(
    df["Outcome"].dropna().astype(str).unique().tolist()
)

selected_outcome = st.sidebar.selectbox(
    "Outcome",
    outcome_options
)


# =========================================================
# 6. APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"].astype(str) == selected_gender
    ]


if selected_lga != "All":
    filtered_df = filtered_df[
        filtered_df["LGA"].astype(str) == selected_lga
    ]


if selected_age_group != "All":
    filtered_df = filtered_df[
        filtered_df["Age_group"].astype(str)
        == selected_age_group
    ]


if selected_treatment != "All":
    filtered_df = filtered_df[
        filtered_df["Treatment_Status"].astype(str)
        == selected_treatment
    ]


if selected_outcome != "All":
    filtered_df = filtered_df[
        filtered_df["Outcome"].astype(str)
        == selected_outcome
    ]


# =========================================================
# 7. DASHBOARD METRICS
# =========================================================

st.header("📌 Overview")

total_patients = len(filtered_df)

average_age = filtered_df["Age"].mean()

living_count = (
    filtered_df["Outcome"]
    .astype(str)
    .str.lower()
    .eq("living")
    .sum()
)

dead_count = (
    filtered_df["Outcome"]
    .astype(str)
    .str.lower()
    .eq("dead")
    .sum()
)


if total_patients > 0:
    dead_percentage = (dead_count / total_patients) * 100
else:
    dead_percentage = 0


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Patients",
    total_patients
)

col2.metric(
    "Average Age",
    f"{average_age:.1f}"
)

col3.metric(
    "Living",
    living_count
)

col4.metric(
    "Dead",
    dead_count
)


st.caption(
    f"Outcome rate for filtered records: "
    f"{dead_percentage:.1f}% recorded as Dead."
)


st.divider()


# =========================================================
# 8. DEMOGRAPHIC ANALYSIS
# =========================================================

st.header("👥 Demographic Analysis")


col1, col2 = st.columns(2)


# Gender chart
with col1:

    st.subheader("Gender Distribution")

    gender_counts = filtered_df["Gender"].value_counts()

    st.bar_chart(gender_counts)


# Age group chart
with col2:

    st.subheader("Age Group Distribution")

    age_group_counts = (
        filtered_df["Age_group"]
        .value_counts()
        .sort_index()
    )

    st.bar_chart(age_group_counts)


st.divider()


# =========================================================
# 9. GEOGRAPHICAL ANALYSIS
# =========================================================

st.header("📍 LGA Distribution")

lga_counts = filtered_df["LGA"].value_counts()

st.bar_chart(lga_counts)


st.divider()


# =========================================================
# 10. TREATMENT ANALYSIS
# =========================================================

st.header("💊 Treatment Analysis")


col1, col2 = st.columns(2)


with col1:

    st.subheader("Treatment Status")

    treatment_counts = (
        filtered_df["Treatment_Status"]
        .value_counts()
    )

    st.bar_chart(treatment_counts)


with col2:

    st.subheader("Adherence Level")

    adherence_counts = (
        filtered_df["Adherence_level"]
        .value_counts()
    )

    st.bar_chart(adherence_counts)


st.divider()


# =========================================================
# 11. CLINICAL ANALYSIS
# =========================================================

st.header("🧬 Clinical Analysis")


col1, col2 = st.columns(2)


with col1:

    st.subheader("CD4 Count Distribution")

    cd4_data = filtered_df["CD4 Count"].dropna()

    if len(cd4_data) > 0:

        fig, ax = plt.subplots()

        ax.hist(cd4_data, bins=10)

        ax.set_xlabel("CD4 Count")

        ax.set_ylabel("Number of Patients")

        ax.set_title("Distribution of CD4 Counts")

        st.pyplot(fig)

        plt.close(fig)

    else:

        st.info("No CD4 data available.")


with col2:

    st.subheader("CD4 Bands")

    cd4_band_counts = (
        filtered_df["CD4_band"]
        .value_counts()
    )

    st.bar_chart(cd4_band_counts)


st.divider()


# =========================================================
# 12. VIRAL LOAD
# =========================================================

st.header("🦠 Viral Load Analysis")


viral_load = filtered_df["Viral_load"].dropna()


if len(viral_load) > 0:

    fig, ax = plt.subplots()

    ax.hist(viral_load, bins=10)

    ax.set_xlabel("Viral Load")

    ax.set_ylabel("Number of Patients")

    ax.set_title("Viral Load Distribution")

    st.pyplot(fig)

    plt.close(fig)

else:

    st.info("No viral load data available.")


st.divider()


# =========================================================
# 13. OUTCOME ANALYSIS
# =========================================================

st.header("❤️ Outcome Analysis")


col1, col2 = st.columns(2)


with col1:

    st.subheader("Overall Outcome")

    outcome_counts = (
        filtered_df["Outcome"]
        .value_counts()
    )

    st.bar_chart(outcome_counts)


with col2:

    st.subheader("Outcome by Gender")

    outcome_gender = pd.crosstab(
        filtered_df["Gender"],
        filtered_df["Outcome"]
    )

    st.bar_chart(outcome_gender)


st.divider()


# =========================================================
# 14. OUTCOME BY AGE GROUP
# =========================================================

st.subheader("Outcome by Age Group")

outcome_age = pd.crosstab(
    filtered_df["Age_group"],
    filtered_df["Outcome"]
)

st.bar_chart(outcome_age)


st.divider()


# =========================================================
# 15. DATA TABLE
# =========================================================

st.header("📋 Dataset")


st.write(
    f"Showing {len(filtered_df)} records "
    "based on the selected filters."
)


# Do not publicly display Patient_ID
display_df = filtered_df.drop(
    columns=["Patient_ID"],
    errors="ignore"
)


st.dataframe(
    display_df,
    use_container_width=True
)


# =========================================================
# 16. FOOTER
# =========================================================

st.divider()

st.caption(
    "HIV Data Analysis Dashboard | "
    "Jos, Plateau State"
)
