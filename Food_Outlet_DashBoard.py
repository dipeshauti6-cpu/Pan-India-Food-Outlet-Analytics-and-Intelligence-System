import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Junk Food Outlet Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("Pan_India_Junk_Food_Outlets_3000_Rows_20_Columns_Cleaned.csv")

    df["Opening_Date"] = pd.to_datetime(
        df["Opening_Date"],
        errors="coerce"
    )

    return df

data = load_data()


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title(
    "Junk Food Outlet Analytics"
)


# ----------------------------------------------------------
# YEAR FILTER
# ----------------------------------------------------------

min_year = int(
    data["Opening_Date"]
    .dt.year
    .min()
)

max_year = int(
    data["Opening_Date"]
    .dt.year
    .max()
)


year_range = st.sidebar.slider(
    "Choose Year",
    value=(min_year, max_year),
    min_value=min_year,
    max_value=max_year,
    key="year_range"
)


# ----------------------------------------------------------
# BRAND FILTER
# ----------------------------------------------------------

brand = st.sidebar.multiselect(
    "Brand",
    data["Brand"].unique(),
    key="brand"
)


# ----------------------------------------------------------
# STATE FILTER
# ----------------------------------------------------------

state = st.sidebar.multiselect(
    "State",
    data["State"].unique(),
    key="state"
)


# ----------------------------------------------------------
# CATEGORY FILTER
# ----------------------------------------------------------

category = st.sidebar.multiselect(
    "Primary Category",
    data["Primary_Category"].unique(),
    key="category"
)


# ----------------------------------------------------------
# OUTLET FORMAT FILTER
# ----------------------------------------------------------

outlet_format = st.sidebar.multiselect(
    "Outlet Format",
    data["Outlet_Format"].unique(),
    key="outlet_format"
)


# ==========================================================
# FILTER DATA
# ==========================================================

filtered_df = data[
    (
        data["Opening_Date"].dt.year >= year_range[0]
    )
    &
    (
        data["Opening_Date"].dt.year <= year_range[1]
    )
]


if brand:

    filtered_df = filtered_df[
        filtered_df["Brand"].isin(brand)
    ]


if state:

    filtered_df = filtered_df[
        filtered_df["State"].isin(state)
    ]


if category:

    filtered_df = filtered_df[
        filtered_df["Primary_Category"].isin(category)
    ]


if outlet_format:

    filtered_df = filtered_df[
        filtered_df["Outlet_Format"].isin(outlet_format)
    ]


# ==========================================================
# SIDEBAR FOOTER
# ==========================================================

st.sidebar.divider()

st.sidebar.caption(
    "Pan-India Junk Food Outlet Data\n"
    "Analytics Dashboard"
)


# ==========================================================
# KPI CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)


# Total Outlets

col1.metric(
    label="Total Outlets",
    value=f"{filtered_df['Outlet_ID'].nunique():,}"
)


# Monthly Sales

col2.metric(
    label="Monthly Sales",
    value=f"₹{filtered_df['Monthly_Sales_INR'].sum():,.0f}"
)


# Average Order Value

col3.metric(
    label="Average Order Value",
    value=f"₹{filtered_df['Avg_Order_Value_INR'].mean():,.0f}"
)


# Monthly Orders

col4.metric(
    label="Monthly Orders",
    value=f"{filtered_df['Monthly_Orders'].sum():,.0f}"
)


st.divider()


# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "Dashboard",
        "Insight",
        "Raw Data"
    ]
)


# ==========================================================
# DASHBOARD TAB
# ==========================================================

