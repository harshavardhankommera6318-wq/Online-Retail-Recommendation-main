import pandas as pd

from src.data_cleaning import clean_data
from src.recommender import (
    popular_products,
    customer_recommendations,
    category_products
)


def sample_data():
    return pd.DataFrame({
        "transaction_id": ["T1", "T2", "T3", "T4"],
        "customer_id": ["C1", "C1", "C2", "C2"],
        "product_name": ["Laptop", "Mouse", "Laptop", "Keyboard"],
        "category": ["Electronics"] * 4,
        "subcategory": ["Electronics"] * 4,
        "quantity": [2, 3, 1, 4],
        "unit_price": [1000, 200, 1000, 300],
        "total_amount": [2000, 600, 1000, 1200],
        "purchase_month": ["January"] * 4
    })


def test_clean_data():
    df = sample_data()
    cleaned = clean_data(df)

    assert len(cleaned) == 4
    assert cleaned["quantity"].min() > 0


def test_popular_products():
    result = popular_products(sample_data(), 2)

    assert len(result) == 2
    assert result.iloc[0]["product_name"] == "Keyboard"


def test_customer_recommendations():
    df = sample_data()

    result = customer_recommendations(df, "C1", 5)

    assert "Laptop" not in result["product_name"].values
    assert "Mouse" not in result["product_name"].values


def test_category_products():
    result = category_products(
        sample_data(), "Electronics"
    )

    assert len(result) > 0
    assert "revenue" in result.columns