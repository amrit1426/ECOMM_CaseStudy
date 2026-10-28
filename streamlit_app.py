import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Sale Analysis", layout="wide")
st.title("🛒 E-Commerce Sale Analysis Dashboard")
st.markdown("Customer purchase behavior and sale insights.")

df = pd.read_csv("20251121_ECOMM_Dataset.csv")

with st.sidebar:
    st.header("Filters")
    cities = st.multiselect("City Category", options=df["City_Category"].dropna().unique(), default=df["City_Category"].dropna().unique())
    genders = st.multiselect("Gender", options=df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())
    age_min, age_max = st.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))

filtered = df[
    df["City_Category"].isin(cities) &
    df["Gender"].isin(genders) &
    df["Age"].between(age_min, age_max)
]

col1, col2, col3 = st.columns(3)
col1.metric("Transactions", len(filtered))
col2.metric("Total Revenue (₹)", f"{filtered['Purchase'].sum():,.0f}" if len(filtered) else "N/A")
col3.metric("Avg Purchase (₹)", f"{filtered['Purchase'].mean():,.0f}" if len(filtered) else "N/A")

st.subheader("Purchase by Product Category")
if len(filtered):
    cat = filtered.groupby("Product_Category")["Purchase"].mean().reset_index()
    fig = px.bar(cat, x="Product_Category", y="Purchase")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Purchase by Gender & City")
if len(filtered):
    pivot = filtered.groupby(["Gender", "City_Category"])["Purchase"].mean().reset_index()
    fig = px.bar(pivot, x="Gender", y="Purchase", color="City_Category", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Age Distribution")
if len(filtered):
    fig = px.histogram(filtered, x="Age", y="Purchase", histfunc="avg")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Data Preview")
st.dataframe(filtered.head(100))