with tab1:

    # ======================================================
    # FIRST ROW
    # ======================================================

    col1, col2 = st.columns(2)


    # ------------------------------------------------------
    # TOP 10 STATES
    # ------------------------------------------------------

    with col1:

        st.subheader(
            "Top 10 States",
            text_alignment="center"
        )


        top_states = (
            filtered_df
            .groupby("State")[
                "Monthly_Sales_INR"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
        )


        fig, ax = plt.subplots(
            figsize=(6, 4)
        )


        ax.barh(
            top_states.index,
            top_states.values
        )


        ax.set_xlabel(
            "Monthly Sales (₹)"
        )


        ax.set_title(
            "Top 10 States by Monthly Sales"
        )


        ax.invert_yaxis()

        plt.tight_layout()

        st.pyplot(fig)


    # ------------------------------------------------------
    # TOP 10 OUTLETS
    # ------------------------------------------------------

    with col2:

        st.subheader(
            "Top 10 Outlets",
            text_alignment="center"
        )


        top_outlets = (
            filtered_df
            .groupby("Outlet_Name")[
                "Monthly_Sales_INR"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
        )


        fig, ax = plt.subplots(
            figsize=(6, 4)
        )


        ax.bar(
            top_outlets.index,
            top_outlets.values
        )


        ax.set_xlabel(
            "Outlet"
        )


        ax.set_ylabel(
            "Monthly Sales (₹)"
        )


        ax.set_title(
            "Top 10 Outlets by Monthly Sales"
        )


        plt.xticks(
            rotation=45,
            ha="right"
        )


        plt.tight_layout()

        st.pyplot(fig)


    # ======================================================
    # DIVIDER
    # ======================================================

    st.divider()


    # ======================================================
    # SECOND ROW
    # ======================================================

    left, right = st.columns(2)


    # ------------------------------------------------------
    # CATEGORY DISTRIBUTION
    # ------------------------------------------------------

    with left:

        st.subheader(
            "Primary Category Distribution",
            text_alignment="center"
        )


        category_data = (
            filtered_df[
                filtered_df[
                    "Primary_Category"
                ] != "Unknown"
            ]
            .groupby(
                "Primary_Category"
            )[
                "Outlet_ID"
            ]
            .nunique()
            .sort_values(
                ascending=False
            )
            .head(8)
        )


        fig, ax = plt.subplots(
            figsize=(6, 4)
        )


        ax.pie(
            category_data.values,
            labels=category_data.index,
            autopct="%1.1f%%",
            wedgeprops={
                "width": 0.7
            }
        )


        ax.set_title(
            "Junk Food Category Distribution"
        )


        st.pyplot(fig)


    # ------------------------------------------------------
    # SALES VS ORDERS
    # ------------------------------------------------------

    with right:

        st.subheader(
            "Monthly Sales Vs Orders",
            text_alignment="center"
        )


        fig, ax = plt.subplots(
            figsize=(6, 4)
        )


        ax.scatter(
            filtered_df["Monthly_Orders"],
            filtered_df["Monthly_Sales_INR"],
            alpha=0.6
        )


        ax.set_xlabel(
            "Monthly Orders"
        )


        ax.set_ylabel(
            "Monthly Sales (₹)"
        )


        ax.set_title(
            "Monthly Sales Vs Monthly Orders"
        )


        plt.tight_layout()

        st.pyplot(fig)


# ==========================================================
# INSIGHT TAB
# ==========================================================

with tab2:

    st.subheader(
        "Key Insights"
    )


    if filtered_df.empty:

        st.warning(
            "No data available for the selected filters."
        )

    else:

        # --------------------------------------------------
        # STATE INSIGHT
        # --------------------------------------------------

        state_count = (
            filtered_df
            .groupby("State")[
                "Outlet_ID"
            ]
            .nunique()
            .sort_values(
                ascending=False
            )
        )


        if not state_count.empty:

            st.info(
                f"🏆 **Top State:** "
                f"{state_count.index[0]} "
                f"has {state_count.iloc[0]:,} outlets."
            )


        # --------------------------------------------------
        # CATEGORY INSIGHT
        # --------------------------------------------------

        category_count = (
            filtered_df[
                filtered_df[
                    "Primary_Category"
                ] != "Unknown"
            ]
            .groupby(
                "Primary_Category"
            )[
                "Outlet_ID"
            ]
            .nunique()
            .sort_values(
                ascending=False
            )
        )


        if not category_count.empty:

            st.info(
                f"🍔 **Most Common Category:** "
                f"{category_count.index[0]} "
                f"with {category_count.iloc[0]:,} outlets."
            )


        # --------------------------------------------------
        # CITY INSIGHT
        # --------------------------------------------------

        city_count = (
            filtered_df
            .groupby("City")[
                "Outlet_ID"
            ]
            .nunique()
            .sort_values(
                ascending=False
            )
        )


        if not city_count.empty:

            st.info(
                f"🏙️ **Top City:** "
                f"{city_count.index[0]} "
                f"has {city_count.iloc[0]:,} outlets."
            )


        # --------------------------------------------------
        # HIGHEST RATED CATEGORY
        # --------------------------------------------------

        category_rating = (
            filtered_df[
                filtered_df[
                    "Primary_Category"
                ] != "Unknown"
            ]
            .groupby(
                "Primary_Category"
            )[
                "Customer_Rating"
            ]
            .mean()
            .sort_values(
                ascending=False
            )
        )


        if not category_rating.empty:

            st.info(
                f"⭐ **Highest Rated Category:** "
                f"{category_rating.index[0]} "
                f"with an average rating of "
                f"{category_rating.iloc[0]:.2f}/5."
            )


        # --------------------------------------------------
        # HIGHEST SALES CATEGORY
        # --------------------------------------------------

        category_sales = (
            filtered_df[
                filtered_df[
                    "Primary_Category"
                ] != "Unknown"
            ]
            .groupby(
                "Primary_Category"
            )[
                "Monthly_Sales_INR"
            ]
            .mean()
            .sort_values(
                ascending=False
            )
        )


        if not category_sales.empty:

            st.info(
                f"💰 **Highest Average Sales Category:** "
                f"{category_sales.index[0]} "
                f"with average monthly sales of "
                f"₹{category_sales.iloc[0]:,.0f}."
            )


        # --------------------------------------------------
        # TOP BRAND
        # --------------------------------------------------

        brand_sales = (
            filtered_df
            .groupby("Brand")[
                "Monthly_Sales_INR"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        if not brand_sales.empty:

            st.info(
                f"🏪 **Top Brand by Sales:** "
                f"{brand_sales.index[0]} "
                f"with total monthly sales of "
                f"₹{brand_sales.iloc[0]:,.0f}."
            )


# ==========================================================
# RAW DATA TAB
# ==========================================================

with tab3:

    st.subheader(
        "Raw Data"
    )


    st.write(
        f"Total Records: "
        f"**{len(filtered_df):,}**"
    )


    st.dataframe(
        filtered_df,
        use_container_width=True
    )


    # ------------------------------------------------------
    # DOWNLOAD
    # ------------------------------------------------------

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_junk_food_outlets.csv",
        mime="text/csv"
    )