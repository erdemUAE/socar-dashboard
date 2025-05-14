
import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_excel("SOCAR Entities.xlsx", sheet_name="Results")

# Simplify and rename columns
df = df[[
    "Company name Latin alphabet",
    "Country ISO code",
    "Status",
    "BvD sectors",
    "GUO - Name",
    "GUO - Country ISO code",
    "GUO - As sanctions",
    "GUO - As watchlist",
    "GUO - As PEP",
    "GUO - As media"
]]

df.columns = [
    "CompanyName", "CountryISO", "Status", "Sector",
    "GUO_Name", "GUO_CountryISO", "Sanctions",
    "Watchlist", "PEP", "Media"
]

# Sidebar filters
st.sidebar.title("Filters")
country_filter = st.sidebar.multiselect("Select Country", sorted(df["CountryISO"].dropna().unique()))
sector_filter = st.sidebar.multiselect("Select Sector", sorted(df["Sector"].dropna().unique()))
risk_flags = st.sidebar.multiselect(
    "Select Risk Flags",
    ["Sanctions", "Watchlist", "PEP", "Media"]
)

# Apply filters
filtered_df = df.copy()
if country_filter:
    filtered_df = filtered_df[filtered_df["CountryISO"].isin(country_filter)]
if sector_filter:
    filtered_df = filtered_df[filtered_df["Sector"].isin(sector_filter)]
for flag in risk_flags:
    filtered_df = filtered_df[filtered_df[flag] == "Yes"]

# Title
st.title("SOCAR Entity Risk Dashboard")

# World map
st.subheader("Entity Distribution by Country")
map_data = filtered_df["CountryISO"].value_counts().reset_index()
map_data.columns = ["CountryISO", "EntityCount"]
fig_map = px.choropleth(map_data, locations="CountryISO", color="EntityCount",
                        color_continuous_scale="Reds", title="Entities by Country")
st.plotly_chart(fig_map)

# Risk summary bar chart
st.subheader("Risk Summary")
risk_summary = pd.DataFrame({
    "Sanctions": (df["Sanctions"] == "Yes").sum(),
    "Watchlist": (df["Watchlist"] == "Yes").sum(),
    "PEP": (df["PEP"] == "Yes").sum(),
    "Media": (df["Media"] == "Yes").sum()
}, index=["Count"]).T.reset_index().rename(columns={"index": "RiskType"})
fig_risk = px.bar(risk_summary, x="RiskType", y="Count", title="Total Entities by Risk Type")
st.plotly_chart(fig_risk)

# Detailed Table
st.subheader("Detailed Entity Data")
st.dataframe(filtered_df.reset_index(drop=True))
