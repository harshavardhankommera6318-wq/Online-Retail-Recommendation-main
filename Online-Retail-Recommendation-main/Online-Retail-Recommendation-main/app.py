import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.data_cleaning import load_data
from src.recommender import (
    popular_products,
    customer_recommendations,
    category_products
)

st.set_page_config(
    page_title="Online Retail Recommendation System",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ Online Retail Recommendation System")
st.write(
    "A machine learning recommendation dashboard "
    "for analysing retail transactions and suggesting products."
)

# Load dataset
try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Run: python generate_data.py")
    st.stop()

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Retail Overview",
        "Popular Products",
        "Customer Recommendations",
        "Category Explorer"
    ]
)

st.sidebar.success("Dataset loaded successfully")

# Retail Overview
if page == "Retail Overview":

    st.header("Retail Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Transactions", len(df))
    col2.metric("Customers", df["customer_id"].nunique())
    col3.metric("Products", df["product_name"].nunique())
    col4.metric(
        "Total Revenue",
        f"₹{df['total_amount'].sum():,.0f}"
    )

    st.subheader("Revenue by Category")

    category_sales = (
        df.groupby("category")["total_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

    st.subheader("Transaction Dataset")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download Transaction Dataset",
        df.to_csv(index=False),
        file_name="retail_transactions.csv",
        mime="text/csv"
    )


# Popular Products
elif page == "Popular Products":

    st.header("🔥 Most Popular Products")

    top_n = st.slider(
        "Number of recommendations",
        min_value=3,
        max_value=15,
        value=5
    )

    result = popular_products(df, top_n)

    st.dataframe(result, use_container_width=True)

    st.subheader("Popular Product Chart")

    chart = result.set_index("product_name")
    st.bar_chart(chart["units_sold"])

    st.download_button(
        "Download Popular Products",
        result.to_csv(index=False),
        file_name="popular_products.csv",
        mime="text/csv"
    )


# Customer Recommendations
elif page == "Customer Recommendations":

    st.header("🎯 Personalized Recommendations")

    customers = sorted(df["customer_id"].unique())

    customer_id = st.selectbox(
        "Choose Customer",
        customers
    )

    st.subheader("Previously Purchased Products")

    purchased = df[
        df["customer_id"] == customer_id
    ]["product_name"].unique()

    st.write(", ".join(purchased))

    top_n = st.slider(
        "Number of recommended products",
        3, 10, 5
    )

    recommendations = customer_recommendations(
        df,
        customer_id,
        top_n
    )

    st.subheader("Recommended Products")
    st.dataframe(
        recommendations,
        use_container_width=True
    )

    st.download_button(
        "Download Recommendations",
        recommendations.to_csv(index=False),
        file_name="customer_recommendations.csv",
        mime="text/csv"
    )


# Category Explorer
elif page == "Category Explorer":

    st.header("📊 Category Explorer")

    categories = sorted(df["category"].unique())

    selected_category = st.selectbox(
        "Choose Product Category",
        categories
    )

    result = category_products(df, selected_category)

    st.dataframe(result, use_container_width=True)

    st.subheader("Revenue by Product")

    st.bar_chart(
        result.set_index("product_name")["revenue"]
    )

    st.download_button(
        "Download Category Report",
        result.to_csv(index=False),
        file_name="category_report.csv",
        mime="text/csv"
    )


st.divider()

st.caption(
    "Online Retail Recommendation System | "
    "Machine Learning Internship Project 3"
)